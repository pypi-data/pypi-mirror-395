"""
OpenStreetMap data collection module.
Fetches infrastructure and amenity data using OSMnx.
"""

import os
import osmnx as ox
import geopandas as gpd
import pandas as pd
from shapely.geometry import Point
from typing import Dict, List, Optional
import warnings

warnings.filterwarnings('ignore')
# Configure OSMnx settings using the new API (v2.0+)
ox.settings.use_cache = True
ox.settings.log_console = False


class OSMDataCollector:
    """
    Collects infrastructure data from OpenStreetMap.
    """
    
    def __init__(self, cache_dir: str = "./data/cache/osm"):
        self.cache_dir = cache_dir
        os.makedirs(cache_dir, exist_ok=True)
        
    def get_amenities(self, lat: float, lon: float, 
                     dist: int = 5000, 
                     amenity_types: Optional[List[str]] = None) -> gpd.GeoDataFrame:
        """
        Get amenities from OSM around a location.
        
        Args:
            lat: Latitude
            lon: Longitude
            dist: Distance in meters
            amenity_types: List of amenity types to fetch
            
        Returns:
            GeoDataFrame with amenities
        """
        if amenity_types is None:
            amenity_types = [
                "school", "hospital", "clinic", "doctors",
                "marketplace", "bank", "atm", "pharmacy",
                "restaurant", "cafe", "fuel", "police"
            ]
        
        print(f"Fetching OSM amenities within {dist}m of ({lat:.4f}, {lon:.4f})")
        
        try:
            # Query OSM for amenities (using v2.0+ API)
            tags = {"amenity": amenity_types}
            gdf = ox.features_from_point(
                (lat, lon),
                tags=tags,
                dist=dist
            )
            
            # Clean and prepare data
            gdf = gdf[gdf.geometry.geom_type.isin(['Point', 'Polygon'])]
            
            # Convert polygons to centroids
            gdf['geometry'] = gdf.geometry.apply(
                lambda x: x.centroid if x.geom_type == 'Polygon' else x
            )
            
            # Add distance from center point
            center = Point(lon, lat)
            gdf['distance_m'] = gdf.geometry.apply(
                lambda x: center.distance(x) * 111139  # Approx meters per degree
            )
            
            return gdf
            
        except Exception as e:
            print(f"Error fetching OSM data: {e}")
            # Return empty GeoDataFrame with expected columns
            return gpd.GeoDataFrame(columns=['amenity', 'name', 'geometry', 'distance_m'])
    
    def get_roads(self, lat: float, lon: float, 
                 dist: int = 5000,
                 network_type: str = 'all') -> Optional[gpd.GeoDataFrame]:
        """
        Get road network from OSM.
        
        Args:
            lat: Latitude
            lon: Longitude
            dist: Distance in meters
            network_type: 'all', 'drive', 'walk', 'bike'
            
        Returns:
            GeoDataFrame with roads
        """
        print(f"Fetching road network within {dist}m of ({lat:.4f}, {lon:.4f})")
        
        try:
            G = ox.graph_from_point(
                (lat, lon),
                dist=dist,
                network_type=network_type,
                simplify=True
            )
            
            # Convert to GeoDataFrame
            gdf_edges = ox.graph_to_gdfs(G, nodes=False, edges=True)
            
            return gdf_edges
            
        except Exception as e:
            print(f"Error fetching road network: {e}")
            return None
    
    def count_amenities_by_type(self, lat: float, lon: float, 
                               dist: int = 5000) -> Dict:
        """
        Count amenities by type around a location.
        
        Args:
            lat: Latitude
            lon: Longitude
            dist: Distance in meters
            
        Returns:
            Dictionary with counts by amenity type
        """
        gdf = self.get_amenities(lat, lon, dist)
        
        if gdf.empty:
            return {
                'schools': 0,
                'health': 0,
                'markets': 0,
                'banks': 0,
                'total': 0,
                'density_per_km2': 0.0
            }
        
        # Count by category
        schools = len(gdf[gdf['amenity'].isin(['school', 'kindergarten', 'university'])])
        health = len(gdf[gdf['amenity'].isin(['hospital', 'clinic', 'doctors', 'pharmacy'])])
        markets = len(gdf[gdf['amenity'].isin(['marketplace', 'supermarket'])])
        banks = len(gdf[gdf['amenity'].isin(['bank', 'atm', 'bureau_de_change'])])
        
        total = len(gdf)
        area_km2 = (dist / 1000) ** 2 * 3.14159
        density = total / area_km2 if area_km2 > 0 else 0
        
        return {
            'schools': schools,
            'health': health,
            'markets': markets,
            'banks': banks,
            'total': total,
            'density_per_km2': density,
            'buffer_m': dist
        }
    
    def get_road_density(self, lat: float, lon: float, 
                        dist: int = 5000) -> Dict:
        """
        Calculate road density around a location.
        
        Args:
            lat: Latitude
            lon: Longitude
            dist: Distance in meters
            
        Returns:
            Dictionary with road statistics
        """
        gdf_roads = self.get_roads(lat, lon, dist)
        
        if gdf_roads is None or gdf_roads.empty:
            return {
                'total_length_km': 0.0,
                'density_km_per_km2': 0.0,
                'num_segments': 0
            }
        
        # Calculate total road length
        gdf_roads = gdf_roads.to_crs(epsg=3857)  # Project to meters
        total_length = gdf_roads['length'].sum() / 1000  # Convert to km
        
        # Calculate density
        area_km2 = (dist / 1000) ** 2 * 3.14159
        density = total_length / area_km2 if area_km2 > 0 else 0
        
        return {
            'total_length_km': total_length,
            'density_km_per_km2': density,
            'num_segments': len(gdf_roads),
            'buffer_m': dist
        }
    
    def get_nearest_amenity(self, lat: float, lon: float, 
                           amenity_type: str,
                           max_dist: int = 50000) -> Dict:
        """
        Find nearest amenity of specified type.
        
        Args:
            lat: Latitude
            lon: Longitude
            amenity_type: Type of amenity (e.g., 'hospital', 'school')
            max_dist: Maximum search distance in meters
            
        Returns:
            Dictionary with nearest amenity info
        """
        gdf = self.get_amenities(lat, lon, max_dist, [amenity_type])
        
        if gdf.empty:
            return {
                'amenity_type': amenity_type,
                'found': False,
                'distance_m': None,
                'distance_km': None
            }
        
        # Find nearest
        nearest = gdf.loc[gdf['distance_m'].idxmin()]
        
        return {
            'amenity_type': amenity_type,
            'found': True,
            'distance_m': float(nearest['distance_m']),
            'distance_km': float(nearest['distance_m'] / 1000),
            'name': nearest.get('name', 'Unknown'),
            'lat': nearest.geometry.y,
            'lon': nearest.geometry.x
        }
    
    def get_infrastructure_summary(self, lat: float, lon: float, 
                                  dist: int = 5000) -> Dict:
        """
        Get comprehensive infrastructure summary.
        
        Args:
            lat: Latitude
            lon: Longitude
            dist: Distance in meters
            
        Returns:
            Dictionary with all infrastructure metrics
        """
        print(f"Generating infrastructure summary for ({lat:.4f}, {lon:.4f})")
        
        # Get amenity counts
        amenities = self.count_amenities_by_type(lat, lon, dist)
        
        # Get road density
        roads = self.get_road_density(lat, lon, dist)
        
        # Find nearest critical amenities
        nearest_hospital = self.get_nearest_amenity(lat, lon, 'hospital', dist*2)
        nearest_school = self.get_nearest_amenity(lat, lon, 'school', dist*2)
        nearest_market = self.get_nearest_amenity(lat, lon, 'marketplace', dist*2)
        
        return {
            'amenity_counts': amenities,
            'road_network': roads,
            'nearest': {
                'hospital': nearest_hospital,
                'school': nearest_school,
                'market': nearest_market
            },
            'lat': lat,
            'lon': lon,
            'buffer_m': dist
        }


def get_infrastructure_data(lat: float, lon: float, 
                           dist: int = 5000) -> Dict:
    """
    Convenience function to get all infrastructure data.
    
    Args:
        lat: Latitude
        lon: Longitude
        dist: Distance in meters
        
    Returns:
        Dictionary with infrastructure summary
    """
    collector = OSMDataCollector()
    return collector.get_infrastructure_summary(lat, lon, dist)
