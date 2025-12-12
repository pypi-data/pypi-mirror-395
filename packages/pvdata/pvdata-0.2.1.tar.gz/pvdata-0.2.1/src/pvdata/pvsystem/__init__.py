"""
pvdata.pvsystem - 光伏系统性能计算

主要功能:
- 计算光伏组件发电潜力（POA辐照度 → 温度 → 功率 → 效率）
- 支持CEC单二极管模型（21,500+组件）
- 考虑热惯性（Prilliman模型）
- 向量化计算，高性能

Examples
--------
>>> import pvdata as pv
>>> df = pv.read_parquet('weather.parquet')
>>> df_pv = pv.calculate_pv_potential(
...     df,
...     module='Canadian_Solar_CS5P_220M___2009_',
...     surface_tilt=30,
...     surface_azimuth=180
... )
>>> print(df_pv[['poa_global', 'cell_temperature', 'dc_power', 'efficiency']].head())
"""

from .module_config import ModuleConfig
from .constants import (
    SAPM_STANDARD_PARAMS,
    SAPM_BASE_PARAMS_BY_TECH,
    MODULE_DENSITY_BY_TECH,
    DEFAULT_OUTPUT_COLUMNS,
    ALL_OUTPUT_COLUMNS,
)

# 阶段2计算函数
from .irradiance import calculate_poa_irradiance, calculate_aoi, decompose_ghi
from .temperature import (
    calculate_cell_temperature,
    calculate_sapm_cell_temperature,
    calculate_pvsyst_cell_temperature,
    apply_prilliman_thermal_inertia,
    calculate_noct_temperature,
)
from .power import (
    calculate_dc_power,
    calculate_efficiency,
    calculate_iv_curve_points,
    calculate_max_power_point,
)

# 主函数（阶段3）
from .core import calculate_pv_potential

__all__ = [
    # 核心类
    "ModuleConfig",
    # 常量（高级用户）
    "SAPM_STANDARD_PARAMS",
    "SAPM_BASE_PARAMS_BY_TECH",
    "MODULE_DENSITY_BY_TECH",
    "DEFAULT_OUTPUT_COLUMNS",
    "ALL_OUTPUT_COLUMNS",
    # 分步计算函数
    "calculate_poa_irradiance",
    "calculate_aoi",
    "decompose_ghi",
    "calculate_cell_temperature",
    "calculate_sapm_cell_temperature",
    "calculate_pvsyst_cell_temperature",
    "apply_prilliman_thermal_inertia",
    "calculate_noct_temperature",
    "calculate_dc_power",
    "calculate_efficiency",
    "calculate_iv_curve_points",
    "calculate_max_power_point",
    # 主要函数（阶段3）
    "calculate_pv_potential",
]

__version__ = "0.2.0"
