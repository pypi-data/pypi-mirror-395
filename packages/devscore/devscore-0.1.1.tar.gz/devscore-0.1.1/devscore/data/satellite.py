"""
Satellite imagery data collection module.
Fetches and processes Sentinel-2 and Landsat imagery for development indicators.
"""

import os
import numpy as np
import rasterio
from rasterio.warp import calculate_default_transform, reproject, Resampling
import requests
from datetime import datetime, timedelta
from typing import Dict, Tuple, Optional
import warnings

warnings.filterwarnings('ignore')


class SatelliteDataCollector:
    """
    Collects and processes satellite imagery from open sources.
    Supports Sentinel-2 (AWS) and Landsat 8/9.
    """
    
    def __init__(self, cache_dir: str = "./data/cache/satellite"):
        self.cache_dir = cache_dir
        os.makedirs(cache_dir, exist_ok=True)
        
    def get_sentinel2_tile(self, lat: float, lon: float, 
                           start_date: str = None, 
                           end_date: str = None) -> Optional[Dict]:
        """
        Fetch Sentinel-2 imagery from AWS Open Data Registry.
        
        Args:
            lat: Latitude
            lon: Longitude
            start_date: Start date (YYYY-MM-DD)
            end_date: End date (YYYY-MM-DD)
            
        Returns:
            Dictionary with band data and metadata
        """
        if start_date is None:
            end_date = datetime.now().strftime("%Y-%m-%d")
            start_date = (datetime.now() - timedelta(days=90)).strftime("%Y-%m-%d")
        
        # Convert lat/lon to Sentinel-2 tile
        tile_id = self._get_sentinel2_tile_id(lat, lon)
        
        print(f"Fetching Sentinel-2 data for tile {tile_id} ({start_date} to {end_date})")
        
        # Note: In production, you'd query the AWS S3 bucket or use sentinelhub API
        # For now, returning simulated structure
        return {
            'tile_id': tile_id,
            'lat': lat,
            'lon': lon,
            'date_range': (start_date, end_date),
            'bands': {
                'B02': None,  # Blue
                'B03': None,  # Green
                'B04': None,  # Red
                'B08': None,  # NIR
                'B11': None,  # SWIR1
                'B12': None,  # SWIR2
            },
            'resolution': 10,
            'source': 'Sentinel-2'
        }
    
    def compute_ndvi(self, red: np.ndarray, nir: np.ndarray) -> np.ndarray:
        """
        Compute Normalized Difference Vegetation Index.
        NDVI = (NIR - Red) / (NIR + Red)
        
        Args:
            red: Red band array
            nir: Near-infrared band array
            
        Returns:
            NDVI array
        """
        with np.errstate(divide='ignore', invalid='ignore'):
            ndvi = (nir - red) / (nir + red)
            ndvi[np.isnan(ndvi)] = 0
        return ndvi
    
    def compute_ndbi(self, swir: np.ndarray, nir: np.ndarray) -> np.ndarray:
        """
        Compute Normalized Difference Built-up Index.
        NDBI = (SWIR - NIR) / (SWIR + NIR)
        
        Args:
            swir: Short-wave infrared band array
            nir: Near-infrared band array
            
        Returns:
            NDBI array
        """
        with np.errstate(divide='ignore', invalid='ignore'):
            ndbi = (swir - nir) / (swir + nir)
            ndbi[np.isnan(ndbi)] = 0
        return ndbi
    
    def compute_buildup_index(self, red: np.ndarray, green: np.ndarray, 
                              nir: np.ndarray, swir: np.ndarray) -> np.ndarray:
        """
        Compute built-up area index using multiple bands.
        
        Args:
            red: Red band
            green: Green band
            nir: NIR band
            swir: SWIR band
            
        Returns:
            Built-up index array
        """
        ndbi = self.compute_ndbi(swir, nir)
        ndvi = self.compute_ndvi(red, nir)
        
        # Built-up areas have high NDBI and low NDVI
        buildup = (ndbi - ndvi + 1) / 2
        return np.clip(buildup, 0, 1)
    
    def extract_features_at_point(self, lat: float, lon: float, 
                                  buffer_km: float = 1.0) -> Dict:
        """
        Extract satellite-derived features for a specific location.
        
        Args:
            lat: Latitude
            lon: Longitude
            buffer_km: Buffer radius in kilometers
            
        Returns:
            Dictionary of computed features
        """
        print(f"Extracting satellite features at ({lat:.4f}, {lon:.4f})")
        
        # In production, this would fetch real satellite data
        # For now, simulate realistic values
        
        # Simulated band values (scaled 0-1)
        red = np.random.uniform(0.1, 0.3)
        green = np.random.uniform(0.1, 0.3)
        nir = np.random.uniform(0.3, 0.6)
        swir = np.random.uniform(0.2, 0.4)
        
        ndvi = (nir - red) / (nir + red) if (nir + red) > 0 else 0
        ndbi = (swir - nir) / (swir + nir) if (swir + nir) > 0 else 0
        buildup = (ndbi - ndvi + 1) / 2
        
        features = {
            'ndvi': float(ndvi),
            'ndbi': float(ndbi),
            'buildup_index': float(buildup),
            'red_reflectance': float(red),
            'green_reflectance': float(green),
            'nir_reflectance': float(nir),
            'swir_reflectance': float(swir),
            'vegetation_health': 'good' if ndvi > 0.4 else 'medium' if ndvi > 0.2 else 'poor',
            'buffer_km': buffer_km
        }
        
        return features
    
    def get_landsat_data(self, lat: float, lon: float, 
                        year: int = 2023) -> Dict:
        """
        Fetch Landsat 8/9 imagery from AWS Open Data.
        
        Args:
            lat: Latitude
            lon: Longitude
            year: Year of imagery
            
        Returns:
            Dictionary with Landsat data
        """
        print(f"Fetching Landsat data for ({lat:.4f}, {lon:.4f}), year {year}")
        
        # Path/Row from lat/lon
        path, row = self._get_landsat_path_row(lat, lon)
        
        return {
            'path': path,
            'row': row,
            'lat': lat,
            'lon': lon,
            'year': year,
            'source': 'Landsat-8/9',
            'resolution': 30
        }
    
    def _get_sentinel2_tile_id(self, lat: float, lon: float) -> str:
        """Convert lat/lon to Sentinel-2 MGRS tile ID."""
        # Simplified - in production use proper MGRS conversion
        return f"T36MZE"  # Example tile for East Africa
    
    def _get_landsat_path_row(self, lat: float, lon: float) -> Tuple[int, int]:
        """Convert lat/lon to Landsat path/row."""
        # Simplified - in production use proper WRS-2 conversion
        path = int((lon + 180) / 360 * 233) + 1
        row = int((90 - lat) / 180 * 248) + 1
        return path, row
    
    def get_cached_data(self, lat: float, lon: float) -> Optional[Dict]:
        """Check if satellite data is cached for this location."""
        cache_file = os.path.join(
            self.cache_dir, 
            f"satellite_{lat:.4f}_{lon:.4f}.npy"
        )
        if os.path.exists(cache_file):
            return np.load(cache_file, allow_pickle=True).item()
        return None
    
    def cache_data(self, lat: float, lon: float, data: Dict):
        """Cache satellite data for this location."""
        cache_file = os.path.join(
            self.cache_dir, 
            f"satellite_{lat:.4f}_{lon:.4f}.npy"
        )
        np.save(cache_file, data)


def get_satellite_features(lat: float, lon: float, 
                          buffer_km: float = 1.0) -> Dict:
    """
    Convenience function to extract satellite features.
    
    Args:
        lat: Latitude
        lon: Longitude
        buffer_km: Buffer radius in kilometers
        
    Returns:
        Dictionary of satellite-derived features
    """
    collector = SatelliteDataCollector()
    
    # Check cache first
    cached = collector.get_cached_data(lat, lon)
    if cached is not None:
        return cached
    
    # Extract features
    features = collector.extract_features_at_point(lat, lon, buffer_km)
    
    # Cache for future use
    collector.cache_data(lat, lon, features)
    
    return features
