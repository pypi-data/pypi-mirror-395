"""
Geospatial utility functions.
"""

import numpy as np
from math import radians, cos, sin, asin, sqrt
from typing import Tuple, List
from shapely.geometry import Point, Polygon
import geopandas as gpd


def haversine_distance(lat1: float, lon1: float, 
                      lat2: float, lon2: float) -> float:
    """
    Calculate great circle distance between two points on Earth.
    
    Args:
        lat1, lon1: First point coordinates
        lat2, lon2: Second point coordinates
        
    Returns:
        Distance in meters
    """
    # Convert to radians
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    
    # Haversine formula
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    
    # Earth radius in meters
    r = 6371000
    
    return c * r


def create_buffer(lat: float, lon: float, radius_km: float) -> Polygon:
    """
    Create a circular buffer around a point.
    
    Args:
        lat: Latitude
        lon: Longitude
        radius_km: Radius in kilometers
        
    Returns:
        Shapely Polygon
    """
    # Approximate degrees per km at this latitude
    lat_deg_per_km = 1 / 110.574
    lon_deg_per_km = 1 / (111.320 * cos(radians(lat)))
    
    # Create circle points
    angles = np.linspace(0, 2 * np.pi, 64)
    x = lon + radius_km * lon_deg_per_km * np.cos(angles)
    y = lat + radius_km * lat_deg_per_km * np.sin(angles)
    
    return Polygon(zip(x, y))


def latlon_to_utm(lat: float, lon: float) -> Tuple[int, str]:
    """
    Determine UTM zone from lat/lon coordinates.
    
    Args:
        lat: Latitude
        lon: Longitude
        
    Returns:
        Tuple of (zone_number, hemisphere)
    """
    zone_number = int((lon + 180) / 6) + 1
    hemisphere = 'N' if lat >= 0 else 'S'
    
    return zone_number, hemisphere


def get_epsg_from_latlon(lat: float, lon: float) -> int:
    """
    Get appropriate EPSG code for UTM projection.
    
    Args:
        lat: Latitude
        lon: Longitude
        
    Returns:
        EPSG code
    """
    zone_number, hemisphere = latlon_to_utm(lat, lon)
    
    if hemisphere == 'N':
        epsg = 32600 + zone_number
    else:
        epsg = 32700 + zone_number
    
    return epsg


def calculate_area_km2(polygon: Polygon, lat: float = None) -> float:
    """
    Calculate area of polygon in km².
    
    Args:
        polygon: Shapely Polygon
        lat: Latitude for more accurate calculation (optional)
        
    Returns:
        Area in square kilometers
    """
    if lat is not None:
        # Use latitude-adjusted conversion
        lat_deg_per_km = 1 / 110.574
        lon_deg_per_km = 1 / (111.320 * cos(radians(lat)))
        
        # Convert area from deg² to km²
        area_deg2 = polygon.area
        area_km2 = area_deg2 / (lat_deg_per_km * lon_deg_per_km)
    else:
        # Rough approximation
        area_km2 = polygon.area * 12364  # Approx at equator
    
    return area_km2


def create_grid(lat_min: float, lat_max: float,
               lon_min: float, lon_max: float,
               grid_size: int = 10) -> List[Tuple[float, float]]:
    """
    Create a grid of points within bounding box.
    
    Args:
        lat_min, lat_max: Latitude bounds
        lon_min, lon_max: Longitude bounds
        grid_size: Number of points per dimension
        
    Returns:
        List of (lat, lon) tuples
    """
    lats = np.linspace(lat_min, lat_max, grid_size)
    lons = np.linspace(lon_min, lon_max, grid_size)
    
    grid = [(lat, lon) for lat in lats for lon in lons]
    
    return grid


def point_in_polygon(lat: float, lon: float, polygon: Polygon) -> bool:
    """
    Check if point is inside polygon.
    
    Args:
        lat: Latitude
        lon: Longitude
        polygon: Shapely Polygon
        
    Returns:
        True if point is inside polygon
    """
    point = Point(lon, lat)
    return polygon.contains(point)


def calculate_bbox(lat: float, lon: float, buffer_km: float) -> Tuple:
    """
    Calculate bounding box around a point.
    
    Args:
        lat: Latitude
        lon: Longitude
        buffer_km: Buffer in kilometers
        
    Returns:
        Tuple of (min_lat, min_lon, max_lat, max_lon)
    """
    lat_deg_per_km = 1 / 110.574
    lon_deg_per_km = 1 / (111.320 * cos(radians(lat)))
    
    min_lat = lat - buffer_km * lat_deg_per_km
    max_lat = lat + buffer_km * lat_deg_per_km
    min_lon = lon - buffer_km * lon_deg_per_km
    max_lon = lon + buffer_km * lon_deg_per_km
    
    return min_lat, min_lon, max_lat, max_lon


def degrees_to_meters(degrees: float, latitude: float) -> float:
    """
    Convert degrees to meters at given latitude.
    
    Args:
        degrees: Degrees of longitude/latitude
        latitude: Latitude for calculation
        
    Returns:
        Distance in meters
    """
    # For latitude (constant)
    meters_per_lat_degree = 110574
    
    # For longitude (varies with latitude)
    meters_per_lon_degree = 111320 * cos(radians(latitude))
    
    # Return average for simplicity
    return degrees * (meters_per_lat_degree + meters_per_lon_degree) / 2


def meters_to_degrees(meters: float, latitude: float) -> float:
    """
    Convert meters to degrees at given latitude.
    
    Args:
        meters: Distance in meters
        latitude: Latitude for calculation
        
    Returns:
        Degrees
    """
    meters_per_lat_degree = 110574
    meters_per_lon_degree = 111320 * cos(radians(latitude))
    
    avg_meters_per_degree = (meters_per_lat_degree + meters_per_lon_degree) / 2
    
    return meters / avg_meters_per_degree


def validate_coordinates(lat: float, lon: float) -> bool:
    """
    Validate lat/lon coordinates.
    
    Args:
        lat: Latitude
        lon: Longitude
        
    Returns:
        True if valid
    """
    if not (-90 <= lat <= 90):
        return False
    if not (-180 <= lon <= 180):
        return False
    
    return True


def normalize_longitude(lon: float) -> float:
    """
    Normalize longitude to -180 to 180 range.
    
    Args:
        lon: Longitude
        
    Returns:
        Normalized longitude
    """
    while lon > 180:
        lon -= 360
    while lon < -180:
        lon += 360
    
    return lon
