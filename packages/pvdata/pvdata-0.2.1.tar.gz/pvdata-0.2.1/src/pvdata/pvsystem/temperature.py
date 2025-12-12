"""
电池温度计算

稳态模型（SAPM/PVsyst）+ 可选热惯性平滑（Prilliman）
"""

import pandas as pd
import numpy as np
import pvlib
from typing import Optional, Dict, Union

from ..utils.logger import get_logger
from ..utils.decorators import log_execution
from ..utils.exceptions import PVDataError

from .module_config import ModuleConfig
from .utils import check_required_columns

logger = get_logger(__name__)


@log_execution(level="debug")
def calculate_cell_temperature(
    df: pd.DataFrame,
    module: ModuleConfig,
    temp_model: str = "sapm",
    apply_thermal_inertia: bool = True,
    poa_col: str = "poa_global",
    temp_air_col: str = "Temperature",
    wind_speed_col: str = "Wind Speed",
    inplace: bool = False,
) -> pd.DataFrame:
    """
    计算电池温度

    使用稳态模型（SAPM或PVsyst）+ 可选Prilliman热惯性平滑

    Parameters
    ----------
    df : pd.DataFrame
        输入数据，必须包含:
        - poa_global: POA辐照度 [W/m²]（或通过poa_col指定）
        - Temperature: 环境温度 [°C]（或通过temp_air_col指定）
        - Wind Speed: 风速 [m/s]（或通过wind_speed_col指定）
        - timestamp: 时间戳（如果apply_thermal_inertia=True）

    module : ModuleConfig
        组件配置对象，包含SAPM温度参数和unit_mass

    temp_model : str, default 'sapm'
        温度模型选择
        - 'sapm': Sandia Array Performance Model（稳态，快速）
        - 'pvsyst': PVsyst温度模型

    apply_thermal_inertia : bool, default True
        是否应用Prilliman热惯性模型（20分钟滑动窗口平滑）
        - True: 考虑组件热质量，温度变化更平滑（推荐）
        - False: 仅使用稳态温度

    poa_col : str, default 'poa_global'
        POA辐照度列名

    temp_air_col : str, default 'Temperature'
        环境温度列名

    wind_speed_col : str, default 'Wind Speed'
        风速列名

    inplace : bool, default False
        是否原地修改DataFrame

    Returns
    -------
    pd.DataFrame
        原数据 + 新增列:
        - temp_cell_steady: 稳态电池温度 [°C]
        - cell_temperature: 平滑电池温度 [°C]（如果apply_thermal_inertia=True）

    Raises
    ------
    PVDataError
        如果缺少必需列或参数无效

    Examples
    --------
    >>> import pvdata as pv
    >>> from pvdata.pvsystem import ModuleConfig
    >>> module = ModuleConfig.from_cec_database('Canadian_Solar_Inc__CS5A_150M')
    >>> df_temp = pv.calculate_cell_temperature(
    ...     df,
    ...     module=module,
    ...     temp_model='sapm',
    ...     apply_thermal_inertia=True
    ... )
    >>> print(df_temp[['Temperature', 'temp_cell_steady', 'cell_temperature']].head())

    Notes
    -----
    - SAPM模型计算快速，适用于大多数情况
    - Prilliman热惯性模型需要时间序列数据（DatetimeIndex）
    - 20分钟滑动窗口需要至少3个数据点（10分钟分辨率）
    - 夜间（POA≈0）温度仍会计算，反映组件的热惯性
    """
    if not inplace:
        df = df.copy()

    # 检查必需列
    required_cols = [poa_col, temp_air_col, wind_speed_col]
    check_required_columns(df, required_cols)

    # 如果需要热惯性，检查timestamp列
    if apply_thermal_inertia and "timestamp" not in df.columns:
        logger.warning(
            "timestamp column not found, thermal inertia calculation requires "
            "DatetimeIndex. Will attempt to use existing index."
        )

    # 确保timestamp是索引（Prilliman需要）
    original_index = df.index
    needs_index_reset = False

    if apply_thermal_inertia:
        if "timestamp" in df.columns and not isinstance(df.index, pd.DatetimeIndex):
            df = df.set_index("timestamp")
            needs_index_reset = True
            logger.debug("Set timestamp as index for thermal inertia calculation")
        elif not isinstance(df.index, pd.DatetimeIndex):
            raise PVDataError(
                "Thermal inertia calculation requires DatetimeIndex. "
                "Please provide 'timestamp' column or set index to datetime."
            )

    # 步骤1: 计算稳态温度
    logger.debug(f"Calculating steady-state temperature using {temp_model} model")

    if temp_model == "sapm":
        temp_steady = pvlib.temperature.sapm_cell(
            poa_global=df[poa_col],
            temp_air=df[temp_air_col],
            wind_speed=df[wind_speed_col],
            a=module.sapm_temp_params["a"],
            b=module.sapm_temp_params["b"],
            deltaT=module.sapm_temp_params["deltaT"],
        )

    elif temp_model == "pvsyst":
        # 检查是否有PVsyst参数
        if "u_c" in module.sapm_temp_params and "u_v" in module.sapm_temp_params:
            temp_steady = pvlib.temperature.pvsyst_cell(
                poa_global=df[poa_col],
                temp_air=df[temp_air_col],
                wind_speed=df[wind_speed_col],
                u_c=module.sapm_temp_params["u_c"],
                u_v=module.sapm_temp_params["u_v"],
            )
        else:
            logger.warning(
                "PVsyst params (u_c, u_v) not available in module config, "
                "falling back to SAPM model"
            )
            temp_steady = pvlib.temperature.sapm_cell(
                poa_global=df[poa_col],
                temp_air=df[temp_air_col],
                wind_speed=df[wind_speed_col],
                a=module.sapm_temp_params["a"],
                b=module.sapm_temp_params["b"],
                deltaT=module.sapm_temp_params["deltaT"],
            )

    else:
        raise PVDataError(
            f"Unknown temp_model: '{temp_model}'. Valid options: 'sapm', 'pvsyst'"
        )

    df["temp_cell_steady"] = temp_steady

    # 步骤2: 应用热惯性平滑（如果需要）
    if apply_thermal_inertia:
        logger.debug(
            f"Applying Prilliman thermal inertia (unit_mass={module.unit_mass:.1f} kg/m²)"
        )

        try:
            # Prilliman要求Series with DatetimeIndex
            temp_smoothed = pvlib.temperature.prilliman(
                temp_cell=temp_steady,  # 必须是Series with DatetimeIndex
                wind_speed=df[wind_speed_col],
                unit_mass=module.unit_mass,
                coefficients=None,  # 使用pvlib默认系数
            )
            df["cell_temperature"] = temp_smoothed

        except Exception as e:
            logger.error(
                f"Prilliman thermal inertia calculation failed: {e}. "
                f"Falling back to steady-state temperature."
            )
            df["cell_temperature"] = temp_steady

    else:
        # 不应用热惯性，直接使用稳态温度
        df["cell_temperature"] = temp_steady
        logger.debug("Thermal inertia not applied, using steady-state temperature")

    # 恢复原索引
    if needs_index_reset:
        df = df.reset_index(drop=False)
        df.index = original_index
        logger.debug("Reset index to original")

    logger.debug(
        f"Cell temperature calculated: "
        f"mean steady={df['temp_cell_steady'].mean():.1f}°C, "
        f"mean smoothed={df['cell_temperature'].mean():.1f}°C"
    )

    return df


def calculate_sapm_cell_temperature(
    poa_global: Union[float, pd.Series],
    temp_air: Union[float, pd.Series],
    wind_speed: Union[float, pd.Series],
    a: float,
    b: float,
    deltaT: float,
) -> Union[float, pd.Series]:
    """
    使用SAPM模型计算稳态电池温度

    T_cell = T_air + (POA / 1000) × exp(a + b × WS) × ΔT

    Parameters
    ----------
    poa_global : float or pd.Series
        POA辐照度 [W/m²]
    temp_air : float or pd.Series
        环境温度 [°C]
    wind_speed : float or pd.Series
        风速 [m/s]
    a : float
        SAPM参数a（基础散热系数）
    b : float
        SAPM参数b（风速敏感系数）
    deltaT : float
        SAPM参数deltaT（温差修正）

    Returns
    -------
    float or pd.Series
        电池温度 [°C]

    Examples
    --------
    >>> from pvdata.pvsystem.constants import SAPM_STANDARD_PARAMS
    >>> params = SAPM_STANDARD_PARAMS['open_rack_glass_polymer']
    >>> T_cell = calculate_sapm_cell_temperature(
    ...     poa_global=800,
    ...     temp_air=20,
    ...     wind_speed=1.0,
    ...     **params
    ... )
    >>> print(f"Cell temperature: {T_cell:.1f}°C")
    """
    return pvlib.temperature.sapm_cell(
        poa_global=poa_global,
        temp_air=temp_air,
        wind_speed=wind_speed,
        a=a,
        b=b,
        deltaT=deltaT,
    )


def calculate_pvsyst_cell_temperature(
    poa_global: Union[float, pd.Series],
    temp_air: Union[float, pd.Series],
    wind_speed: Union[float, pd.Series],
    u_c: float,
    u_v: float,
) -> Union[float, pd.Series]:
    """
    使用PVsyst模型计算稳态电池温度

    Parameters
    ----------
    poa_global : float or pd.Series
        POA辐照度 [W/m²]
    temp_air : float or pd.Series
        环境温度 [°C]
    wind_speed : float or pd.Series
        风速 [m/s]
    u_c : float
        PVsyst常数传热系数 [W/(m²·K)]
    u_v : float
        PVsyst风速传热系数 [W/(m³·K)]

    Returns
    -------
    float or pd.Series
        电池温度 [°C]

    Examples
    --------
    >>> T_cell = calculate_pvsyst_cell_temperature(
    ...     poa_global=800,
    ...     temp_air=20,
    ...     wind_speed=1.0,
    ...     u_c=20.0,
    ...     u_v=0.0
    ... )
    """
    return pvlib.temperature.pvsyst_cell(
        poa_global=poa_global, temp_air=temp_air, wind_speed=wind_speed, u_c=u_c, u_v=u_v
    )


def apply_prilliman_thermal_inertia(
    temp_cell_steady: pd.Series,
    wind_speed: pd.Series,
    unit_mass: float,
    coefficients: Optional[list] = None,
) -> pd.Series:
    """
    应用Prilliman热惯性模型平滑温度

    使用20分钟滑动窗口考虑组件热质量对温度变化的缓冲效应

    Parameters
    ----------
    temp_cell_steady : pd.Series
        稳态电池温度 [°C]，必须有DatetimeIndex
    wind_speed : pd.Series
        风速 [m/s]
    unit_mass : float
        单位面积质量 [kg/m²]
    coefficients : list of 4 floats, optional
        Prilliman系数 [a0, a1, a2, a3]
        None则使用pvlib默认值

    Returns
    -------
    pd.Series
        平滑后的电池温度 [°C]

    Raises
    ------
    PVDataError
        如果temp_cell_steady没有DatetimeIndex

    Examples
    --------
    >>> temp_smoothed = apply_prilliman_thermal_inertia(
    ...     temp_cell_steady=df['temp_cell_steady'],
    ...     wind_speed=df['Wind Speed'],
    ...     unit_mass=11.0
    ... )

    Notes
    -----
    - 需要至少20分钟的数据（对于10分钟分辨率，至少3个点）
    - 窗口大小自动根据时间分辨率调整
    - 适用于5-60分钟分辨率数据
    """
    if not isinstance(temp_cell_steady.index, pd.DatetimeIndex):
        raise PVDataError(
            "Prilliman thermal inertia requires Series with DatetimeIndex. "
            "Received index type: " + str(type(temp_cell_steady.index))
        )

    try:
        temp_smoothed = pvlib.temperature.prilliman(
            temp_cell=temp_cell_steady,
            wind_speed=wind_speed,
            unit_mass=unit_mass,
            coefficients=coefficients,
        )
        return temp_smoothed

    except Exception as e:
        logger.error(f"Prilliman calculation failed: {e}")
        raise PVDataError(f"Failed to apply thermal inertia: {e}")


def calculate_noct_temperature(
    poa_global: float = 800.0,
    temp_air: float = 20.0,
    wind_speed: float = 1.0,
    a: float = -3.56,
    b: float = -0.075,
    deltaT: float = 3.0,
) -> float:
    """
    计算NOCT条件下的电池温度

    NOCT (Nominal Operating Cell Temperature): 标称工作电池温度
    标准条件: 800 W/m², 20°C, 1 m/s风速

    Parameters
    ----------
    poa_global : float, default 800.0
        POA辐照度 [W/m²]
    temp_air : float, default 20.0
        环境温度 [°C]
    wind_speed : float, default 1.0
        风速 [m/s]
    a : float, default -3.56
        SAPM参数a
    b : float, default -0.075
        SAPM参数b
    deltaT : float, default 3.0
        SAPM参数deltaT

    Returns
    -------
    float
        NOCT条件下的电池温度 [°C]

    Examples
    --------
    >>> from pvdata.pvsystem.constants import SAPM_STANDARD_PARAMS
    >>> params = SAPM_STANDARD_PARAMS['open_rack_glass_polymer']
    >>> T_noct = calculate_noct_temperature(**params)
    >>> print(f"NOCT temperature: {T_noct:.1f}°C")  # ~48°C

    Notes
    -----
    用于验证SAPM参数是否与CEC数据库的T_NOCT匹配
    """
    return pvlib.temperature.sapm_cell(
        poa_global=poa_global,
        temp_air=temp_air,
        wind_speed=wind_speed,
        a=a,
        b=b,
        deltaT=deltaT,
    )
