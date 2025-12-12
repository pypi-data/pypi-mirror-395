"""
DC功率和I-V特性计算

使用CEC单二极管模型
"""

import pandas as pd
import numpy as np
import pvlib
from typing import List, Union, Optional

from ..utils.logger import get_logger
from ..utils.decorators import log_execution
from ..utils.exceptions import PVDataError

from .module_config import ModuleConfig
from .utils import check_required_columns

logger = get_logger(__name__)


@log_execution(level="debug")
def calculate_dc_power(
    df: pd.DataFrame,
    module: ModuleConfig,
    effective_irradiance_col: str = "poa_global",
    cell_temp_col: str = "cell_temperature",
    outputs: List[str] = ["dc_power"],
    inplace: bool = False,
) -> pd.DataFrame:
    """
    使用CEC单二极管模型计算DC功率和I-V特性

    Parameters
    ----------
    df : pd.DataFrame
        输入数据，必须包含:
        - poa_global: POA辐照度 [W/m²]（或通过effective_irradiance_col指定）
        - cell_temperature: 电池温度 [°C]（或通过cell_temp_col指定）

    module : ModuleConfig
        组件配置对象，包含完整CEC参数

    effective_irradiance_col : str, default 'poa_global'
        有效辐照度列名

    cell_temp_col : str, default 'cell_temperature'
        电池温度列名

    outputs : list of str, default ['dc_power']
        指定输出列，可选:
        - 'i_sc': 短路电流 [A]
        - 'v_oc': 开路电压 [V]
        - 'i_mp': 最大功率点电流 [A]
        - 'v_mp': 最大功率点电压 [V]
        - 'dc_power': 直流功率 [W] (i_mp × v_mp)

    inplace : bool, default False
        是否原地修改DataFrame

    Returns
    -------
    pd.DataFrame
        原数据 + 指定的输出列

    Raises
    ------
    PVDataError
        如果缺少必需列或计算失败

    Examples
    --------
    >>> import pvdata as pv
    >>> from pvdata.pvsystem import ModuleConfig
    >>> module = ModuleConfig.from_cec_database('Canadian_Solar_Inc__CS5A_150M')
    >>> df_power = pv.calculate_dc_power(
    ...     df,
    ...     module=module,
    ...     outputs=['i_mp', 'v_mp', 'dc_power']
    ... )
    >>> print(df_power[['poa_global', 'cell_temperature', 'dc_power']].head())

    Notes
    -----
    - 使用pvlib的calcparams_cec计算SDM参数
    - 使用pvlib的singlediode求解I-V特性
    - Lambert W方法求解单二极管方程（快速准确）
    - 低辐照度条件下功率可能为NaN或负值（自动clip到0）
    """
    if not inplace:
        df = df.copy()

    # 检查必需列
    required_cols = [effective_irradiance_col, cell_temp_col]
    check_required_columns(df, required_cols)

    # 验证输出列
    valid_outputs = ["i_sc", "v_oc", "i_mp", "v_mp", "dc_power"]
    invalid = [col for col in outputs if col not in valid_outputs]
    if invalid:
        raise PVDataError(
            f"Invalid output columns: {invalid}. Valid options: {valid_outputs}"
        )

    logger.debug(f"Calculating DC power using CEC single-diode model")

    # 步骤1: 计算SDM参数
    cec = module.cec_params

    try:
        sdm_params = pvlib.pvsystem.calcparams_cec(
            effective_irradiance=df[effective_irradiance_col],
            temp_cell=df[cell_temp_col],
            alpha_sc=cec["alpha_sc"],
            a_ref=cec["a_ref"],
            I_L_ref=cec["I_L_ref"],
            I_o_ref=cec["I_o_ref"],
            R_sh_ref=cec["R_sh_ref"],
            R_s=cec["R_s"],
            Adjust=cec["Adjust"],
        )

    except Exception as e:
        raise PVDataError(f"Failed to calculate SDM parameters: {e}")

    # 步骤2: 求解单二极管方程
    try:
        iv_curve = pvlib.pvsystem.singlediode(
            photocurrent=sdm_params[0],  # I_L
            saturation_current=sdm_params[1],  # I_0
            resistance_series=sdm_params[2],  # R_s
            resistance_shunt=sdm_params[3],  # R_sh
            nNsVth=sdm_params[4],  # nNsVth
            method="lambertw",  # Lambert W方法（快速准确）
        )

    except Exception as e:
        raise PVDataError(f"Failed to solve single-diode equation: {e}")

    # 步骤3: 提取输出并应用物理约束
    if "i_sc" in outputs:
        df["i_sc"] = iv_curve["i_sc"].clip(lower=0)

    if "v_oc" in outputs:
        df["v_oc"] = iv_curve["v_oc"].clip(lower=0)

    if "i_mp" in outputs:
        df["i_mp"] = iv_curve["i_mp"].clip(lower=0)

    if "v_mp" in outputs:
        df["v_mp"] = iv_curve["v_mp"].clip(lower=0)

    if "dc_power" in outputs:
        df["dc_power"] = iv_curve["p_mp"].clip(lower=0)

    logger.debug(
        f"DC power calculated: mean={df['dc_power'].mean():.1f}W, "
        f"max={df['dc_power'].max():.1f}W"
    )

    return df


@log_execution(level="debug")
def calculate_ac_power(
    df: pd.DataFrame,
    module: ModuleConfig,
    dc_power_col: str = "dc_power",
    nominal_efficiency: float = 0.96,
    dc_ac_ratio: float = 1.2,
    inplace: bool = False,
) -> pd.DataFrame:
    """
    计算交流功率 (AC Power)

    使用 pvlib.inverter.pvwatts 模型模拟逆变器行为。
    包含效率损失和削峰 (Clipping)。

    Parameters
    ----------
    df : pd.DataFrame
        输入数据，必须包含 dc_power_col
    module : ModuleConfig
        组件配置（用于获取额定功率）
    dc_power_col : str, default 'dc_power'
        直流功率列名 [W]
    nominal_efficiency : float, default 0.96
        逆变器标称效率 (96%)
    dc_ac_ratio : float, default 1.2
        容配比 (DC/AC Ratio)，用于确定逆变器额定功率
        Inverter Rated Power = Module Rated Power / dc_ac_ratio
    inplace : bool, default False
        是否原地修改

    Returns
    -------
    pd.DataFrame
        新增 'ac_power' 列 [W]
    """
    if not inplace:
        df = df.copy()

    check_required_columns(df, [dc_power_col])

    # 1. 确定逆变器参数
    # 假设每个组件配备一个微逆，或者按比例分摊的大逆变器
    pdc0 = module.rated_power  # 组件额定直流功率
    pac0 = pdc0 / dc_ac_ratio  # 逆变器额定交流功率 (削峰阈值)

    logger.debug(
        f"Calculating AC power: Module DC={pdc0:.1f}W, "
        f"Inverter AC={pac0:.1f}W (Ratio={dc_ac_ratio}), Eff={nominal_efficiency:.1%}"
    )

    # 2. 计算 AC 功率
    try:
        # pvlib.inverter.pvwatts 自动处理效率曲线和削峰
        # pdc: 直流输入功率
        # pdc0: 逆变器直流额定功率 (用于归一化效率曲线)
        # eta_inv_nom: 标称效率
        # eta_inv_ref: 参考效率 (通常略高于标称，默认 0.9637)
        ac_power = pvlib.inverter.pvwatts(
            pdc=df[dc_power_col],
            pdc0=pdc0,
            eta_inv_nom=nominal_efficiency,
            eta_inv_ref=0.9637,
        )

        # 额外的削峰检查 (pvwatts 理论上会处理，但为了保险)
        ac_power = ac_power.clip(upper=pac0)

        # 确保非负
        df["ac_power"] = ac_power.clip(lower=0.0)

    except Exception as e:
        logger.error(f"AC power calculation failed: {e}")
        raise PVDataError(f"Failed to calculate AC power: {e}")

    logger.debug(
        f"AC power calculated: mean={df['ac_power'].mean():.1f}W, "
        f"max={df['ac_power'].max():.1f}W"
    )

    return df


def calculate_efficiency(
    dc_power: Union[float, pd.Series],
    poa_global: Union[float, pd.Series],
    module_area: float,
) -> Union[float, pd.Series]:
    """
    计算转换效率

    efficiency = dc_power / (poa_global × module_area)

    Parameters
    ----------
    dc_power : float or pd.Series
        直流功率 [W]
    poa_global : float or pd.Series
        POA辐照度 [W/m²]
    module_area : float
        组件面积 [m²]

    Returns
    -------
    float or pd.Series
        转换效率 [0-1]

    Examples
    --------
    >>> eff = calculate_efficiency(
    ...     dc_power=250,
    ...     poa_global=1000,
    ...     module_area=1.6
    ... )
    >>> print(f"Efficiency: {eff:.2%}")  # 15.62%

    Notes
    -----
    - 效率自动clip到[0, 0.30]范围
    - 低辐照度时（POA<10 W/m²）返回0避免除零
    """
    # 避免除零
    denominator = poa_global * module_area
    epsilon = 1e-6

    if isinstance(poa_global, pd.Series):
        # Series操作
        efficiency = dc_power / (denominator + epsilon)
        efficiency = efficiency.clip(0, 0.30)
        # 低辐照度时设为0
        efficiency[poa_global < 10] = 0
    else:
        # 标量操作
        if poa_global < 10:
            efficiency = 0.0
        else:
            efficiency = dc_power / (denominator + epsilon)
            efficiency = np.clip(efficiency, 0, 0.30)

    return efficiency


def calculate_iv_curve_points(
    module: ModuleConfig,
    poa_global: float,
    cell_temperature: float,
    num_points: int = 100,
) -> pd.DataFrame:
    """
    计算完整I-V曲线

    Parameters
    ----------
    module : ModuleConfig
        组件配置对象
    poa_global : float
        POA辐照度 [W/m²]
    cell_temperature : float
        电池温度 [°C]
    num_points : int, default 100
        曲线点数

    Returns
    -------
    pd.DataFrame
        包含 'voltage', 'current', 'power' 列

    Examples
    --------
    >>> from pvdata.pvsystem import ModuleConfig
    >>> module = ModuleConfig.from_cec_database('Canadian_Solar_Inc__CS5A_150M')
    >>> iv_curve = calculate_iv_curve_points(
    ...     module=module,
    ...     poa_global=1000,
    ...     cell_temperature=25
    ... )
    >>> # 绘制I-V曲线
    >>> import matplotlib.pyplot as plt
    >>> plt.plot(iv_curve['voltage'], iv_curve['current'])
    >>> plt.xlabel('Voltage [V]')
    >>> plt.ylabel('Current [A]')

    Notes
    -----
    - 电压范围从0到V_oc
    - 用于绘图或详细分析
    - 计算较慢，不适合大批量数据
    """
    logger.debug(
        f"Calculating I-V curve: POA={poa_global} W/m², T_cell={cell_temperature}°C"
    )

    cec = module.cec_params

    # 计算SDM参数
    sdm_params = pvlib.pvsystem.calcparams_cec(
        effective_irradiance=poa_global,
        temp_cell=cell_temperature,
        alpha_sc=cec["alpha_sc"],
        a_ref=cec["a_ref"],
        I_L_ref=cec["I_L_ref"],
        I_o_ref=cec["I_o_ref"],
        R_sh_ref=cec["R_sh_ref"],
        R_s=cec["R_s"],
        Adjust=cec["Adjust"],
    )

    # 求解I-V曲线
    iv_curve = pvlib.pvsystem.singlediode(
        photocurrent=sdm_params[0],
        saturation_current=sdm_params[1],
        resistance_series=sdm_params[2],
        resistance_shunt=sdm_params[3],
        nNsVth=sdm_params[4],
        ivcurve_pnts=num_points,
        method="lambertw",
    )

    # 提取I-V曲线点
    result = pd.DataFrame(
        {
            "voltage": iv_curve["v"],
            "current": iv_curve["i"],
            "power": iv_curve["v"] * iv_curve["i"],
        }
    )

    return result


def calculate_max_power_point(
    module: ModuleConfig, poa_global: float, cell_temperature: float
) -> dict:
    """
    计算最大功率点

    Parameters
    ----------
    module : ModuleConfig
        组件配置对象
    poa_global : float
        POA辐照度 [W/m²]
    cell_temperature : float
        电池温度 [°C]

    Returns
    -------
    dict
        包含 'i_mp', 'v_mp', 'p_mp', 'i_sc', 'v_oc'

    Examples
    --------
    >>> from pvdata.pvsystem import ModuleConfig
    >>> module = ModuleConfig.from_cec_database('Canadian_Solar_Inc__CS5A_150M')
    >>> mpp = calculate_max_power_point(
    ...     module=module,
    ...     poa_global=1000,
    ...     cell_temperature=25
    ... )
    >>> print(f"Max Power: {mpp['p_mp']:.1f} W at {mpp['v_mp']:.1f} V, {mpp['i_mp']:.2f} A")
    """
    cec = module.cec_params

    # 计算SDM参数
    sdm_params = pvlib.pvsystem.calcparams_cec(
        effective_irradiance=poa_global,
        temp_cell=cell_temperature,
        alpha_sc=cec["alpha_sc"],
        a_ref=cec["a_ref"],
        I_L_ref=cec["I_L_ref"],
        I_o_ref=cec["I_o_ref"],
        R_sh_ref=cec["R_sh_ref"],
        R_s=cec["R_s"],
        Adjust=cec["Adjust"],
    )

    # 求解单二极管方程
    iv_curve = pvlib.pvsystem.singlediode(
        photocurrent=sdm_params[0],
        saturation_current=sdm_params[1],
        resistance_series=sdm_params[2],
        resistance_shunt=sdm_params[3],
        nNsVth=sdm_params[4],
        method="lambertw",
    )

    return {
        "i_mp": iv_curve["i_mp"],
        "v_mp": iv_curve["v_mp"],
        "p_mp": iv_curve["p_mp"],
        "i_sc": iv_curve["i_sc"],
        "v_oc": iv_curve["v_oc"],
    }


def scale_voltage_current_to_modules_per_string(
    voltage: Union[float, pd.Series],
    current: Union[float, pd.Series],
    modules_per_string: int = 1,
) -> tuple:
    """
    将单个组件的电压和电流缩放到串联组件

    Parameters
    ----------
    voltage : float or pd.Series
        单个组件电压 [V]
    current : float or pd.Series
        单个组件电流 [A]
    modules_per_string : int, default 1
        每串组件数量

    Returns
    -------
    tuple of (voltage, current)
        缩放后的电压和电流

    Examples
    --------
    >>> # 10个组件串联
    >>> v_string, i_string = scale_voltage_current_to_modules_per_string(
    ...     voltage=37.5,  # 单个组件MPP电压
    ...     current=8.0,   # 单个组件MPP电流
    ...     modules_per_string=10
    ... )
    >>> print(f"String: {v_string}V, {i_string}A")  # 375V, 8.0A

    Notes
    -----
    - 串联: 电压相加，电流不变
    - 并联: 电流相加，电压不变（不在此函数处理）
    """
    voltage_string = voltage * modules_per_string
    current_string = current  # 串联时电流不变

    return voltage_string, current_string
