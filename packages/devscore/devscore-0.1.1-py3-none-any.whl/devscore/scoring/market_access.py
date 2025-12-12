"""
Market access scoring module.
Computes accessibility to markets, roads, and economic centers.
"""

import numpy as np
from typing import Dict, List, Tuple
from math import radians, cos, sin, asin, sqrt


class MarketAccessCalculator:
    """
    Calculates market access scores based on distance to key economic amenities.
    Based on economic geography literature.
    """
    
    def __init__(self):
        self.decay_factor = 10000  # Distance decay in meters
        
    def haversine_distance(self, lat1: float, lon1: float, 
                          lat2: float, lon2: float) -> float:
        """
        Calculate great circle distance between two points.
        
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
    
    def compute_accessibility_score(self, distance_m: float) -> float:
        """
        Compute accessibility score from distance using exponential decay.
        
        Args:
            distance_m: Distance in meters (None means no facility found)
            
        Returns:
            Accessibility score (0-1)
        """
        # Handle None/missing distance (no facility found)
        if distance_m is None or distance_m >= 50000:
            return 0.0
            
        # Exponential decay: score = exp(-distance / decay_factor)
        score = np.exp(-distance_m / self.decay_factor)
        return float(score)
    
    def compute_market_access(self, lat: float, lon: float, 
                             infrastructure_data: Dict) -> Dict:
        """
        Compute market access score from infrastructure data.
        
        Args:
            lat: Latitude
            lon: Longitude
            infrastructure_data: OSM infrastructure data
            
        Returns:
            Dictionary with market access metrics
        """
        print(f"Computing market access for ({lat:.4f}, {lon:.4f})")
        
        nearest = infrastructure_data.get('nearest', {})
        
        # Extract distances to key amenities (default to None if not found)
        distances = {
            'market': nearest.get('market', {}).get('distance_m', None),
            'hospital': nearest.get('hospital', {}).get('distance_m', None),
            'school': nearest.get('school', {}).get('distance_m', None),
        }
        
        # Compute accessibility scores (handles None values)
        accessibility = {
            key: self.compute_accessibility_score(dist)
            for key, dist in distances.items()
        }
        
        # Overall market access (weighted average)
        weights = {
            'market': 0.4,
            'hospital': 0.3,
            'school': 0.3
        }
        
        overall_score = sum(
            accessibility[key] * weights[key]
            for key in weights.keys()
        )
        
        # Road access score
        road_density = infrastructure_data.get('road_network', {}).get('density_km_per_km2', 0)
        road_score = min(road_density / 5.0, 1.0)  # Normalize by typical urban density
        
        # Combined score (70% proximity, 30% road network)
        combined_score = 0.7 * overall_score + 0.3 * road_score
        
        result = {
            'score': float(combined_score),
            'distances_m': distances,
            'accessibility_scores': {k: float(v) for k, v in accessibility.items()},
            'road_network_score': float(road_score),
            'classification': self._classify_access(combined_score)
        }
        
        return result
    
    def compute_travel_time(self, distance_m: float, 
                          road_type: str = 'paved') -> float:
        """
        Estimate travel time based on distance and road type.
        
        Args:
            distance_m: Distance in meters
            road_type: 'paved', 'unpaved', 'footpath'
            
        Returns:
            Travel time in minutes
        """
        # Average speeds (km/h)
        speeds = {
            'paved': 40,
            'unpaved': 20,
            'footpath': 4
        }
        
        speed_kmh = speeds.get(road_type, 20)
        distance_km = distance_m / 1000
        time_hours = distance_km / speed_kmh
        
        return time_hours * 60  # Convert to minutes
    
    def compute_economic_potential(self, lat: float, lon: float,
                                  population_data: Dict,
                                  market_access: Dict) -> Dict:
        """
        Compute economic potential based on market access and population.
        
        Args:
            lat: Latitude
            lon: Longitude
            population_data: Population density data
            market_access: Market access scores
            
        Returns:
            Economic potential metrics
        """
        pop_density = population_data.get('population_density', 0)
        market_score = market_access.get('score', 0)
        
        # Economic potential = f(population, accessibility)
        # Using gravity model: Potential = Population * Accessibility
        potential = pop_density * market_score
        
        # Normalize (typical range: 0-5000)
        normalized_potential = min(potential / 5000, 1.0)
        
        return {
            'economic_potential': float(potential),
            'economic_potential_normalized': float(normalized_potential),
            'population_density': float(pop_density),
            'market_access_score': float(market_score)
        }
    
    def _classify_access(self, score: float) -> str:
        """Classify market access level."""
        if score > 0.7:
            return "excellent"
        elif score > 0.5:
            return "good"
        elif score > 0.3:
            return "moderate"
        elif score > 0.1:
            return "poor"
        else:
            return "very_poor"
    
    def compute_isolation_index(self, distances: Dict[str, float]) -> float:
        """
        Compute isolation index based on distances to amenities.
        Higher values indicate more isolation.
        
        Args:
            distances: Dictionary of distances to amenities (None means not found)
            
        Returns:
            Isolation index (0-1)
        """
        # Filter out None values and use 50000m as default for missing
        valid_distances = [d if d is not None else 50000 for d in distances.values()]
        
        if not valid_distances:
            return 1.0  # Maximum isolation if no data
            
        avg_distance = np.mean(valid_distances)
        
        # Normalize by typical maximum (50km)
        isolation = min(avg_distance / 50000, 1.0)
        
        return float(isolation)


def compute_market_access_score(lat: float, lon: float,
                                infrastructure_data: Dict,
                                population_data: Dict = None) -> Dict:
    """
    Convenience function to compute market access score.
    
    Args:
        lat: Latitude
        lon: Longitude
        infrastructure_data: Infrastructure data from OSM
        population_data: Optional population data
        
    Returns:
        Dictionary with market access metrics
    """
    calculator = MarketAccessCalculator()
    
    # Compute basic market access
    result = calculator.compute_market_access(lat, lon, infrastructure_data)
    
    # Add economic potential if population data available
    if population_data:
        potential = calculator.compute_economic_potential(
            lat, lon, population_data, result
        )
        result['economic_potential'] = potential
    
    # Add isolation index
    if 'distances_m' in result:
        result['isolation_index'] = calculator.compute_isolation_index(
            result['distances_m']
        )
    
    return result
