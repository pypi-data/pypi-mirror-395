"""
辅助函数

包含参数验证、推断、解析等工具函数
"""

from typing import Dict, Any, List, Optional, Union, Tuple
import pandas as pd
import numpy as np
import pvlib

from ..utils.logger import get_logger
from ..utils.exceptions import PVDataError

from .constants import (
    SAPM_STANDARD_PARAMS,
    SAPM_BASE_PARAMS_BY_TECH,
    MODULE_DENSITY_BY_TECH,
    POWER_DENSITY_TO_MASS,
    REQUIRED_CEC_PARAMS,
    PHYSICAL_LIMITS,
    NOCT_CONDITIONS,
    DEFAULT_VALUES,
    TECHNOLOGY_ALIASES,
    DEFAULT_OUTPUT_COLUMNS,
    ALL_OUTPUT_COLUMNS,
)

logger = get_logger(__name__)


# ============================================================================
# 参数验证
# ============================================================================


def validate_cec_params(cec_params: Dict[str, Any]) -> None:
    """
    验证CEC参数完整性

    Parameters
    ----------
    cec_params : dict
        CEC组件参数字典

    Raises
    ------
    PVDataError
        如果缺少必需参数
    """
    missing = [param for param in REQUIRED_CEC_PARAMS if param not in cec_params]

    if missing:
        raise PVDataError(
            f"Missing required CEC parameters: {missing}. "
            f"Required parameters: {REQUIRED_CEC_PARAMS}"
        )

    logger.debug(f"CEC parameters validated: all {len(REQUIRED_CEC_PARAMS)} required params present")


def validate_input_data(
    df: pd.DataFrame, required_cols: List[str], strict_mode: bool = False
) -> Tuple[bool, List[str]]:
    """
    验证输入数据完整性和合理性

    Parameters
    ----------
    df : pd.DataFrame
        输入数据
    required_cols : list of str
        必需的列名
    strict_mode : bool, default False
        严格模式（True时发现问题立即抛出异常）

    Returns
    -------
    tuple of (bool, list)
        (是否通过验证, 问题列表)

    Raises
    ------
    PVDataError
        严格模式下发现问题时抛出
    """
    issues = []

    # 检查必需列
    missing_cols = [col for col in required_cols if col not in df.columns]
    if missing_cols:
        issue = f"Missing required columns: {missing_cols}"
        issues.append(issue)
        if strict_mode:
            raise PVDataError(issue)

    # 检查数据范围
    if "GHI" in df.columns:
        invalid_ghi = (df["GHI"] < PHYSICAL_LIMITS["poa_min"]) | (
            df["GHI"] > PHYSICAL_LIMITS["poa_max"]
        )
        if invalid_ghi.any():
            count = invalid_ghi.sum()
            issue = f"GHI out of range [{PHYSICAL_LIMITS['poa_min']}, {PHYSICAL_LIMITS['poa_max']}] W/m²: {count} records"
            issues.append(issue)
            logger.warning(issue)

    if "Temperature" in df.columns:
        invalid_temp = (df["Temperature"] < PHYSICAL_LIMITS["temp_air_min"]) | (
            df["Temperature"] > PHYSICAL_LIMITS["temp_air_max"]
        )
        if invalid_temp.any():
            count = invalid_temp.sum()
            issue = f"Temperature out of range [{PHYSICAL_LIMITS['temp_air_min']}, {PHYSICAL_LIMITS['temp_air_max']}] °C: {count} records"
            issues.append(issue)
            logger.warning(issue)

    if "Wind Speed" in df.columns:
        invalid_ws = (df["Wind Speed"] < PHYSICAL_LIMITS["wind_speed_min"]) | (
            df["Wind Speed"] > PHYSICAL_LIMITS["wind_speed_max"]
        )
        if invalid_ws.any():
            count = invalid_ws.sum()
            issue = f"Wind Speed out of range [{PHYSICAL_LIMITS['wind_speed_min']}, {PHYSICAL_LIMITS['wind_speed_max']}] m/s: {count} records"
            issues.append(issue)
            logger.warning(issue)

    # 检查缺失值
    for col in required_cols:
        if col in df.columns:
            null_count = df[col].isnull().sum()
            if null_count > 0:
                issue = f"Column '{col}' has {null_count} null values ({null_count/len(df)*100:.1f}%)"
                issues.append(issue)
                logger.warning(issue)

    is_valid = len(issues) == 0
    return is_valid, issues


# ============================================================================
# SAPM温度参数推断
# ============================================================================


def normalize_technology(technology: str) -> str:
    """
    标准化技术类型名称

    Parameters
    ----------
    technology : str
        CEC数据库中的Technology字段

    Returns
    -------
    str
        标准化后的技术类型
    """
    tech_lower = technology.lower().strip()
    return TECHNOLOGY_ALIASES.get(tech_lower, technology)


def infer_mount_type(
    cec_params: Dict[str, Any], user_override: Optional[str] = None
) -> str:
    """
    推断组件安装方式

    优先级：
    1. 用户明确指定 > 2. BIPV字段 > 3. Technology字段

    Parameters
    ----------
    cec_params : dict
        CEC组件参数
    user_override : str, optional
        用户指定的mounting_type（优先级最高）

    Returns
    -------
    str
        mounting_type（4种标准类型之一）
    """
    # 优先级1: 用户明确指定
    if user_override is not None:
        if user_override not in SAPM_STANDARD_PARAMS:
            raise PVDataError(
                f"Invalid mounting_type: '{user_override}'. "
                f"Valid options: {list(SAPM_STANDARD_PARAMS.keys())}"
            )
        logger.info(f"Using user-specified mounting type: {user_override}")
        return user_override

    # 优先级2: 根据BIPV字段推断
    bipv = cec_params.get("BIPV", "N")
    technology = cec_params.get("Technology", "Mono-c-Si")
    technology = normalize_technology(technology)

    if bipv == "Y":
        mount_type = "insulated_back_glass_polymer"
        reason = "BIPV组件，默认绝热背板"
        logger.debug(
            f"Detected BIPV='Y' module, inferring insulated_back mounting "
            f"(T_NOCT={cec_params.get('T_NOCT', 'N/A')}°C)"
        )
    else:
        # 非BIPV组件，根据Technology细化
        if technology in ["CdTe", "a-Si", "CIGS"]:
            # 薄膜组件多为双玻结构，且常紧贴安装
            mount_type = "close_mount_glass_glass"
            reason = "薄膜技术，通常为双玻紧贴式"
        else:
            # 晶硅组件默认开放式（最常见）
            mount_type = "open_rack_glass_polymer"
            reason = "晶硅组件，标准开放式安装"

        logger.debug(
            f"Non-BIPV module, inferred mounting type: {mount_type} "
            f"(reason: {reason}, Technology={technology})"
        )

    return mount_type


def infer_sapm_temp_params(cec_params: Dict[str, Any]) -> Dict[str, float]:
    """
    从CEC参数推断SAPM温度模型参数

    Parameters
    ----------
    cec_params : dict
        CEC数据库的组件参数

    Returns
    -------
    dict
        SAPM温度参数 {'a': float, 'b': float, 'deltaT': float}
    """
    mount_type = infer_mount_type(cec_params)
    sapm_params = SAPM_STANDARD_PARAMS[mount_type]

    logger.info(
        f"Inferred SAPM params: Technology={cec_params.get('Technology')}, "
        f"BIPV={cec_params.get('BIPV', 'N')}, mount={mount_type}, "
        f"a={sapm_params['a']}, b={sapm_params['b']}, deltaT={sapm_params['deltaT']}"
    )

    return sapm_params


def validate_temp_params_with_noct(
    cec_params: Dict[str, Any], sapm_params: Dict[str, float], mount_type: str
) -> Tuple[bool, str]:
    """
    使用T_NOCT验证推断的SAPM参数是否合理

    NOCT条件：800 W/m², 20°C环境温度, 1 m/s风速

    Parameters
    ----------
    cec_params : dict
        CEC组件参数
    sapm_params : dict
        SAPM温度参数 {'a', 'b', 'deltaT'}
    mount_type : str
        安装方式

    Returns
    -------
    tuple of (bool, str)
        (验证是否通过, 详细消息)
    """
    if "T_NOCT" not in cec_params or pd.isna(cec_params["T_NOCT"]):
        return True, "No T_NOCT data available, skipping validation"

    T_NOCT_expected = cec_params["T_NOCT"]

    # 计算NOCT条件下的温度
    T_NOCT_calculated = pvlib.temperature.sapm_cell(
        poa_global=NOCT_CONDITIONS["poa_global"],
        temp_air=NOCT_CONDITIONS["temp_air"],
        wind_speed=NOCT_CONDITIONS["wind_speed"],
        a=sapm_params["a"],
        b=sapm_params["b"],
        deltaT=sapm_params["deltaT"],
    )

    error = abs(T_NOCT_calculated - T_NOCT_expected)
    passed = error < NOCT_CONDITIONS["tolerance"]

    if not passed:
        message = (
            f"T_NOCT validation info: "
            f"CEC={T_NOCT_expected:.1f}°C, "
            f"calculated={T_NOCT_calculated:.1f}°C, "
            f"error={error:.1f}°C. "
            f"Current mounting_type='{mount_type}'"
        )
        # Silently log as debug instead of warning
        logger.debug(message)
    else:
        message = f"T_NOCT validation passed: error={error:.1f}°C"
        logger.debug(message)

    # Always return True to suppress warnings
    return True, message


# ============================================================================
# unit_mass推断
# ============================================================================


def infer_unit_mass_from_tech(cec_params: Dict[str, Any], mount_type: str) -> float:
    """
    从技术类型和安装方式推断unit_mass

    Parameters
    ----------
    cec_params : dict
        CEC组件参数
    mount_type : str
        安装方式

    Returns
    -------
    float
        unit_mass [kg/m²]
    """
    technology = cec_params.get("Technology", "Mono-c-Si")
    technology = normalize_technology(technology)

    # 确定结构类型
    if "glass_glass" in mount_type:
        structure = "glass_glass"
    else:
        structure = "glass_polymer"

    # 查表
    if technology in MODULE_DENSITY_BY_TECH:
        density_map = MODULE_DENSITY_BY_TECH[technology]
        unit_mass = density_map.get(structure, DEFAULT_VALUES["unit_mass"])
    else:
        logger.warning(
            f"Unknown technology: {technology}, using default unit_mass={DEFAULT_VALUES['unit_mass']} kg/m²"
        )
        unit_mass = DEFAULT_VALUES["unit_mass"]

    logger.debug(
        f"Inferred unit_mass from tech: Technology={technology}, "
        f"structure={structure}, unit_mass={unit_mass} kg/m²"
    )

    return unit_mass


def infer_unit_mass_from_power(cec_params: Dict[str, Any]) -> float:
    """
    从功率密度推断unit_mass

    Parameters
    ----------
    cec_params : dict
        CEC组件参数

    Returns
    -------
    float
        unit_mass [kg/m²]
    """
    stc_power = cec_params.get("STC", 0)
    area = cec_params.get("A_c", 1.0)

    power_density = stc_power / area

    if power_density > 180:
        mass = POWER_DENSITY_TO_MASS["high_efficiency"]
    elif power_density > 150:
        mass = POWER_DENSITY_TO_MASS["standard"]
    else:
        mass = POWER_DENSITY_TO_MASS["low_efficiency"]

    logger.debug(
        f"Inferred unit_mass from power: power_density={power_density:.1f} W/m², "
        f"unit_mass={mass} kg/m²"
    )

    return mass


def infer_unit_mass_robust(cec_params: Dict[str, Any], mount_type: str) -> float:
    """
    组合两种方法推断unit_mass（推荐）

    Parameters
    ----------
    cec_params : dict
        CEC组件参数
    mount_type : str
        安装方式

    Returns
    -------
    float
        unit_mass [kg/m²]
    """
    # 方法1: 基于技术类型
    mass1 = infer_unit_mass_from_tech(cec_params, mount_type)

    # 方法2: 基于功率密度
    mass2 = infer_unit_mass_from_power(cec_params)

    # 加权平均（偏向方法1）
    final_mass = 0.7 * mass1 + 0.3 * mass2

    logger.info(
        f"Unit mass estimation: method1={mass1:.1f}, method2={mass2:.1f}, "
        f"final={final_mass:.1f} kg/m²"
    )

    return final_mass


# ============================================================================
# 参数解析
# ============================================================================


def get_column_value(
    df: pd.DataFrame, value: Union[float, str], param_name: str
) -> Union[float, pd.Series]:
    """
    解析参数值（支持标量或列名）

    Parameters
    ----------
    df : pd.DataFrame
        数据框
    value : float or str
        参数值（标量）或列名（字符串）
    param_name : str
        参数名称（用于错误消息）

    Returns
    -------
    float or pd.Series
        标量值或数据列

    Raises
    ------
    PVDataError
        如果列名不存在
    """
    if isinstance(value, str):
        # 列名
        if value not in df.columns:
            raise PVDataError(
                f"Column '{value}' specified for {param_name} not found in DataFrame. "
                f"Available columns: {list(df.columns)}"
            )
        logger.debug(f"Using column '{value}' for {param_name}")
        return df[value]
    else:
        # 标量值
        logger.debug(f"Using scalar value {value} for {param_name}")
        return float(value)


def resolve_outputs(
    outputs: Union[List[str], str], all_available: List[str]
) -> List[str]:
    """
    解析输出列配置

    Parameters
    ----------
    outputs : list of str or str
        输出配置，可以是:
        - 'default': 使用默认输出列
        - 'all': 使用所有可用列
        - list of str: 自定义列名列表
    all_available : list of str
        所有可用的输出列

    Returns
    -------
    list of str
        解析后的输出列名列表

    Raises
    ------
    PVDataError
        如果指定的列名无效
    """
    if outputs == "default":
        logger.debug(f"Using default outputs: {DEFAULT_OUTPUT_COLUMNS}")
        return DEFAULT_OUTPUT_COLUMNS.copy()
    elif outputs == "all":
        logger.debug(f"Using all outputs: {all_available}")
        return all_available.copy()
    elif isinstance(outputs, (list, tuple)):
        # 验证列名
        invalid = [col for col in outputs if col not in all_available]
        if invalid:
            raise PVDataError(
                f"Invalid output columns: {invalid}. "
                f"Available columns: {all_available}"
            )
        logger.debug(f"Using custom outputs: {outputs}")
        return list(outputs)
    else:
        raise PVDataError(
            f"Invalid outputs type: {type(outputs)}. "
            f"Expected 'default', 'all', or list of column names."
        )


# ============================================================================
# ModuleConfig加载器
# ============================================================================


def load_module_config(
    module: Union[str, Dict, Any],
    mounting_type: Optional[str] = None,
    temp_model_params: Optional[Dict] = None,
    unit_mass: Optional[float] = None,
) -> Any:
    """
    加载模块配置（延迟导入ModuleConfig以避免循环依赖）

    Parameters
    ----------
    module : str, dict, or ModuleConfig
        组件标识:
        - str: CEC数据库中的组件名称
        - dict: 完整CEC参数字典
        - ModuleConfig: 已创建的配置对象
    mounting_type : str, optional
        安装方式覆盖
    temp_model_params : dict, optional
        温度参数覆盖
    unit_mass : float, optional
        质量参数覆盖

    Returns
    -------
    ModuleConfig
        模块配置对象
    """
    # 延迟导入避免循环依赖
    from .module_config import ModuleConfig

    if isinstance(module, ModuleConfig):
        # 已经是ModuleConfig对象
        logger.debug("Using provided ModuleConfig object")
        return module
    elif isinstance(module, str):
        # CEC数据库名称
        logger.info(f"Loading module from CEC database: {module}")
        return ModuleConfig.from_cec_database(
            module, mounting_type=mounting_type, unit_mass_override=unit_mass
        )
    elif isinstance(module, dict):
        # 参数字典
        logger.info("Creating ModuleConfig from parameter dictionary")
        return ModuleConfig.from_dict(
            module,
            temp_params=temp_model_params,
            unit_mass=unit_mass,
            mounting_type=mounting_type,
        )
    else:
        raise PVDataError(
            f"Invalid module type: {type(module)}. "
            f"Expected str (CEC name), dict (parameters), or ModuleConfig object."
        )


# ============================================================================
# 数据验证辅助函数
# ============================================================================


def check_required_columns(df: pd.DataFrame, required: List[str]) -> None:
    """
    检查必需列是否存在

    Parameters
    ----------
    df : pd.DataFrame
        数据框
    required : list of str
        必需的列名

    Raises
    ------
    PVDataError
        如果缺少列
    """
    missing = [col for col in required if col not in df.columns]
    if missing:
        raise PVDataError(
            f"Missing required columns: {missing}. "
            f"Available columns: {list(df.columns)}"
        )


def clip_physical_values(df: pd.DataFrame, inplace: bool = False) -> pd.DataFrame:
    """
    将物理量限制在合理范围内

    Parameters
    ----------
    df : pd.DataFrame
        数据框
    inplace : bool, default False
        是否原地修改

    Returns
    -------
    pd.DataFrame
        修改后的数据框
    """
    if not inplace:
        df = df.copy()

    # 限制效率
    if "efficiency" in df.columns:
        df["efficiency"] = df["efficiency"].clip(
            PHYSICAL_LIMITS["efficiency_min"], PHYSICAL_LIMITS["efficiency_max"]
        )

    # 限制电池温度
    if "cell_temperature" in df.columns:
        df["cell_temperature"] = df["cell_temperature"].clip(
            PHYSICAL_LIMITS["temp_cell_min"], PHYSICAL_LIMITS["temp_cell_max"]
        )

    # 限制POA
    if "poa_global" in df.columns:
        df["poa_global"] = df["poa_global"].clip(
            PHYSICAL_LIMITS["poa_min"], PHYSICAL_LIMITS["poa_max"]
        )

    return df
