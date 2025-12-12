"""
Food security scoring module.
Computes food security indicators using NDVI and agricultural potential.
"""

import numpy as np
from typing import Dict, Optional


class FoodSecurityScorer:
    """
    Scores food security based on vegetation indices and agricultural indicators.
    """
    
    def __init__(self):
        # NDVI thresholds for vegetation health
        self.ndvi_thresholds = {
            'bare': 0.0,
            'sparse': 0.2,
            'moderate': 0.4,
            'dense': 0.6,
            'very_dense': 0.8
        }
        
    def compute_food_security_score(self, satellite_data: Dict,
                                   population_data: Dict = None) -> Dict:
        """
        Compute food security score from satellite data.
        
        Args:
            satellite_data: Satellite imagery features
            population_data: Optional population data
            
        Returns:
            Dictionary with food security metrics
        """
        print("Computing food security score")
        
        ndvi = satellite_data.get('ndvi', 0)
        
        # Base score from NDVI
        ndvi_score = self._ndvi_to_score(ndvi)
        
        # Agricultural potential (simplified)
        ag_potential = self._estimate_agricultural_potential(satellite_data)
        
        # Vegetation health classification
        veg_health = satellite_data.get('vegetation_health', 
                                       self._classify_ndvi(ndvi))
        
        # Overall food security score
        # Combines vegetation health and agricultural potential
        overall_score = 0.6 * ndvi_score + 0.4 * ag_potential
        
        result = {
            'score': float(overall_score),
            'ndvi': float(ndvi),
            'ndvi_score': float(ndvi_score),
            'agricultural_potential': float(ag_potential),
            'vegetation_health': veg_health,
            'classification': self._classify_food_security(overall_score),
            'risk_level': self._assess_risk(overall_score)
        }
        
        # Add population pressure if available
        if population_data:
            pop_density = population_data.get('population_density', 0)
            pressure = self._compute_population_pressure(ndvi_score, pop_density)
            result['population_pressure'] = pressure
        
        return result
    
    def _ndvi_to_score(self, ndvi: float) -> float:
        """
        Convert NDVI to food security score.
        
        Args:
            ndvi: NDVI value (-1 to 1)
            
        Returns:
            Score (0-1)
        """
        if ndvi < 0.0:
            return 0.0
        elif ndvi < 0.2:
            # Very sparse vegetation
            return ndvi / 0.2 * 0.3
        elif ndvi < 0.4:
            # Sparse to moderate
            return 0.3 + (ndvi - 0.2) / 0.2 * 0.3
        elif ndvi < 0.6:
            # Moderate to good
            return 0.6 + (ndvi - 0.4) / 0.2 * 0.2
        else:
            # Good to excellent
            return 0.8 + min((ndvi - 0.6) / 0.4 * 0.2, 0.2)
    
    def _estimate_agricultural_potential(self, satellite_data: Dict) -> float:
        """
        Estimate agricultural potential from satellite features.
        
        Args:
            satellite_data: Satellite features
            
        Returns:
            Agricultural potential score (0-1)
        """
        ndvi = satellite_data.get('ndvi', 0)
        ndbi = satellite_data.get('ndbi', 0)
        buildup = satellite_data.get('buildup_index', 0)
        
        # Good agriculture: high NDVI, low built-up
        ag_score = 0.0
        
        # Positive factors
        if 0.3 < ndvi < 0.7:  # Optimal range for crops
            ag_score += 0.5
        elif ndvi >= 0.2:
            ag_score += 0.3
        
        # Negative factors
        if buildup > 0.5:  # High built-up = less agricultural land
            ag_score *= 0.5
        
        if ndbi > 0.2:  # High built-up index
            ag_score *= 0.7
        
        return float(np.clip(ag_score, 0, 1))
    
    def _classify_ndvi(self, ndvi: float) -> str:
        """Classify vegetation health from NDVI."""
        if ndvi < 0.0:
            return "water_or_snow"
        elif ndvi < 0.2:
            return "bare_or_sparse"
        elif ndvi < 0.4:
            return "moderate_vegetation"
        elif ndvi < 0.6:
            return "good_vegetation"
        else:
            return "dense_vegetation"
    
    def _classify_food_security(self, score: float) -> str:
        """Classify food security level."""
        if score > 0.7:
            return "food_secure"
        elif score > 0.5:
            return "moderately_secure"
        elif score > 0.3:
            return "at_risk"
        else:
            return "food_insecure"
    
    def _assess_risk(self, score: float) -> str:
        """Assess food security risk level."""
        if score > 0.7:
            return "low_risk"
        elif score > 0.5:
            return "moderate_risk"
        elif score > 0.3:
            return "high_risk"
        else:
            return "critical_risk"
    
    def _compute_population_pressure(self, food_score: float, 
                                    pop_density: float) -> Dict:
        """
        Compute population pressure on food resources.
        
        Args:
            food_score: Food security score
            pop_density: Population density per km²
            
        Returns:
            Population pressure metrics
        """
        # Pressure = population / food_production_capacity
        # Simplified: high population + low food score = high pressure
        
        # Normalize population density (log scale)
        normalized_pop = np.log1p(pop_density) / np.log1p(10000)
        
        # Pressure increases with population and decreases with food score
        pressure = normalized_pop * (1 - food_score)
        
        return {
            'pressure_index': float(pressure),
            'population_density': float(pop_density),
            'food_production_capacity': float(food_score),
            'assessment': 'high' if pressure > 0.6 else 'moderate' if pressure > 0.3 else 'low'
        }
    
    def compute_drought_risk(self, ndvi: float, 
                            ndvi_historical: Optional[float] = None) -> Dict:
        """
        Assess drought risk from current and historical NDVI.
        
        Args:
            ndvi: Current NDVI
            ndvi_historical: Historical average NDVI (optional)
            
        Returns:
            Drought risk metrics
        """
        risk_score = 0.0
        
        # Current vegetation stress
        if ndvi < 0.2:
            risk_score = 0.8
        elif ndvi < 0.3:
            risk_score = 0.5
        elif ndvi < 0.4:
            risk_score = 0.3
        else:
            risk_score = 0.1
        
        # If historical data available, check for decline
        if ndvi_historical is not None:
            decline = (ndvi_historical - ndvi) / max(ndvi_historical, 0.1)
            if decline > 0.3:  # 30% decline
                risk_score = min(risk_score + 0.3, 1.0)
        
        return {
            'drought_risk_score': float(risk_score),
            'current_ndvi': float(ndvi),
            'historical_ndvi': float(ndvi_historical) if ndvi_historical else None,
            'risk_level': 'critical' if risk_score > 0.7 else 'high' if risk_score > 0.5 else 'moderate' if risk_score > 0.3 else 'low'
        }


def compute_food_security_score(satellite_data: Dict,
                                population_data: Dict = None) -> Dict:
    """
    Convenience function to compute food security score.
    
    Args:
        satellite_data: Satellite imagery features
        population_data: Optional population data
        
    Returns:
        Dictionary with food security metrics
    """
    scorer = FoodSecurityScorer()
    return scorer.compute_food_security_score(satellite_data, population_data)
