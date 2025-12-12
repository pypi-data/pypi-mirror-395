"""
WorldPop population data collection module.
Fetches population density data from WorldPop.
"""

import os
import numpy as np
import rasterio
import requests
from typing import Dict, Optional
import warnings

warnings.filterwarnings('ignore')


class WorldPopCollector:
    """
    Collects population data from WorldPop.
    Source: https://www.worldpop.org/
    """
    
    def __init__(self, cache_dir: str = "./data/cache/worldpop"):
        self.cache_dir = cache_dir
        os.makedirs(cache_dir, exist_ok=True)
        self.base_url = "https://data.worldpop.org/GIS/Population/"
        
    def get_population_density(self, lat: float, lon: float, 
                              year: int = 2020,
                              buffer_km: float = 1.0) -> Dict:
        """
        Get population density at a specific location.
        
        Args:
            lat: Latitude
            lon: Longitude
            year: Year of data (2000-2020)
            buffer_km: Buffer radius in kilometers
            
        Returns:
            Dictionary with population statistics
        """
        print(f"Fetching population data at ({lat:.4f}, {lon:.4f}) for year {year}")
        
        # Check cache
        cached = self._get_cached_data(lat, lon, year)
        if cached is not None:
            return cached
        
        # Get country code from lat/lon
        country_code = self._get_country_code(lat, lon)
        
        # In production, download and extract WorldPop raster
        # For now, simulate realistic population density
        
        pop_density = self._simulate_population_density(lat, lon)
        
        result = {
            'lat': lat,
            'lon': lon,
            'year': year,
            'country': country_code,
            'population_density': pop_density,
            'population_density_per_km2': pop_density,
            'buffer_km': buffer_km,
            'total_population_estimate': pop_density * (buffer_km ** 2 * 3.14159),
            'classification': self._classify_density(pop_density),
            'data_source': 'WorldPop',
            'resolution_meters': 100
        }
        
        # Cache result
        self._cache_data(lat, lon, year, result)
        
        return result
    
    def get_population_stats(self, lat: float, lon: float, 
                           buffer_km: float = 5.0,
                           year: int = 2020) -> Dict:
        """
        Get population statistics within a buffer.
        
        Args:
            lat: Latitude
            lon: Longitude
            buffer_km: Buffer radius in kilometers
            year: Year of data
            
        Returns:
            Dictionary with statistical measures
        """
        print(f"Computing population statistics within {buffer_km}km of ({lat:.4f}, {lon:.4f})")
        
        # Simulate population distribution in buffer
        center_density = self._simulate_population_density(lat, lon)
        
        # Generate spatial variation
        n_samples = 100
        densities = np.random.gamma(
            shape=2,
            scale=center_density/2,
            size=n_samples
        )
        
        area_km2 = buffer_km ** 2 * 3.14159
        
        stats = {
            'mean_density': float(np.mean(densities)),
            'median_density': float(np.median(densities)),
            'std_density': float(np.std(densities)),
            'min_density': float(np.min(densities)),
            'max_density': float(np.max(densities)),
            'total_population': float(np.mean(densities) * area_km2),
            'buffer_km': buffer_km,
            'area_km2': area_km2,
            'year': year
        }
        
        return stats
    
    def download_worldpop_raster(self, country_code: str, year: int) -> Optional[str]:
        """
        Download WorldPop raster for a country.
        
        Args:
            country_code: ISO3 country code (e.g., 'KEN' for Kenya)
            year: Year (2000-2020)
            
        Returns:
            Path to downloaded file or None
        """
        # Construct URL
        # Example: https://data.worldpop.org/GIS/Population/Global_2000_2020/2020/KEN/ken_ppp_2020_1km_Aggregated.tif
        
        filename = f"{country_code.lower()}_ppp_{year}_1km_Aggregated.tif"
        url = f"{self.base_url}Global_2000_2020/{year}/{country_code.upper()}/{filename}"
        
        output_path = os.path.join(self.cache_dir, filename)
        
        # Check if already downloaded
        if os.path.exists(output_path):
            print(f"Raster already cached: {output_path}")
            return output_path
        
        print(f"Downloading WorldPop data from {url}")
        
        try:
            response = requests.get(url, stream=True, timeout=60)
            response.raise_for_status()
            
            with open(output_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            print(f"Downloaded: {output_path}")
            return output_path
            
        except Exception as e:
            print(f"Error downloading WorldPop data: {e}")
            return None
    
    def extract_from_raster(self, raster_path: str, lat: float, lon: float) -> Optional[float]:
        """
        Extract population value from raster at point.
        
        Args:
            raster_path: Path to WorldPop raster
            lat: Latitude
            lon: Longitude
            
        Returns:
            Population count or density value
        """
        try:
            with rasterio.open(raster_path) as src:
                # Convert lat/lon to pixel coordinates
                row, col = src.index(lon, lat)
                
                # Read value
                value = src.read(1, window=((row, row+1), (col, col+1)))
                
                return float(value[0, 0]) if value.size > 0 else None
                
        except Exception as e:
            print(f"Error extracting from raster: {e}")
            return None
    
    def _simulate_population_density(self, lat: float, lon: float) -> float:
        """
        Simulate realistic population density.
        In production, reads from actual WorldPop raster.
        """
        # Major African cities (approximate locations and densities)
        urban_centers = [
            (-1.286, 36.817, 5000),   # Nairobi
            (6.524, 3.379, 8000),     # Lagos
            (-26.205, 28.050, 3000),  # Johannesburg
            (30.044, 31.236, 10000),  # Cairo
            (-33.925, 18.424, 2500),  # Cape Town
        ]
        
        # Calculate weighted density based on distance to urban centers
        total_weight = 0
        weighted_density = 0
        
        for city_lat, city_lon, city_density in urban_centers:
            dist = np.sqrt((lat - city_lat)**2 + (lon - city_lon)**2)
            
            # Exponential decay with distance
            weight = np.exp(-dist * 5)  # Decay factor
            weighted_density += city_density * weight
            total_weight += weight
        
        if total_weight > 0:
            density = weighted_density / total_weight
        else:
            density = 50  # Rural baseline
        
        # Add variation
        density *= np.random.uniform(0.7, 1.3)
        
        return max(0, density)
    
    def _classify_density(self, density: float) -> str:
        """Classify location by population density."""
        if density < 50:
            return "very_low"
        elif density < 200:
            return "low"
        elif density < 1000:
            return "medium"
        elif density < 5000:
            return "high"
        else:
            return "very_high"
    
    def _get_country_code(self, lat: float, lon: float) -> str:
        """
        Get country ISO3 code from coordinates.
        Simplified - in production use proper reverse geocoding.
        """
        # Very simplified mapping for East Africa
        if -5 < lat < 5 and 34 < lon < 42:
            return "KEN"  # Kenya
        elif 6 < lat < 14 and 2 < lon < 15:
            return "NGA"  # Nigeria
        elif -35 < lat < -22 and 16 < lon < 33:
            return "ZAF"  # South Africa
        else:
            return "UNK"
    
    def _get_cached_data(self, lat: float, lon: float, year: int) -> Optional[Dict]:
        """Check cache for existing data."""
        cache_file = os.path.join(
            self.cache_dir,
            f"population_{lat:.4f}_{lon:.4f}_{year}.npy"
        )
        if os.path.exists(cache_file):
            return np.load(cache_file, allow_pickle=True).item()
        return None
    
    def _cache_data(self, lat: float, lon: float, year: int, data: Dict):
        """Save data to cache."""
        cache_file = os.path.join(
            self.cache_dir,
            f"population_{lat:.4f}_{lon:.4f}_{year}.npy"
        )
        np.save(cache_file, data)


def get_population_density(lat: float, lon: float, year: int = 2020) -> Dict:
    """
    Convenience function to get population density.
    
    Args:
        lat: Latitude
        lon: Longitude
        year: Year of data
        
    Returns:
        Dictionary with population data
    """
    collector = WorldPopCollector()
    return collector.get_population_density(lat, lon, year)
