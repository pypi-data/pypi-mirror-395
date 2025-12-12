"""
POA辐照度计算

将GHI/DNI/DHI转换为倾斜平面辐照度
"""

from typing import Union, Optional
import pandas as pd
import numpy as np
import pvlib

from ..utils.logger import get_logger
from ..utils.decorators import log_execution
from ..utils.exceptions import PVDataError

from .utils import get_column_value, check_required_columns

logger = get_logger(__name__)


@log_execution(level="debug")
def calculate_poa_irradiance(
    df: pd.DataFrame,
    surface_tilt: Union[float, str],
    surface_azimuth: Union[float, str],
    albedo: Union[float, str] = 0.2,
    solar_zenith_col: str = "solar_zenith",
    solar_azimuth_col: str = "solar_azimuth",
    model: str = "isotropic",
    inplace: bool = False,
) -> pd.DataFrame:
    """
    计算平面阵列辐照度（POA）

    将GHI/DNI/DHI转换为倾斜阵列上的辐照度

    Parameters
    ----------
    df : pd.DataFrame
        输入数据，必须包含:
        - GHI: 全球水平辐照度 [W/m²]
        - DNI: 直射法向辐照度 [W/m²]
        - DHI: 散射水平辐照度 [W/m²]
        - solar_zenith: 太阳天顶角 [度]（或通过solar_zenith_col指定）
        - solar_azimuth: 太阳方位角 [度]（或通过solar_azimuth_col指定）

    surface_tilt : float or str
        组件倾角 [度]，0-90°
        - float: 固定倾角
        - str: DataFrame中的列名（支持每行不同倾角）

    surface_azimuth : float or str
        组件方位角 [度]，0-360°
        北=0°，东=90°，南=180°，西=270°
        - float: 固定方位角
        - str: DataFrame中的列名

    albedo : float or str, default 0.2
        地面反射率（0-1）
        - float: 固定值（通用默认0.2）
        - str: DataFrame中的列名（如'Surface Albedo'）

    solar_zenith_col : str, default 'solar_zenith'
        太阳天顶角列名

    solar_azimuth_col : str, default 'solar_azimuth'
        太阳方位角列名

    model : str, default 'isotropic'
        散射辐照度模型
        - 'isotropic': 各向同性天空（最简单，最快）
        - 'klucher': Klucher模型（考虑地平线增亮）
        - 'haydavies': Hay-Davies模型（各向异性）
        - 'reindl': Reindl模型（各向异性+地平线）
        - 'king': King模型
        - 'perez': Perez模型（最复杂，最准确）

    inplace : bool, default False
        是否原地修改DataFrame

    Returns
    -------
    pd.DataFrame
        原数据 + 新增列:
        - poa_global: POA总辐照度 [W/m²]
        - poa_direct: POA直射辐照度 [W/m²]
        - poa_sky_diffuse: POA天空散射 [W/m²]
        - poa_ground_diffuse: POA地面反射 [W/m²]
        - aoi: 入射角 [度]

    Raises
    ------
    PVDataError
        如果缺少必需列或参数无效

    Examples
    --------
    >>> import pvdata as pv
    >>> df = pv.read_parquet('weather.parquet')
    >>> df_poa = pv.calculate_poa_irradiance(
    ...     df,
    ...     surface_tilt=30,
    ...     surface_azimuth=180,
    ...     model='isotropic'
    ... )
    >>> print(df_poa[['GHI', 'poa_global', 'aoi']].head())

    Notes
    -----
    - POA = Plane of Array（平面阵列辐照度）
    - isotropic模型适用于大多数情况，计算快速
    - perez模型最准确但计算较慢，推荐用于高精度需求
    - 如果DNI或DHI缺失，会尝试使用DISC/DIRINT模型分解GHI
    """
    if not inplace:
        df = df.copy()

    # 检查必需列
    required_cols = ["GHI", solar_zenith_col, solar_azimuth_col]
    check_required_columns(df, required_cols)

    # 获取倾角和方位角（支持列名或标量）
    tilt = get_column_value(df, surface_tilt, "surface_tilt")
    azimuth = get_column_value(df, surface_azimuth, "surface_azimuth")

    # 验证倾角和方位角范围
    if isinstance(tilt, (int, float)):
        if not (0 <= tilt <= 90):
            raise PVDataError(
                f"surface_tilt must be between 0 and 90 degrees, got {tilt}"
            )
    else:
        if (tilt < 0).any() or (tilt > 90).any():
            logger.warning(
                f"Some surface_tilt values are out of range [0, 90]: "
                f"min={tilt.min():.1f}, max={tilt.max():.1f}"
            )

    if isinstance(azimuth, (int, float)):
        if not (0 <= azimuth <= 360):
            logger.warning(
                f"surface_azimuth should be between 0 and 360 degrees, got {azimuth}"
            )
    else:
        if (azimuth < 0).any() or (azimuth > 360).any():
            logger.warning(
                f"Some surface_azimuth values are out of range [0, 360]: "
                f"min={azimuth.min():.1f}, max={azimuth.max():.1f}"
            )

    # 获取反射率
    if isinstance(albedo, str):
        if albedo in df.columns:
            albedo_val = df[albedo]
            logger.debug(f"Using albedo from column '{albedo}'")
        else:
            logger.warning(
                f"Albedo column '{albedo}' not found, using default 0.2"
            )
            albedo_val = 0.2
    else:
        albedo_val = float(albedo)
        logger.debug(f"Using constant albedo: {albedo_val}")

    # 检查DNI和DHI是否存在
    has_dni = "DNI" in df.columns
    has_dhi = "DHI" in df.columns

    if not has_dni or not has_dhi:
        logger.warning(
            "DNI or DHI not found in DataFrame. "
            "Attempting to decompose GHI using DISC/DIRINT model..."
        )

        # 使用DISC模型分解GHI
        try:
            # 需要额外时间信息用于分解
            if "timestamp" not in df.columns:
                raise PVDataError(
                    "Missing timestamp column required for GHI decomposition"
                )

            # DISC模型分解
            disc_output = pvlib.irradiance.disc(
                ghi=df["GHI"],
                solar_zenith=df[solar_zenith_col],
                datetime_or_doy=df["timestamp"],
            )

            df["DNI"] = disc_output["dni"]
            df["DHI"] = df["GHI"] - df["DNI"] * np.cos(np.radians(df[solar_zenith_col]))
            df["DHI"] = df["DHI"].clip(lower=0)  # 确保非负

            logger.info("Successfully decomposed GHI to DNI and DHI using DISC model")

        except Exception as e:
            raise PVDataError(
                f"Failed to decompose GHI to DNI/DHI: {e}. "
                f"Please provide DNI and DHI columns in input data."
            )

    # 计算入射角（AOI）
    aoi = pvlib.irradiance.aoi(
        surface_tilt=tilt,
        surface_azimuth=azimuth,
        solar_zenith=df[solar_zenith_col],
        solar_azimuth=df[solar_azimuth_col],
    )
    df["aoi"] = aoi

    # 计算POA辐照度
    logger.debug(f"Calculating POA irradiance using {model} model")

    try:
        if model == "isotropic":
            poa_components = pvlib.irradiance.get_total_irradiance(
                surface_tilt=tilt,
                surface_azimuth=azimuth,
                solar_zenith=df[solar_zenith_col],
                solar_azimuth=df[solar_azimuth_col],
                dni=df["DNI"],
                ghi=df["GHI"],
                dhi=df["DHI"],
                albedo=albedo_val,
                model="isotropic",
            )
        elif model in ["klucher", "haydavies", "reindl", "king", "perez"]:
            poa_components = pvlib.irradiance.get_total_irradiance(
                surface_tilt=tilt,
                surface_azimuth=azimuth,
                solar_zenith=df[solar_zenith_col],
                solar_azimuth=df[solar_azimuth_col],
                dni=df["DNI"],
                ghi=df["GHI"],
                dhi=df["DHI"],
                albedo=albedo_val,
                model=model,
            )
        else:
            raise PVDataError(
                f"Unknown diffuse model: '{model}'. "
                f"Valid options: isotropic, klucher, haydavies, reindl, king, perez"
            )

    except Exception as e:
        raise PVDataError(f"POA calculation failed: {e}")

    # 添加结果列
    df["poa_global"] = poa_components["poa_global"]
    df["poa_direct"] = poa_components["poa_direct"]
    df["poa_sky_diffuse"] = poa_components["poa_sky_diffuse"]
    df["poa_ground_diffuse"] = poa_components["poa_ground_diffuse"]

    # 确保非负（物理约束）
    for col in ["poa_global", "poa_direct", "poa_sky_diffuse", "poa_ground_diffuse"]:
        df[col] = df[col].clip(lower=0)

    logger.debug(
        f"POA irradiance calculated: "
        f"mean poa_global={df['poa_global'].mean():.1f} W/m², "
        f"max={df['poa_global'].max():.1f} W/m²"
    )

    return df


def calculate_aoi(
    surface_tilt: Union[float, pd.Series],
    surface_azimuth: Union[float, pd.Series],
    solar_zenith: pd.Series,
    solar_azimuth: pd.Series,
) -> pd.Series:
    """
    计算入射角（Angle of Incidence）

    Parameters
    ----------
    surface_tilt : float or pd.Series
        组件倾角 [度]
    surface_azimuth : float or pd.Series
        组件方位角 [度]
    solar_zenith : pd.Series
        太阳天顶角 [度]
    solar_azimuth : pd.Series
        太阳方位角 [度]

    Returns
    -------
    pd.Series
        入射角 [度]，0-90°

    Examples
    --------
    >>> aoi = calculate_aoi(
    ...     surface_tilt=30,
    ...     surface_azimuth=180,
    ...     solar_zenith=df['solar_zenith'],
    ...     solar_azimuth=df['solar_azimuth']
    ... )
    """
    return pvlib.irradiance.aoi(
        surface_tilt=surface_tilt,
        surface_azimuth=surface_azimuth,
        solar_zenith=solar_zenith,
        solar_azimuth=solar_azimuth,
    )


def decompose_ghi(
    ghi: pd.Series,
    solar_zenith: pd.Series,
    datetime_or_doy: pd.Series,
    model: str = "disc",
) -> pd.DataFrame:
    """
    将GHI分解为DNI和DHI

    当DNI/DHI数据缺失时使用

    Parameters
    ----------
    ghi : pd.Series
        全球水平辐照度 [W/m²]
    solar_zenith : pd.Series
        太阳天顶角 [度]
    datetime_or_doy : pd.Series
        时间戳或一年中的第几天
    model : str, default 'disc'
        分解模型
        - 'disc': DISC模型（推荐）
        - 'dirint': DIRINT模型
        - 'dirindex': DIRINDEX模型
        - 'erbs': Erbs模型

    Returns
    -------
    pd.DataFrame
        包含 'dni' 和 'dhi' 列

    Examples
    --------
    >>> result = decompose_ghi(
    ...     ghi=df['GHI'],
    ...     solar_zenith=df['solar_zenith'],
    ...     datetime_or_doy=df['timestamp']
    ... )
    >>> df['DNI'] = result['dni']
    >>> df['DHI'] = result['dhi']

    Notes
    -----
    - DISC模型最常用，准确性适中，速度快
    - DIRINT在高纬度地区更准确但需要额外参数
    - 分解结果是估算值，精度低于直接测量
    """
    logger.info(f"Decomposing GHI using {model} model")

    if model == "disc":
        disc_output = pvlib.irradiance.disc(
            ghi=ghi, solar_zenith=solar_zenith, datetime_or_doy=datetime_or_doy
        )
        dni = disc_output["dni"]

    elif model == "dirint":
        dni = pvlib.irradiance.dirint(
            ghi=ghi, solar_zenith=solar_zenith, times=datetime_or_doy
        )

    elif model == "dirindex":
        dni = pvlib.irradiance.dirindex(
            ghi=ghi, solar_zenith=solar_zenith, times=datetime_or_doy
        )

    elif model == "erbs":
        erbs_output = pvlib.irradiance.erbs(ghi=ghi, zenith=solar_zenith)
        dni = erbs_output["dni"]
        dhi = erbs_output["dhi"]
        return pd.DataFrame({"dni": dni, "dhi": dhi})

    else:
        raise PVDataError(
            f"Unknown decomposition model: '{model}'. "
            f"Valid options: disc, dirint, dirindex, erbs"
        )

    # 计算DHI = GHI - DNI * cos(zenith)
    dhi = ghi - dni * np.cos(np.radians(solar_zenith))
    dhi = dhi.clip(lower=0)  # 确保非负

    return pd.DataFrame({"dni": dni, "dhi": dhi})
