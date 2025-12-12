"""
Infrastructure scoring module.
Computes infrastructure density and quality scores.
"""

import numpy as np
from typing import Dict, List


class InfrastructureScorer:
    """
    Scores infrastructure development based on amenity density and diversity.
    """
    
    def __init__(self):
        # Benchmark values (amenities per km²) for different development levels
        self.benchmarks = {
            'schools': {'low': 0.5, 'medium': 2, 'high': 5},
            'health': {'low': 0.2, 'medium': 1, 'high': 3},
            'markets': {'low': 0.1, 'medium': 0.5, 'high': 2},
            'banks': {'low': 0.1, 'medium': 0.5, 'high': 2},
        }
        
    def compute_infrastructure_score(self, infrastructure_data: Dict,
                                    buffer_km: float = 5.0) -> Dict:
        """
        Compute overall infrastructure score.
        
        Args:
            infrastructure_data: Infrastructure data from OSM
            buffer_km: Buffer radius for density calculation
            
        Returns:
            Dictionary with infrastructure scores
        """
        print(f"Computing infrastructure score")
        
        amenity_counts = infrastructure_data.get('amenity_counts', {})
        road_network = infrastructure_data.get('road_network', {})
        
        # Calculate area
        area_km2 = buffer_km ** 2 * 3.14159
        
        # Compute density scores for each amenity type
        density_scores = {}
        for amenity_type in ['schools', 'health', 'markets', 'banks']:
            count = amenity_counts.get(amenity_type, 0)
            density = count / area_km2 if area_km2 > 0 else 0
            
            # Normalize by benchmark
            benchmark_high = self.benchmarks[amenity_type]['high']
            score = min(density / benchmark_high, 1.0)
            
            density_scores[amenity_type] = {
                'count': count,
                'density': float(density),
                'score': float(score)
            }
        
        # Overall amenity score (average)
        amenity_score = np.mean([
            density_scores[k]['score'] 
            for k in density_scores.keys()
        ])
        
        # Road network score
        road_density = road_network.get('density_km_per_km2', 0)
        road_score = min(road_density / 5.0, 1.0)  # Normalize by typical urban
        
        # Combined infrastructure score (70% amenities, 30% roads)
        overall_score = 0.7 * amenity_score + 0.3 * road_score
        
        # Diversity index (how many types of amenities are present)
        diversity = sum(
            1 for k in density_scores.keys() 
            if density_scores[k]['count'] > 0
        ) / len(density_scores)
        
        result = {
            'overall_score': float(overall_score),
            'amenity_score': float(amenity_score),
            'road_score': float(road_score),
            'diversity_index': float(diversity),
            'density_scores': density_scores,
            'total_amenities': amenity_counts.get('total', 0),
            'classification': self._classify_infrastructure(overall_score),
            'area_km2': float(area_km2)
        }
        
        return result
    
    def compute_service_coverage(self, infrastructure_data: Dict,
                                population_data: Dict = None) -> Dict:
        """
        Compute service coverage ratios.
        
        Args:
            infrastructure_data: Infrastructure data
            population_data: Population data (optional)
            
        Returns:
            Service coverage metrics
        """
        amenity_counts = infrastructure_data.get('amenity_counts', {})
        
        # If population data available, compute per-capita metrics
        if population_data:
            population = population_data.get('total_population_estimate', 1000)
            
            # People per service facility
            coverage = {
                'people_per_school': population / max(amenity_counts.get('schools', 0), 1),
                'people_per_health_facility': population / max(amenity_counts.get('health', 0), 1),
                'people_per_market': population / max(amenity_counts.get('markets', 0), 1),
                'people_per_bank': population / max(amenity_counts.get('banks', 0), 1),
            }
            
            # Ideal ratios (WHO/UNESCO recommendations)
            ideal_ratios = {
                'people_per_school': 500,
                'people_per_health_facility': 1000,
                'people_per_market': 2000,
                'people_per_bank': 5000,
            }
            
            # Coverage adequacy scores
            adequacy = {}
            for key in coverage.keys():
                actual = coverage[key]
                ideal = ideal_ratios[key]
                # Score: 1.0 if actual <= ideal, decreases as ratio worsens
                adequacy[key] = min(ideal / actual, 1.0) if actual > 0 else 0
            
            avg_adequacy = np.mean(list(adequacy.values()))
            
            return {
                'coverage_ratios': {k: float(v) for k, v in coverage.items()},
                'adequacy_scores': {k: float(v) for k, v in adequacy.items()},
                'average_adequacy': float(avg_adequacy),
                'population': float(population)
            }
        
        # Without population, just return counts
        return {
            'amenity_counts': amenity_counts,
            'note': 'Population data not available for coverage calculation'
        }
    
    def compute_infrastructure_quality(self, infrastructure_data: Dict) -> Dict:
        """
        Estimate infrastructure quality based on diversity and density.
        
        Args:
            infrastructure_data: Infrastructure data
            
        Returns:
            Quality metrics
        """
        amenity_counts = infrastructure_data.get('amenity_counts', {})
        road_network = infrastructure_data.get('road_network', {})
        
        # Diversity: how many types present
        types_present = sum(
            1 for k in ['schools', 'health', 'markets', 'banks']
            if amenity_counts.get(k, 0) > 0
        )
        diversity_score = types_present / 4
        
        # Density: total amenities per area
        total = amenity_counts.get('total', 0)
        density = amenity_counts.get('density_per_km2', 0)
        density_score = min(density / 20, 1.0)  # Normalize by good urban density
        
        # Road connectivity
        road_score = min(road_network.get('density_km_per_km2', 0) / 5.0, 1.0)
        
        # Quality index (weighted combination)
        quality_index = (
            0.4 * diversity_score +
            0.4 * density_score +
            0.2 * road_score
        )
        
        return {
            'quality_index': float(quality_index),
            'diversity_score': float(diversity_score),
            'density_score': float(density_score),
            'road_connectivity_score': float(road_score),
            'classification': self._classify_quality(quality_index)
        }
    
    def _classify_infrastructure(self, score: float) -> str:
        """Classify infrastructure development level."""
        if score > 0.7:
            return "well_developed"
        elif score > 0.5:
            return "moderately_developed"
        elif score > 0.3:
            return "developing"
        else:
            return "underdeveloped"
    
    def _classify_quality(self, score: float) -> str:
        """Classify infrastructure quality."""
        if score > 0.7:
            return "high_quality"
        elif score > 0.5:
            return "good_quality"
        elif score > 0.3:
            return "moderate_quality"
        else:
            return "low_quality"


def compute_infrastructure_score(infrastructure_data: Dict,
                                population_data: Dict = None,
                                buffer_km: float = 5.0) -> Dict:
    """
    Convenience function to compute infrastructure score.
    
    Args:
        infrastructure_data: Infrastructure data from OSM
        population_data: Optional population data
        buffer_km: Buffer radius
        
    Returns:
        Dictionary with infrastructure scores
    """
    scorer = InfrastructureScorer()
    
    # Compute main score
    result = scorer.compute_infrastructure_score(infrastructure_data, buffer_km)
    
    # Add service coverage if population available
    if population_data:
        coverage = scorer.compute_service_coverage(infrastructure_data, population_data)
        result['service_coverage'] = coverage
    
    # Add quality metrics
    quality = scorer.compute_infrastructure_quality(infrastructure_data)
    result['quality'] = quality
    
    return result
