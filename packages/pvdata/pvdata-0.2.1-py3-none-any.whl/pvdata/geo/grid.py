"""
Geographic grid generation utilities

Provides functions to generate grid points around a center location.
"""

import math
from typing import Dict, List


def haversine_distance(
    lat1: float, lon1: float, lat2: float, lon2: float
) -> float:
    """
    Calculate the great circle distance between two points on Earth.

    Args:
        lat1: Latitude of first point (degrees)
        lon1: Longitude of first point (degrees)
        lat2: Latitude of second point (degrees)
        lon2: Longitude of second point (degrees)

    Returns:
        Distance in kilometers

    Examples:
        >>> # Distance from Phoenix to Chicago
        >>> haversine_distance(33.4484, -112.0740, 41.8781, -87.6298)
        2237.9

        >>> # Distance should be symmetric
        >>> d1 = haversine_distance(0, 0, 1, 1)
        >>> d2 = haversine_distance(1, 1, 0, 0)
        >>> abs(d1 - d2) < 0.001
        True
    """
    # Earth radius in kilometers
    R = 6371.0

    # Convert to radians
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)

    # Haversine formula
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad

    a = (
        math.sin(dlat / 2) ** 2
        + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2) ** 2
    )
    c = 2 * math.asin(math.sqrt(a))

    return R * c


def generate_grid(
    center_lat: float,
    center_lon: float,
    pattern: str = "10_point",
    radius_km: float = 20,
) -> List[Dict]:
    """
    Generate grid points around a center location.

    Args:
        center_lat: Center latitude (degrees)
        center_lon: Center longitude (degrees)
        pattern: Grid pattern type. Options:
            - "10_point": Center + 8 directions @ radius + North @ radius/2
            - "5_point": Center + 4 cardinal directions (N, E, S, W)
            - "9_point": 3x3 grid
        radius_km: Radius in kilometers

    Returns:
        List of grid point dictionaries, each containing:
            - grid_id: Grid point identifier (int)
            - lat: Latitude (float)
            - lon: Longitude (float)
            - description: Human-readable description (str)

    Examples:
        >>> # Generate 10-point grid around Phoenix
        >>> grids = generate_grid(33.4484, -112.0740, pattern="10_point", radius_km=20)
        >>> len(grids)
        10
        >>> grids[0]['description']
        'center'

        >>> # Generate 5-point grid
        >>> grids = generate_grid(33.4484, -112.0740, pattern="5_point", radius_km=10)
        >>> len(grids)
        5
    """
    if pattern == "10_point":
        return _generate_10_point_grid(center_lat, center_lon, radius_km)
    elif pattern == "5_point":
        return _generate_5_point_grid(center_lat, center_lon, radius_km)
    elif pattern == "9_point":
        return _generate_9_point_grid(center_lat, center_lon, radius_km)
    else:
        raise ValueError(
            f"Unknown pattern: {pattern}. "
            "Supported patterns: '10_point', '5_point', '9_point'"
        )


def _generate_10_point_grid(
    center_lat: float, center_lon: float, radius_km: float
) -> List[Dict]:
    """
    Generate 10-point grid pattern.

    Pattern:
        - Grid 0: Center point
        - Grid 1-8: 8 directions (N, NE, E, SE, S, SW, W, NW) at radius_km
        - Grid 9: North direction at radius_km/2

    Grid layout:
            N (grid 9, 10km)
                 ↑
                 |
        NW   N   |   NE
          ↖  ↑  ↗
        W  ← ● →  E     ● = center (grid 0)
          ↙  ↓  ↘        others = 20km radius
        SW   S    SE
    """
    R = 6371.0  # Earth radius (km)

    # Calculate latitude and longitude offsets
    # Latitude offset is straightforward
    lat_offset = (radius_km / R) * (180.0 / math.pi)

    # Longitude offset depends on latitude (gets larger near poles)
    lon_offset = (radius_km / R) * (180.0 / math.pi) / math.cos(
        center_lat * math.pi / 180.0
    )

    grids = []

    # Grid 0: Center
    grids.append(
        {
            "grid_id": 0,
            "lat": center_lat,
            "lon": center_lon,
            "description": "center",
        }
    )

    # Grid 1-8: 8 directions
    directions = [
        (1, "N", 1, 0),  # North
        (2, "NE", 1, 1),  # Northeast
        (3, "E", 0, 1),  # East
        (4, "SE", -1, 1),  # Southeast
        (5, "S", -1, 0),  # South
        (6, "SW", -1, -1),  # Southwest
        (7, "W", 0, -1),  # West
        (8, "NW", 1, -1),  # Northwest
    ]

    for grid_id, direction, lat_mult, lon_mult in directions:
        grids.append(
            {
                "grid_id": grid_id,
                "lat": center_lat + lat_offset * lat_mult,
                "lon": center_lon + lon_offset * lon_mult,
                "description": f"{direction}_{radius_km}km",
            }
        )

    # Grid 9: North at half radius
    grids.append(
        {
            "grid_id": 9,
            "lat": center_lat + lat_offset / 2,
            "lon": center_lon,
            "description": f"N_{radius_km//2}km",
        }
    )

    return grids


def _generate_5_point_grid(
    center_lat: float, center_lon: float, radius_km: float
) -> List[Dict]:
    """
    Generate 5-point grid pattern.

    Pattern:
        - Grid 0: Center
        - Grid 1-4: Cardinal directions (N, E, S, W)

    Grid layout:
            N (grid 1)
             ↑
             |
    W ← ● → E     ● = center (grid 0)
        (4) (0) (2)
             |
             ↓
            S (grid 3)
    """
    R = 6371.0
    lat_offset = (radius_km / R) * (180.0 / math.pi)
    lon_offset = (radius_km / R) * (180.0 / math.pi) / math.cos(
        center_lat * math.pi / 180.0
    )

    return [
        {
            "grid_id": 0,
            "lat": center_lat,
            "lon": center_lon,
            "description": "center",
        },
        {
            "grid_id": 1,
            "lat": center_lat + lat_offset,
            "lon": center_lon,
            "description": f"N_{radius_km}km",
        },
        {
            "grid_id": 2,
            "lat": center_lat,
            "lon": center_lon + lon_offset,
            "description": f"E_{radius_km}km",
        },
        {
            "grid_id": 3,
            "lat": center_lat - lat_offset,
            "lon": center_lon,
            "description": f"S_{radius_km}km",
        },
        {
            "grid_id": 4,
            "lat": center_lat,
            "lon": center_lon - lon_offset,
            "description": f"W_{radius_km}km",
        },
    ]


def _generate_9_point_grid(
    center_lat: float, center_lon: float, radius_km: float
) -> List[Dict]:
    """
    Generate 9-point grid pattern (3x3 grid).

    Pattern:
        - 3x3 grid with center and 8 surrounding points

    Grid layout:
        NW    N    NE
        (6)  (1)  (7)

        W  ● ●  E
        (3) (0) (4)

        SW    S    SE
        (8)  (2)  (5)
    """
    R = 6371.0
    lat_offset = (radius_km / R) * (180.0 / math.pi)
    lon_offset = (radius_km / R) * (180.0 / math.pi) / math.cos(
        center_lat * math.pi / 180.0
    )

    return [
        # Center
        {
            "grid_id": 0,
            "lat": center_lat,
            "lon": center_lon,
            "description": "center",
        },
        # First ring (cardinal)
        {
            "grid_id": 1,
            "lat": center_lat + lat_offset,
            "lon": center_lon,
            "description": f"N_{radius_km}km",
        },
        {
            "grid_id": 2,
            "lat": center_lat - lat_offset,
            "lon": center_lon,
            "description": f"S_{radius_km}km",
        },
        {
            "grid_id": 3,
            "lat": center_lat,
            "lon": center_lon - lon_offset,
            "description": f"W_{radius_km}km",
        },
        {
            "grid_id": 4,
            "lat": center_lat,
            "lon": center_lon + lon_offset,
            "description": f"E_{radius_km}km",
        },
        # Second ring (diagonal)
        {
            "grid_id": 5,
            "lat": center_lat - lat_offset,
            "lon": center_lon + lon_offset,
            "description": f"SE_{radius_km}km",
        },
        {
            "grid_id": 6,
            "lat": center_lat + lat_offset,
            "lon": center_lon - lon_offset,
            "description": f"NW_{radius_km}km",
        },
        {
            "grid_id": 7,
            "lat": center_lat + lat_offset,
            "lon": center_lon + lon_offset,
            "description": f"NE_{radius_km}km",
        },
        {
            "grid_id": 8,
            "lat": center_lat - lat_offset,
            "lon": center_lon - lon_offset,
            "description": f"SW_{radius_km}km",
        },
    ]
