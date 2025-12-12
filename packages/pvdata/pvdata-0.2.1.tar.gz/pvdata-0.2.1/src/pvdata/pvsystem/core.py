"""
PV潜力计算核心函数

整合POA辐照度、电池温度、DC功率计算的主函数
"""

from typing import Union, List, Dict, Optional, Any
import pandas as pd
import numpy as np

from ..utils.logger import get_logger
from ..utils.decorators import log_execution
from ..utils.exceptions import PVDataError

from .module_config import ModuleConfig
from .irradiance import calculate_poa_irradiance
from .temperature import calculate_cell_temperature
from .power import calculate_dc_power, calculate_efficiency, calculate_ac_power
from .utils import (
    load_module_config,
    resolve_outputs,
    validate_input_data,
    check_required_columns,
    clip_physical_values,
)
from .constants import ALL_OUTPUT_COLUMNS

logger = get_logger(__name__)


@log_execution(level="info")
def calculate_pv_potential(
    df: pd.DataFrame,
    module: Union[str, Dict, ModuleConfig],
    surface_tilt: Union[float, str],
    surface_azimuth: Union[float, str],
    outputs: Union[List[str], str] = "default",
    temp_model: str = "sapm",
    apply_thermal_inertia: bool = True,
    recalculate_sun_position: bool = False,
    mounting_type: Optional[str] = None,
    module_height: float = 1.0,
    validate_inputs: bool = True,
    strict_mode: bool = False,
    inplace: bool = False,
    **kwargs,
) -> pd.DataFrame:
    """
    计算光伏组件的发电潜力（向量化）

    这是pvdata的主要PV计算函数，支持完整的物理计算链：
    太阳位置 → POA辐照度 → 电池温度 → DC功率 → 转换效率

    Parameters
    ----------
    df : pd.DataFrame
        输入数据，必须包含以下列：
        - GHI, DNI, DHI: 辐照度 [W/m²]
        - Temperature: 环境温度 [°C]
        - Wind Speed: 风速 [m/s]
        - timestamp: 时间戳（DatetimeIndex或列）
        - lat, lon: 纬度经度（如果recalculate_sun_position=True）

    module : str, dict, or ModuleConfig
        光伏组件参数，支持三种输入方式：
        1. CEC数据库名称 (str)
        2. 完整CEC参数字典 (dict)
        3. ModuleConfig对象

    surface_tilt : float or str
        组件倾角 [度]，0-90°
        - float: 固定倾角
        - str: 列名（支持每行不同倾角）

    surface_azimuth : float or str
        组件方位角 [度]，0-360°
        - float: 固定方位角
        - str: 列名

    outputs : list of str or 'default' or 'all', default 'default'
        指定输出列
        - 'default': poa_global, cell_temperature, dc_power, efficiency
        - 'all': 所有可能的列
        - list: 自定义列名列表

    temp_model : str, default 'sapm'
        温度模型: 'sapm' or 'pvsyst'

    apply_thermal_inertia : bool, default True
        是否应用Prilliman热惯性模型

    recalculate_sun_position : bool, default False
        是否重新计算太阳位置

    mounting_type : str, optional
        安装方式，覆盖自动推断

    module_height : float, default 1.0
        组件离地高度 [m]

    validate_inputs : bool, default True
        是否验证输入数据

    strict_mode : bool, default False
        严格模式（遇到异常抛出错误）

    inplace : bool, default False
        是否原地修改DataFrame

    **kwargs : optional
        额外参数:
        - sun_position_method: str
        - diffuse_model: str
        - prilliman_unit_mass: float
        - temp_model_params: dict

    Returns
    -------
    pd.DataFrame
        原数据 + 新增的输出列

    Raises
    ------
    PVDataError
        如果输入验证失败或计算过程出错

    Examples
    --------
    >>> import pvdata as pv
    >>> df = pv.read_parquet('Beijing_2016_10min.parquet')
    >>> df_pv = pv.calculate_pv_potential(
    ...     df,
    ...     module='Canadian_Solar_Inc__CS5A_150M',
    ...     surface_tilt=30,
    ...     surface_azimuth=180
    ... )
    >>> print(df_pv[['poa_global', 'cell_temperature', 'dc_power', 'efficiency']].head())

    Notes
    -----
    - 向量化实现，52,704行数据约需5-10秒
    - 支持10分钟分辨率数据（最佳）
    - 夜间数据也会计算，电池温度反映热惯性
    """
    # ========== 步骤0: 初始化 ==========
    if not inplace:
        df = df.copy()

    logger.info(
        f"Starting PV potential calculation for {len(df):,} records, "
        f"module={module if isinstance(module, str) else 'custom'}"
    )

    # ========== 步骤1: 加载模块配置 ==========
    module_config = load_module_config(
        module,
        mounting_type=mounting_type,
        temp_model_params=kwargs.get("temp_model_params"),
        unit_mass=kwargs.get("prilliman_unit_mass"),
    )
    logger.debug(f"Loaded module config: {module_config}")

    # ========== 步骤2: 解析输出需求 ==========
    output_columns = resolve_outputs(outputs, ALL_OUTPUT_COLUMNS)
    logger.debug(f"Output columns requested: {output_columns}")

    # ========== 步骤3: 输入验证 ==========
    if validate_inputs:
        required_cols = ["GHI", "Temperature", "Wind Speed"]
        if recalculate_sun_position:
            required_cols.extend(["timestamp", "lat", "lon"])

        is_valid, issues = validate_input_data(df, required_cols, strict_mode)
        if not is_valid:
            logger.warning(f"Input validation found {len(issues)} issues:")
            for issue in issues[:5]:  # 只显示前5个
                logger.warning(f"  - {issue}")
            if len(issues) > 5:
                logger.warning(f"  ... and {len(issues)-5} more issues")

    # ========== 步骤4: 太阳位置（可选）==========
    needs_sun_position = (
        "solar_zenith" not in df.columns or "solar_azimuth" not in df.columns
    )

    if recalculate_sun_position or needs_sun_position:
        logger.info("Calculating solar position...")

        # 检查必需列
        try:
            check_required_columns(df, ["timestamp", "lat", "lon"])
        except PVDataError:
            logger.error(
                "Solar position calculation requires 'timestamp', 'lat', 'lon' columns"
            )
            raise

        # 导入solar.position模块
        try:
            from ..solar.position import calculate_sun_position

            df = calculate_sun_position(
                df,
                time_col="timestamp",
                lat_col="lat",
                lon_col="lon",
                altitude_col=kwargs.get("altitude_col", "altitude_m"),
                method=kwargs.get("sun_position_method", "nrel_numpy"),
                inplace=True,
            )
            logger.info("Solar position calculated successfully")

        except ImportError:
            logger.error("solar.position module not available")
            raise PVDataError(
                "Solar position calculation requires pvdata.solar.position module. "
                "Please ensure solar_zenith and solar_azimuth columns exist in input data."
            )
    else:
        logger.debug("Using existing solar position columns")

    # ========== 步骤5: POA辐照度 ==========
    needs_poa = any(
        col in output_columns
        for col in [
            "poa_global",
            "poa_direct",
            "poa_sky_diffuse",
            "poa_ground_diffuse",
            "aoi",
        ]
    )

    if needs_poa or "poa_global" not in df.columns:
        logger.info("Calculating POA irradiance...")
        df = calculate_poa_irradiance(
            df,
            surface_tilt=surface_tilt,
            surface_azimuth=surface_azimuth,
            albedo=kwargs.get("albedo", 0.2),
            solar_zenith_col=kwargs.get("solar_zenith_col", "solar_zenith"),
            solar_azimuth_col=kwargs.get("solar_azimuth_col", "solar_azimuth"),
            model=kwargs.get("diffuse_model", "isotropic"),
            inplace=True,
        )
        logger.info(
            f"POA calculated: mean={df['poa_global'].mean():.1f} W/m², "
            f"max={df['poa_global'].max():.1f} W/m²"
        )
    else:
        logger.debug("Skipping POA calculation (column already exists)")

    # ========== 步骤6: 电池温度 ==========
    needs_temp = any(
        col in output_columns for col in ["cell_temperature", "temp_cell_steady"]
    )

    if needs_temp or "cell_temperature" not in df.columns:
        logger.info("Calculating cell temperature...")
        df = calculate_cell_temperature(
            df,
            module=module_config,
            temp_model=temp_model,
            apply_thermal_inertia=apply_thermal_inertia,
            poa_col=kwargs.get("poa_col", "poa_global"),
            temp_air_col=kwargs.get("temp_air_col", "Temperature"),
            wind_speed_col=kwargs.get("wind_speed_col", "Wind Speed"),
            inplace=True,
        )
        logger.info(
            f"Cell temp calculated: mean={df['cell_temperature'].mean():.1f}°C, "
            f"max={df['cell_temperature'].max():.1f}°C"
        )
    else:
        logger.debug("Skipping temperature calculation (column already exists)")

    # ========== 步骤7: DC功率 ==========
    needs_power = any(
        col in output_columns
        for col in ["i_sc", "v_oc", "i_mp", "v_mp", "dc_power"]
    )

    if needs_power:
        logger.info("Calculating DC power...")
        power_outputs = [
            col
            for col in output_columns
            if col in ["i_sc", "v_oc", "i_mp", "v_mp", "dc_power"]
        ]

        df = calculate_dc_power(
            df,
            module=module_config,
            effective_irradiance_col=kwargs.get("effective_irradiance_col", "poa_global"),
            cell_temp_col=kwargs.get("cell_temp_col", "cell_temperature"),
            outputs=power_outputs,
            inplace=True,
        )
        logger.info(
            f"DC power calculated: mean={df['dc_power'].mean():.1f}W, "
            f"max={df['dc_power'].max():.1f}W"
        )


    # ========== 步骤8: AC功率 (新增) ==========
    if "ac_power" in output_columns:
        logger.info("Calculating AC power...")
        # 默认参数: ILR=1.2, Eff=96%
        df = calculate_ac_power(
            df,
            module=module_config,
            dc_power_col="dc_power",
            nominal_efficiency=0.96,
            dc_ac_ratio=1.2,
            inplace=True,
        )

    # ========== 步骤9: 转换效率 ==========
    if "efficiency" in output_columns:
        logger.info("Calculating efficiency...")
        df["efficiency"] = calculate_efficiency(
            dc_power=df["dc_power"],
            poa_global=df["poa_global"],
            module_area=module_config.area,
        )

    # ========== 步骤9: 物理约束修正 ==========
    df = clip_physical_values(df, inplace=True)

    # ========== 步骤10: 清理不需要的中间列（可选）==========
    # 如果用户没有明确要求，可以删除某些中间变量
    # 但为了完整性，这里保留所有计算的列

    logger.info(
        f"PV potential calculation complete. "
        f"Added {len(output_columns)} columns: {output_columns}"
    )

    return df
