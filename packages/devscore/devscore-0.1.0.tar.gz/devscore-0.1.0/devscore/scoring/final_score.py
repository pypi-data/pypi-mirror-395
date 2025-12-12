"""
Final development score aggregation module.
Combines all component scores into a single development index.
"""

import numpy as np
from typing import Dict, Optional
from ..data import (
    get_satellite_features,
    get_nightlights,
    get_infrastructure_data,
    get_population_density
)
from .poverty import compute_poverty_score
from .market_access import compute_market_access_score
from .infrastructure import compute_infrastructure_score
from .food_security import compute_food_security_score
from .mobile_money import compute_mobile_money_score
from .weights import determine_optimal_weights, AHPWeightCalculator


class DevelopmentScoreCalculator:
    """
    Calculates comprehensive development score from all indicators.
    Supports both fixed and dynamic weight determination.
    """
    
    def __init__(self, weight_method: str = 'ahp', custom_weights: Optional[Dict[str, float]] = None):
        """
        Initialize calculator with specified weighting method.
        
        Args:
            weight_method: Method for determining weights ('fixed', 'ahp', 'entropy', 'pca', 'critic', 'auto')
            custom_weights: Optional custom weights dict (overrides weight_method)
        """
        if custom_weights is not None:
            # Use custom weights
            self.weights = custom_weights
            self.weight_method = 'custom'
        elif weight_method == 'fixed':
            # Legacy fixed weights based on research
            self.weights = {
                'poverty': 0.35,
                'market_access': 0.20,
                'infrastructure': 0.20,
                'food_security': 0.15,
                'mobile_money': 0.10
            }
            self.weight_method = 'fixed'
        elif weight_method == 'ahp':
            # AHP-based weights from expert judgment
            ahp_calc = AHPWeightCalculator()
            self.weights = ahp_calc.get_development_weights_ahp()
            self.weight_method = 'ahp'
        else:
            # Will be calculated from data (entropy, pca, critic, auto)
            self.weight_method = weight_method
            self.weights = None  # Will be calculated when data is available
        
    def compute_development_score(self, lat: float, lon: float,
                                 buffer_km: float = 5.0,
                                 year: int = 2023) -> Dict:
        """
        Compute comprehensive development score for a location.
        
        Args:
            lat: Latitude
            lon: Longitude
            buffer_km: Buffer radius for analysis
            year: Year of data
            
        Returns:
            Dictionary with all scores and components
        """
        print(f"\n{'='*60}")
        print(f"Computing Development Score for ({lat:.4f}, {lon:.4f})")
        print(f"{'='*60}\n")
        
        # Step 1: Collect all data
        print("Step 1/6: Collecting satellite data...")
        satellite_data = get_satellite_features(lat, lon, buffer_km)
        
        print("Step 2/6: Collecting nightlights data...")
        nightlights_data = get_nightlights(lat, lon, year)
        
        print("Step 3/6: Collecting infrastructure data...")
        infrastructure_data = get_infrastructure_data(lat, lon, int(buffer_km * 1000))
        
        print("Step 4/6: Collecting population data...")
        population_data = get_population_density(lat, lon, year)
        
        # Combine all data
        all_data = {
            'satellite': satellite_data,
            'nightlights': nightlights_data,
            'infrastructure': infrastructure_data,
            'population': population_data
        }
        
        # Step 2: Compute component scores
        print("\nStep 5/6: Computing component scores...")
        
        # Poverty score
        poverty_result = compute_poverty_score(all_data)
        poverty_score = 1 - poverty_result['poverty_score']  # Invert: higher = better
        
        # Market access score
        market_access_result = compute_market_access_score(
            lat, lon, infrastructure_data, population_data
        )
        all_data['market_access'] = market_access_result
        market_access_score = market_access_result['score']
        
        # Infrastructure score
        infrastructure_result = compute_infrastructure_score(
            infrastructure_data, population_data, buffer_km
        )
        infrastructure_score = infrastructure_result['overall_score']
        
        # Food security score
        food_security_result = compute_food_security_score(
            satellite_data, population_data
        )
        food_security_score = food_security_result['score']
        
        # Mobile money score
        mobile_money_result = compute_mobile_money_score(
            infrastructure_data, population_data, nightlights_data
        )
        mobile_money_score = mobile_money_result['score']
        
        # Step 3: Compute overall development score
        print("\nStep 6/6: Computing overall development score...")
        
        component_scores = {
            'poverty': poverty_score,
            'market_access': market_access_score,
            'infrastructure': infrastructure_score,
            'food_security': food_security_score,
            'mobile_money': mobile_money_score
        }
        
        overall_score = sum(
            self.weights[component] * score
            for component, score in component_scores.items()
        )
        
        # Compile results
        result = {
            'overall': float(overall_score),
            'components': {
                'poverty': float(poverty_score),
                'market_access': float(market_access_score),
                'infrastructure': float(infrastructure_score),
                'food_security': float(food_security_score),
                'mobile_money': float(mobile_money_score)
            },
            'weights': self.weights,
            'classification': self._classify_development(overall_score),
            'location': {'lat': lat, 'lon': lon},
            'parameters': {
                'buffer_km': buffer_km,
                'year': year
            },
            'detailed_results': {
                'poverty': poverty_result,
                'market_access': market_access_result,
                'infrastructure': infrastructure_result,
                'food_security': food_security_result,
                'mobile_money': mobile_money_result
            },
            'raw_data': all_data
        }
        
        # Calculate dynamic weights if needed
        if self.weights is None:
            component_scores_dict = {
                'poverty': [component_scores['poverty']],
                'market_access': [component_scores['market_access']],
                'infrastructure': [component_scores['infrastructure']],
                'food_security': [component_scores['food_security']],
                'mobile_money': [component_scores['mobile_money']]
            }
            # For single location, use AHP as fallback
            print(f"\nNote: Using AHP method for single-location analysis")
            ahp_calc = AHPWeightCalculator()
            self.weights = ahp_calc.get_development_weights_ahp()
        
        # Print summary
        self._print_summary(result)
        
        return result
    
    def _classify_development(self, score: float) -> str:
        """Classify overall development level."""
        if score > 0.75:
            return "highly_developed"
        elif score > 0.6:
            return "well_developed"
        elif score > 0.45:
            return "moderately_developed"
        elif score > 0.3:
            return "developing"
        else:
            return "underdeveloped"
    
    def update_weights_from_data(self, component_scores: Dict[str, list]):
        """
        Update weights dynamically from historical component scores.
        
        Args:
            component_scores: Dictionary with component names as keys and lists of scores as values
        """
        if self.weight_method in ['entropy', 'pca', 'critic', 'auto']:
            self.weights = determine_optimal_weights(component_scores, method=self.weight_method)
            print(f"\nWeights updated using {self.weight_method} method:")
            for comp, weight in self.weights.items():
                print(f"  {comp}: {weight:.3f}")
    
    def _print_summary(self, result: Dict):
        """Print formatted summary of results."""
        print(f"\n{'='*60}")
        print("DEVELOPMENT SCORE SUMMARY")
        print(f"{'='*60}\n")
        
        print(f"Location: ({result['location']['lat']:.4f}, {result['location']['lon']:.4f})")
        print(f"Overall Development Score: {result['overall']:.3f}")
        print(f"Classification: {result['classification'].upper().replace('_', ' ')}\n")
        
        print("Component Scores:")
        print("-" * 60)
        for component, score in result['components'].items():
            weight = result['weights'][component]
            bar = '█' * int(score * 30) + '░' * (30 - int(score * 30))
            print(f"{component.replace('_', ' ').title():20} {score:.3f} [{bar}] (weight: {weight:.2f})")
        
        print(f"\n{'='*60}\n")
    
    def compare_locations(self, locations: list) -> Dict:
        """
        Compare development scores across multiple locations.
        
        Args:
            locations: List of (lat, lon) tuples
            
        Returns:
            Comparison results
        """
        results = []
        
        for lat, lon in locations:
            score = self.compute_development_score(lat, lon)
            results.append({
                'location': (lat, lon),
                'overall_score': score['overall'],
                'components': score['components'],
                'classification': score['classification']
            })
        
        # Rank by overall score
        results.sort(key=lambda x: x['overall_score'], reverse=True)
        
        return {
            'locations': results,
            'best': results[0],
            'worst': results[-1],
            'average_score': np.mean([r['overall_score'] for r in results])
        }
    
    def compute_regional_average(self, lat_min: float, lat_max: float,
                                lon_min: float, lon_max: float,
                                grid_size: int = 5) -> Dict:
        """
        Compute average development score for a region.
        
        Args:
            lat_min, lat_max: Latitude bounds
            lon_min, lon_max: Longitude bounds
            grid_size: Number of sample points per dimension
            
        Returns:
            Regional statistics
        """
        print(f"Computing regional average with {grid_size}x{grid_size} grid...")
        
        lats = np.linspace(lat_min, lat_max, grid_size)
        lons = np.linspace(lon_min, lon_max, grid_size)
        
        scores = []
        
        for lat in lats:
            for lon in lons:
                try:
                    result = self.compute_development_score(lat, lon)
                    scores.append(result['overall'])
                except Exception as e:
                    print(f"Error at ({lat:.4f}, {lon:.4f}): {e}")
        
        if not scores:
            return {'error': 'No valid scores computed'}
        
        return {
            'mean': float(np.mean(scores)),
            'median': float(np.median(scores)),
            'std': float(np.std(scores)),
            'min': float(np.min(scores)),
            'max': float(np.max(scores)),
            'n_samples': len(scores)
        }


def compute_development_score(lat: float, lon: float, 
                             buffer_km: float = 5.0,
                             year: int = 2023) -> Dict:
    """
    Convenience function to compute development score.
    
    Args:
        lat: Latitude
        lon: Longitude
        buffer_km: Buffer radius for analysis
        year: Year of data
        
    Returns:
        Dictionary with comprehensive development score
    """
    calculator = DevelopmentScoreCalculator()
    return calculator.compute_development_score(lat, lon, buffer_km, year)
