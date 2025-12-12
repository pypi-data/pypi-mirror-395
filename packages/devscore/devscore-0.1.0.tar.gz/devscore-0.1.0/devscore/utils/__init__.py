"""
Utility functions initialization.
"""

from .geospatial import (
    haversine_distance,
    create_buffer,
    latlon_to_utm,
    get_epsg_from_latlon,
    calculate_area_km2,
    create_grid,
    point_in_polygon,
    calculate_bbox,
    degrees_to_meters,
    meters_to_degrees,
    validate_coordinates,
    normalize_longitude
)

from .preprocessing import (
    normalize_features,
    handle_missing_values,
    clip_outliers,
    smooth_timeseries,
    create_feature_matrix,
    aggregate_spatial_data,
    calculate_percentile_rank,
    log_transform,
    inverse_log_transform,
    bin_continuous_variable,
    calculate_z_score,
    robust_scale,
    weighted_average,
    interpolate_missing
)

__all__ = [
    # Geospatial
    'haversine_distance',
    'create_buffer',
    'latlon_to_utm',
    'get_epsg_from_latlon',
    'calculate_area_km2',
    'create_grid',
    'point_in_polygon',
    'calculate_bbox',
    'degrees_to_meters',
    'meters_to_degrees',
    'validate_coordinates',
    'normalize_longitude',
    # Preprocessing
    'normalize_features',
    'handle_missing_values',
    'clip_outliers',
    'smooth_timeseries',
    'create_feature_matrix',
    'aggregate_spatial_data',
    'calculate_percentile_rank',
    'log_transform',
    'inverse_log_transform',
    'bin_continuous_variable',
    'calculate_z_score',
    'robust_scale',
    'weighted_average',
    'interpolate_missing',
]
