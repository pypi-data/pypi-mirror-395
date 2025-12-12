"""
常量定义和映射表

包含SAPM温度参数、组件密度、技术类型映射等常量
"""

from typing import Dict, Any

# ============================================================================
# SAPM温度模型参数
# ============================================================================

SAPM_STANDARD_PARAMS: Dict[str, Dict[str, float]] = {
    "open_rack_glass_polymer": {"a": -3.56, "b": -0.075, "deltaT": 3},
    "open_rack_glass_glass": {"a": -3.47, "b": -0.059, "deltaT": 3},
    "close_mount_glass_glass": {"a": -2.98, "b": -0.047, "deltaT": 1},
    "insulated_back_glass_polymer": {"a": -2.81, "b": -0.046, "deltaT": 0},
}
"""
SAPM温度模型的标准参数组

完整方程: T_cell = T_air + (POA / 1000) × exp(a + b × WS) × ΔT

参数说明:
- a: 基础散热系数（无风条件下的散热能力），越小（更负）散热越好
- b: 风速敏感系数（风速对散热的增强效应），越小（更负）风冷效果越显著
- deltaT: 组件与背板温差修正项

4种标准安装类型:
1. open_rack_glass_polymer: 开放式，玻璃-背板结构（散热最好）
   - 应用：地面电站、屋顶（离屋面>10cm）
   - 特点：前后通风良好，风冷效果明显

2. open_rack_glass_glass: 开放式，双玻结构（散热较好）
   - 应用：地面双玻组件、开放式屋顶双玻
   - 特点：双玻增重，但仍有良好通风

3. close_mount_glass_glass: 紧贴式，双玻结构（散热受限）
   - 应用：平屋顶紧贴安装（间隙<5cm）、薄膜组件
   - 特点：背面通风受限，散热能力下降

4. insulated_back_glass_polymer: BIPV，绝热背板（散热最差）
   - 应用：建筑一体化光伏（BIPV）、立面组件
   - 特点：背面完全绝热，无法散热，温度最高

物理意义:
- open_rack vs insulated_back 温度差异可达5-10°C
- 温度每升高1°C，晶硅组件功率下降约0.4-0.5%
"""

# ============================================================================
# 技术类型映射
# ============================================================================

SAPM_BASE_PARAMS_BY_TECH: Dict[str, Dict[str, Any]] = {
    "Mono-c-Si": {
        "base_mount": "open_rack_glass_polymer",
        "typical_absorptance": 0.90,
        "typical_emissivity": 0.84,
        "density_glass_polymer": 11.0,  # kg/m²
        "density_glass_glass": 14.0,  # kg/m²
    },
    "Multi-c-Si": {
        "base_mount": "open_rack_glass_polymer",
        "typical_absorptance": 0.90,
        "typical_emissivity": 0.84,
        "density_glass_polymer": 11.0,
        "density_glass_glass": 14.0,
    },
    "multi-Si": {  # 别名
        "base_mount": "open_rack_glass_polymer",
        "typical_absorptance": 0.90,
        "typical_emissivity": 0.84,
        "density_glass_polymer": 11.0,
        "density_glass_glass": 14.0,
    },
    "CdTe": {  # 碲化镉薄膜
        "base_mount": "close_mount_glass_glass",
        "typical_absorptance": 0.88,
        "typical_emissivity": 0.87,
        "density_glass_glass": 12.0,
    },
    "a-Si": {  # 非晶硅薄膜
        "base_mount": "close_mount_glass_glass",
        "typical_absorptance": 0.88,
        "typical_emissivity": 0.87,
        "density_glass_glass": 10.0,
    },
    "CIGS": {  # 铜铟镓硒薄膜
        "base_mount": "close_mount_glass_glass",
        "typical_absorptance": 0.88,
        "typical_emissivity": 0.87,
        "density_glass_glass": 11.5,
    },
    "HIT-Si": {  # 异质结
        "base_mount": "open_rack_glass_polymer",
        "typical_absorptance": 0.91,
        "typical_emissivity": 0.84,
        "density_glass_polymer": 11.5,
        "density_glass_glass": 14.5,
    },
    "GaAs": {  # 砷化镓（高效，罕见）
        "base_mount": "open_rack_glass_polymer",
        "typical_absorptance": 0.92,
        "typical_emissivity": 0.85,
        "density_glass_polymer": 12.0,
        "density_glass_glass": 15.0,
    },
}
"""
技术类型到SAPM参数的基础映射

根据CEC数据库的Technology字段推断：
1. 默认安装方式 (base_mount)
2. 典型吸收率 (typical_absorptance)
3. 典型发射率 (typical_emissivity)
4. 典型密度 (density_glass_polymer / density_glass_glass)

推断规则:
- 晶硅(Mono/Multi-c-Si): 默认open_rack（最常见）
- 薄膜(CdTe/a-Si/CIGS): 默认close_mount（多为双玻紧贴）
- 异质结(HIT-Si): 高效晶硅，默认open_rack
"""

# ============================================================================
# 组件密度映射（用于unit_mass推算）
# ============================================================================

MODULE_DENSITY_BY_TECH: Dict[str, Dict[str, float]] = {
    "Mono-c-Si": {
        "glass_polymer": 11.0,  # kg/m²
        "glass_glass": 14.0,
    },
    "Multi-c-Si": {
        "glass_polymer": 11.0,
        "glass_glass": 14.0,
    },
    "multi-Si": {
        "glass_polymer": 11.0,
        "glass_glass": 14.0,
    },
    "CdTe": {
        "glass_glass": 12.0,
    },
    "a-Si": {
        "glass_glass": 10.0,
    },
    "CIGS": {
        "glass_glass": 11.5,
    },
    "HIT-Si": {
        "glass_polymer": 11.5,
        "glass_glass": 14.5,
    },
    "GaAs": {
        "glass_polymer": 12.0,
        "glass_glass": 15.0,
    },
}
"""
组件密度映射表 [kg/m²]

用于推算Prilliman热惯性模型所需的unit_mass参数

结构类型:
- glass_polymer: 玻璃-聚合物背板结构（单玻）
- glass_glass: 双玻结构

典型值:
- 晶硅单玻: 11.0 kg/m²
- 晶硅双玻: 14.0 kg/m²
- 薄膜双玻: 10.0-12.0 kg/m²

注: 实际密度还受组件厚度、边框类型等影响，表中为典型值
"""

# ============================================================================
# 功率密度到质量的经验映射
# ============================================================================

POWER_DENSITY_TO_MASS: Dict[str, float] = {
    "high_efficiency": 13.0,  # > 180 W/m²（高效组件，可能更重）
    "standard": 11.0,  # 150-180 W/m²（标准组件）
    "low_efficiency": 10.0,  # < 150 W/m²（低效组件或薄膜）
}
"""
功率密度到组件质量的经验映射

功率密度 = STC / A_c [W/m²]

分类:
- 高效 (>180 W/m²): 通常为高效单晶或双玻，质量约13 kg/m²
- 标准 (150-180 W/m²): 标准晶硅组件，质量约11 kg/m²
- 低效 (<150 W/m²): 薄膜或老款多晶，质量约10 kg/m²
"""

# ============================================================================
# CEC参数验证
# ============================================================================

REQUIRED_CEC_PARAMS = [
    "Technology",
    "STC",
    "A_c",
    "N_s",
    "I_sc_ref",
    "V_oc_ref",
    "I_mp_ref",
    "V_mp_ref",
    "alpha_sc",
    "beta_oc",
    "a_ref",
    "I_L_ref",
    "I_o_ref",
    "R_s",
    "R_sh_ref",
    "Adjust",
]
"""
CEC单二极管模型必需的参数列表

这些参数必须存在才能进行完整的I-V特性和功率计算
"""

OPTIONAL_CEC_PARAMS = [
    "T_NOCT",  # 用于验证温度模型
    "BIPV",  # 用于推断安装方式
    "Bifacial",  # 双面组件标识（未实现）
    "PTC",  # PVUSA测试条件功率（验证用）
    "Length",  # 组件长度
    "Width",  # 组件宽度
    "gamma_r",  # 最大功率温度系数（验证用）
]
"""
可选的CEC参数

这些参数有助于改进推断准确性，但不是必需的
"""

# ============================================================================
# 物理约束
# ============================================================================

PHYSICAL_LIMITS = {
    "efficiency_max": 0.30,  # 转换效率上限（实验室记录约47%，商用<30%）
    "efficiency_min": 0.0,  # 转换效率下限
    "temp_cell_max": 120.0,  # 电池温度上限 [°C]（物理损坏阈值约150°C）
    "temp_cell_min": -40.0,  # 电池温度下限 [°C]（极地条件）
    "poa_max": 1500.0,  # POA辐照度上限 [W/m²]（晴天+高反射可达1400）
    "poa_min": 0.0,  # POA辐照度下限 [W/m²]
    "wind_speed_max": 50.0,  # 风速上限 [m/s]（台风级别）
    "wind_speed_min": 0.0,  # 风速下限 [m/s]
    "temp_air_max": 60.0,  # 环境温度上限 [°C]（沙漠极端情况）
    "temp_air_min": -60.0,  # 环境温度下限 [°C]（极地）
}
"""
物理量的合理范围约束

用于数据验证和异常值检测

注: 这些是"合理"范围，不是"可能"范围
实际应用中，超出范围的值会被标记为警告，但不一定被拒绝
"""

# ============================================================================
# NOCT验证参数
# ============================================================================

NOCT_CONDITIONS = {
    "poa_global": 800.0,  # W/m²
    "temp_air": 20.0,  # °C
    "wind_speed": 1.0,  # m/s
    "tolerance": 5.0,  # °C（允许误差）
}
"""
NOCT（Nominal Operating Cell Temperature）验证条件

NOCT定义: 800 W/m²辐照度，20°C环境温度，1 m/s风速条件下的组件工作温度

用于验证推断的SAPM温度参数是否与CEC数据库的T_NOCT匹配

tolerance: 允许±5°C误差（考虑到SAPM模型简化和测试条件差异）
"""

# ============================================================================
# 默认值
# ============================================================================

DEFAULT_VALUES = {
    "module_height": 1.0,  # 组件离地高度 [m]（用于风速调整）
    "albedo": 0.2,  # 地面反射率（通用默认值）
    "mounting_type": "open_rack_glass_polymer",  # 默认安装方式
    "unit_mass": 11.0,  # 默认质量 [kg/m²]（晶硅单玻）
    "diffuse_model": "isotropic",  # 默认散射模型
    "temp_model": "sapm",  # 默认温度模型
    "sun_position_method": "nrel_numpy",  # 默认太阳位置计算方法
    "module_length": 1.6,  # 默认组件长度 [m]
    "module_width": 1.0,  # 默认组件宽度 [m]
}
"""
系统默认值

当用户未提供或CEC数据库缺失时使用
"""

# ============================================================================
# 输出列名称
# ============================================================================

DEFAULT_OUTPUT_COLUMNS = [
    "poa_global",
    "cell_temperature",
    "dc_power",
    "efficiency",
]
"""
默认输出列

calculate_pv_potential函数的默认输出（outputs='default'）
"""

ALL_OUTPUT_COLUMNS = [
    "poa_global",
    "poa_direct",
    "poa_sky_diffuse",
    "poa_ground_diffuse",
    "aoi",
    "temp_cell_steady",
    "cell_temperature",
    "i_sc",
    "v_oc",
    "i_mp",
    "v_mp",
    "dc_power",
    "ac_power",
    "efficiency",
]
"""
所有可能的输出列

calculate_pv_potential函数支持的所有输出（outputs='all'）
"""

# ============================================================================
# 技术类型别名映射（处理数据库不一致）
# ============================================================================

TECHNOLOGY_ALIASES = {
    "mono-c-si": "Mono-c-Si",
    "monocrystalline silicon": "Mono-c-Si",
    "multi-c-si": "Multi-c-Si",
    "multi-si": "Multi-Si",
    "multicrystalline silicon": "Multi-c-Si",
    "polycrystalline silicon": "Multi-c-Si",
    "cdte": "CdTe",
    "cadmium telluride": "CdTe",
    "a-si": "a-Si",
    "amorphous silicon": "a-Si",
    "cigs": "CIGS",
    "hit-si": "HIT-Si",
    "heterojunction": "HIT-Si",
    "gaas": "GaAs",
    "gallium arsenide": "GaAs",
}
"""
技术类型别名映射

处理CEC数据库中可能的大小写不一致或不同命名方式
"""
