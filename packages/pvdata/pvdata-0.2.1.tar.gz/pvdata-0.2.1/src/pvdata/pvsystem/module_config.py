"""
光伏组件配置类

管理组件的电气参数、几何参数和热参数
"""

from dataclasses import dataclass
from typing import Dict, Any, Optional
import pandas as pd
import pvlib

from ..utils.logger import get_logger
from ..utils.exceptions import PVDataError

from .constants import (
    SAPM_STANDARD_PARAMS,
    DEFAULT_VALUES,
)
from .utils import (
    validate_cec_params,
    infer_mount_type,
    infer_sapm_temp_params,
    validate_temp_params_with_noct,
    infer_unit_mass_robust,
)

logger = get_logger(__name__)


@dataclass
class ModuleConfig:
    """
    光伏组件完整配置

    包含电气参数（CEC单二极管模型）、热参数（SAPM温度模型）和几何参数

    Attributes
    ----------
    cec_params : dict
        CEC单二极管模型的完整参数（12+个）
    sapm_temp_params : dict
        SAPM温度模型参数 {'a': float, 'b': float, 'deltaT': float}
    unit_mass : float
        单位面积质量 [kg/m²]，用于Prilliman热惯性模型
    area : float
        组件单面面积 [m²]
    length : float
        组件长度 [m]
    width : float
        组件宽度 [m]
    name : str
        组件名称/型号
    technology : str
        技术类型（Mono-c-Si, Multi-Si, CdTe等）
    rated_power : float
        额定功率 [W]（STC条件）
    mounting_type : str
        安装方式（open_rack_glass_polymer等）

    Examples
    --------
    从CEC数据库加载：

    >>> config = ModuleConfig.from_cec_database('Canadian_Solar_CS5P_220M___2009_')
    >>> print(config.rated_power)  # 220.0
    >>> print(config.sapm_temp_params)  # {'a': -3.56, 'b': -0.075, 'deltaT': 3}

    自定义参数：

    >>> config = ModuleConfig.from_dict({
    ...     'Technology': 'Mono-c-Si',
    ...     'STC': 300,
    ...     'A_c': 1.6,
    ...     'I_sc_ref': 8.5,
    ...     # ... 其他CEC参数
    ... })
    """

    cec_params: Dict[str, Any]
    sapm_temp_params: Dict[str, float]
    unit_mass: float
    area: float
    length: float
    width: float
    name: str
    technology: str
    rated_power: float
    mounting_type: str

    @classmethod
    def from_cec_database(
        cls,
        module_name: str,
        mounting_type: Optional[str] = None,
        unit_mass_override: Optional[float] = None,
    ) -> "ModuleConfig":
        """
        从CEC数据库加载组件，自动推断温度参数

        Parameters
        ----------
        module_name : str
            CEC数据库中的组件名称
            查找名称: pvlib.pvsystem.retrieve_sam('CECMod').columns
        mounting_type : str, optional
            安装方式，不提供则自动推断
            选项: 'open_rack_glass_polymer', 'close_mount_glass_glass',
                  'insulated_back_glass_polymer', 'open_rack_glass_glass'
        unit_mass_override : float, optional
            覆盖推断的unit_mass [kg/m²]

        Returns
        -------
        ModuleConfig
            完整配置对象

        Raises
        ------
        PVDataError
            如果组件名称不存在或参数无效

        Examples
        --------
        >>> # 自动推断所有参数
        >>> config = ModuleConfig.from_cec_database('Canadian_Solar_CS5P_220M___2009_')
        >>>
        >>> # 指定安装方式
        >>> config = ModuleConfig.from_cec_database(
        ...     'Canadian_Solar_CS5P_220M___2009_',
        ...     mounting_type='close_mount_glass_glass'
        ... )
        >>>
        >>> # 覆盖质量参数
        >>> config = ModuleConfig.from_cec_database(
        ...     'Canadian_Solar_CS5P_220M___2009_',
        ...     unit_mass_override=12.5
        ... )
        """
        logger.info(f"Loading module from CEC database: {module_name}")

        # 加载CEC数据库
        try:
            cec_modules = pvlib.pvsystem.retrieve_sam("CECMod")
        except Exception as e:
            raise PVDataError(f"Failed to load CEC database: {e}")

        if module_name not in cec_modules.columns:
            raise PVDataError(
                f"Module '{module_name}' not found in CEC database. "
                f"Total modules available: {len(cec_modules.columns)}. "
                f"Use pvlib.pvsystem.retrieve_sam('CECMod').columns to see all names."
            )

        # 提取参数
        cec_params = cec_modules[module_name].to_dict()

        # 验证参数完整性
        validate_cec_params(cec_params)

        # 推断或使用指定的安装方式
        if mounting_type is None:
            inferred_mount = infer_mount_type(cec_params)
            logger.debug(f"Inferred mounting type: {inferred_mount}")
        else:
            if mounting_type not in SAPM_STANDARD_PARAMS:
                raise PVDataError(
                    f"Invalid mounting_type: {mounting_type}. "
                    f"Valid options: {list(SAPM_STANDARD_PARAMS.keys())}"
                )
            inferred_mount = mounting_type
            logger.debug(f"Using specified mounting type: {mounting_type}")

        # 获取SAPM温度参数
        sapm_params = SAPM_STANDARD_PARAMS[inferred_mount]

        # 验证温度参数（使用T_NOCT）- 静默模式
        passed, message = validate_temp_params_with_noct(
            cec_params, sapm_params, inferred_mount
        )
        # Validation result logged internally, no warning needed
        logger.debug(f"T_NOCT validation for {module_name}: {message}")

        # 推断unit_mass
        if unit_mass_override is None:
            unit_mass = infer_unit_mass_robust(cec_params, inferred_mount)
        else:
            unit_mass = unit_mass_override
            logger.debug(f"Using override unit_mass: {unit_mass} kg/m²")

        # 创建实例
        return cls(
            cec_params=cec_params,
            sapm_temp_params=sapm_params,
            unit_mass=unit_mass,
            area=cec_params["A_c"],
            length=cec_params.get("Length", DEFAULT_VALUES["module_length"]),
            width=cec_params.get("Width", DEFAULT_VALUES["module_width"]),
            name=module_name,
            technology=cec_params["Technology"],
            rated_power=cec_params["STC"],
            mounting_type=inferred_mount,
        )

    @classmethod
    def from_dict(
        cls,
        params: Dict[str, Any],
        temp_params: Optional[Dict[str, float]] = None,
        unit_mass: Optional[float] = None,
        mounting_type: Optional[str] = None,
    ) -> "ModuleConfig":
        """
        从参数字典创建配置（高级用户）

        Parameters
        ----------
        params : dict
            必须包含完整CEC参数
        temp_params : dict, optional
            温度参数 {'a': float, 'b': float, 'deltaT': float}
            不提供则自动推断
        unit_mass : float, optional
            质量参数 [kg/m²]，不提供则自动推断
        mounting_type : str, optional
            安装方式，用于推断温度参数

        Returns
        -------
        ModuleConfig
            配置对象

        Raises
        ------
        PVDataError
            如果缺少必需参数

        Examples
        --------
        >>> config = ModuleConfig.from_dict({
        ...     'Technology': 'Mono-c-Si',
        ...     'STC': 300, 'A_c': 1.6,
        ...     'I_sc_ref': 8.5, 'V_oc_ref': 45.2,
        ...     'I_mp_ref': 8.0, 'V_mp_ref': 37.5,
        ...     'alpha_sc': 0.004, 'beta_oc': -0.15,
        ...     'a_ref': 1.6, 'I_L_ref': 8.52,
        ...     'I_o_ref': 2e-10, 'R_s': 0.3,
        ...     'R_sh_ref': 300, 'Adjust': 2.5,
        ...     'N_s': 72
        ... })
        >>>
        >>> # 自定义温度参数
        >>> config = ModuleConfig.from_dict(
        ...     params,
        ...     temp_params={'a': -3.5, 'b': -0.08, 'deltaT': 3.5}
        ... )
        """
        logger.debug("Creating ModuleConfig from dictionary")

        # 验证必需参数
        validate_cec_params(params)

        # 推断或使用提供的温度参数
        if temp_params is None:
            if mounting_type is None:
                inferred_mount = infer_mount_type(params)
            else:
                inferred_mount = mounting_type
            temp_params = SAPM_STANDARD_PARAMS[inferred_mount]
        else:
            # 验证温度参数格式
            required_keys = ["a", "b", "deltaT"]
            missing = [k for k in required_keys if k not in temp_params]
            if missing:
                raise PVDataError(
                    f"Missing temperature parameters: {missing}. "
                    f"Required: {required_keys}"
                )
            inferred_mount = mounting_type or "custom"

        # 推断unit_mass
        if unit_mass is None:
            if inferred_mount != "custom":
                unit_mass = infer_unit_mass_robust(params, inferred_mount)
            else:
                unit_mass = DEFAULT_VALUES["unit_mass"]
                logger.warning(
                    f"Using default unit_mass: {unit_mass} kg/m² "
                    f"(custom temp params provided)"
                )

        # 设置默认几何参数（如果缺失）
        if "Length" not in params:
            params["Length"] = DEFAULT_VALUES["module_length"]
            logger.warning(
                f"Length not provided, using default: {DEFAULT_VALUES['module_length']}m"
            )
        if "Width" not in params:
            params["Width"] = DEFAULT_VALUES["module_width"]
            logger.warning(
                f"Width not provided, using default: {DEFAULT_VALUES['module_width']}m"
            )

        return cls(
            cec_params=params,
            sapm_temp_params=temp_params,
            unit_mass=unit_mass,
            area=params["A_c"],
            length=params["Length"],
            width=params["Width"],
            name=params.get("name", "CustomModule"),
            technology=params["Technology"],
            rated_power=params["STC"],
            mounting_type=inferred_mount,
        )

    def __repr__(self) -> str:
        """字符串表示"""
        return (
            f"ModuleConfig(name='{self.name}', technology='{self.technology}', "
            f"rated_power={self.rated_power:.1f}W, area={self.area:.2f}m², "
            f"mounting='{self.mounting_type}')"
        )

    def __str__(self) -> str:
        """详细字符串表示"""
        return (
            f"ModuleConfig: {self.name}\n"
            f"  Technology: {self.technology}\n"
            f"  Rated Power: {self.rated_power:.1f} W (STC)\n"
            f"  Area: {self.area:.3f} m²\n"
            f"  Dimensions: {self.length:.2f}m × {self.width:.2f}m\n"
            f"  Mounting Type: {self.mounting_type}\n"
            f"  SAPM Temp Params: a={self.sapm_temp_params['a']:.3f}, "
            f"b={self.sapm_temp_params['b']:.4f}, deltaT={self.sapm_temp_params['deltaT']}\n"
            f"  Unit Mass: {self.unit_mass:.1f} kg/m²"
        )

    def to_dict(self) -> Dict[str, Any]:
        """
        转换为字典

        Returns
        -------
        dict
            包含所有配置参数的字典
        """
        return {
            "name": self.name,
            "technology": self.technology,
            "rated_power": self.rated_power,
            "area": self.area,
            "length": self.length,
            "width": self.width,
            "mounting_type": self.mounting_type,
            "sapm_temp_params": self.sapm_temp_params,
            "unit_mass": self.unit_mass,
            "cec_params": self.cec_params,
        }

    def get_efficiency_at_stc(self) -> float:
        """
        计算STC条件下的参考效率

        Returns
        -------
        float
            参考效率（0-1）

        Examples
        --------
        >>> config = ModuleConfig.from_cec_database('Canadian_Solar_CS5P_220M___2009_')
        >>> eff = config.get_efficiency_at_stc()
        >>> print(f"STC efficiency: {eff:.2%}")  # 17.5%
        """
        # STC效率 = 额定功率 / (1000 W/m² × 面积)
        stc_efficiency = self.rated_power / (1000.0 * self.area)
        return stc_efficiency

    def get_power_density(self) -> float:
        """
        计算功率密度

        Returns
        -------
        float
            功率密度 [W/m²]

        Examples
        --------
        >>> config = ModuleConfig.from_cec_database('Canadian_Solar_CS5P_220M___2009_')
        >>> pd = config.get_power_density()
        >>> print(f"Power density: {pd:.1f} W/m²")  # 175.0 W/m²
        """
        return self.rated_power / self.area

    def get_temperature_coefficient(self) -> float:
        """
        获取最大功率温度系数

        Returns
        -------
        float
            温度系数 [1/°C]

        Examples
        --------
        >>> config = ModuleConfig.from_cec_database('Canadian_Solar_CS5P_220M___2009_')
        >>> gamma = config.get_temperature_coefficient()
        >>> print(f"Temp coefficient: {gamma:.4f} /°C")  # -0.0045 /°C
        """
        if "gamma_r" in self.cec_params:
            return self.cec_params["gamma_r"]
        else:
            # 估算：gamma_r ≈ beta_oc / V_mp_ref
            beta_oc = self.cec_params["beta_oc"]
            v_mp = self.cec_params["V_mp_ref"]
            gamma_estimated = beta_oc / v_mp
            logger.debug(
                f"gamma_r not in CEC params, estimated from beta_oc: {gamma_estimated:.6f}"
            )
            return gamma_estimated

    def update_mounting_type(self, new_mounting_type: str) -> None:
        """
        更新安装方式并重新计算相关参数

        Parameters
        ----------
        new_mounting_type : str
            新的安装方式

        Raises
        ------
        PVDataError
            如果安装方式无效

        Examples
        --------
        >>> config = ModuleConfig.from_cec_database('Canadian_Solar_CS5P_220M___2009_')
        >>> print(config.mounting_type)  # open_rack_glass_polymer
        >>> config.update_mounting_type('close_mount_glass_glass')
        >>> print(config.mounting_type)  # close_mount_glass_glass
        >>> print(config.sapm_temp_params)  # {'a': -2.98, 'b': -0.047, 'deltaT': 1}
        """
        if new_mounting_type not in SAPM_STANDARD_PARAMS:
            raise PVDataError(
                f"Invalid mounting_type: {new_mounting_type}. "
                f"Valid options: {list(SAPM_STANDARD_PARAMS.keys())}"
            )

        logger.info(
            f"Updating mounting type from '{self.mounting_type}' to '{new_mounting_type}'"
        )

        self.mounting_type = new_mounting_type
        self.sapm_temp_params = SAPM_STANDARD_PARAMS[new_mounting_type]

        # 重新计算unit_mass
        self.unit_mass = infer_unit_mass_robust(self.cec_params, new_mounting_type)

        logger.info(
            f"Updated: SAPM params={self.sapm_temp_params}, unit_mass={self.unit_mass:.1f} kg/m²"
        )
