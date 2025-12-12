"""
Mobile money adoption scoring module.
Estimates mobile money potential based on infrastructure and connectivity.
"""

import numpy as np
from typing import Dict


class MobileMoneyScorer:
    """
    Scores mobile money adoption potential based on infrastructure and connectivity.
    """
    
    def __init__(self):
        pass
    
    def compute_mobile_money_score(self, infrastructure_data: Dict,
                                  population_data: Dict = None,
                                  nightlights_data: Dict = None) -> Dict:
        """
        Compute mobile money adoption potential score.
        
        Args:
            infrastructure_data: Infrastructure data
            population_data: Population data (optional)
            nightlights_data: Nightlights data (optional)
            
        Returns:
            Dictionary with mobile money metrics
        """
        print("Computing mobile money adoption potential")
        
        # Financial infrastructure score
        financial_infra = self._compute_financial_infrastructure(infrastructure_data)
        
        # Connectivity proxy (from nightlights and population)
        connectivity = self._estimate_connectivity(
            nightlights_data, 
            population_data
        )
        
        # Market access (indicator of economic activity)
        market_score = 0.5
        if 'nearest' in infrastructure_data:
            nearest_market = infrastructure_data['nearest'].get('market', {})
            if nearest_market.get('found', False):
                dist_km = nearest_market.get('distance_km', 50)
                market_score = np.exp(-dist_km / 10)
        
        # Overall mobile money score
        # Weighted combination of factors
        overall_score = (
            0.3 * financial_infra +
            0.4 * connectivity +
            0.3 * market_score
        )
        
        result = {
            'score': float(overall_score),
            'financial_infrastructure': float(financial_infra),
            'connectivity_proxy': float(connectivity),
            'market_access': float(market_score),
            'classification': self._classify_adoption(overall_score),
            'potential': self._assess_potential(overall_score)
        }
        
        # Add agent density if available
        amenity_counts = infrastructure_data.get('amenity_counts', {})
        if amenity_counts:
            result['agent_density'] = self._estimate_agent_density(amenity_counts)
        
        return result
    
    def _compute_financial_infrastructure(self, infrastructure_data: Dict) -> float:
        """
        Compute financial infrastructure score.
        
        Args:
            infrastructure_data: Infrastructure data
            
        Returns:
            Financial infrastructure score (0-1)
        """
        amenity_counts = infrastructure_data.get('amenity_counts', {})
        
        # Count financial service points
        banks = amenity_counts.get('banks', 0)
        total_amenities = amenity_counts.get('total', 1)
        
        # Financial service density
        density = amenity_counts.get('density_per_km2', 0)
        
        # Score based on presence and density
        if banks > 5:
            infra_score = 0.8
        elif banks > 2:
            infra_score = 0.6
        elif banks > 0:
            infra_score = 0.4
        else:
            infra_score = 0.1
        
        # Adjust for overall amenity density (proxy for connectivity)
        density_boost = min(density / 20, 0.2)
        
        return float(min(infra_score + density_boost, 1.0))
    
    def _estimate_connectivity(self, nightlights_data: Dict = None,
                              population_data: Dict = None) -> float:
        """
        Estimate connectivity from nightlights and population.
        
        Args:
            nightlights_data: Nightlights data
            population_data: Population data
            
        Returns:
            Connectivity score (0-1)
        """
        connectivity = 0.3  # Baseline
        
        # Nightlights as proxy for electricity/connectivity
        if nightlights_data:
            nl_score = nightlights_data.get('intensity_normalized', 0)
            connectivity += nl_score * 0.4
        
        # Population density (higher density = better infrastructure)
        if population_data:
            pop_density = population_data.get('population_density', 0)
            # Log scale normalization
            pop_score = min(np.log1p(pop_density) / np.log1p(5000), 1.0)
            connectivity += pop_score * 0.3
        
        return float(min(connectivity, 1.0))
    
    def _estimate_agent_density(self, amenity_counts: Dict) -> Dict:
        """
        Estimate mobile money agent density.
        
        Args:
            amenity_counts: Amenity counts
            
        Returns:
            Agent density metrics
        """
        # Mobile money agents often co-locate with shops, banks, pharmacies
        banks = amenity_counts.get('banks', 0)
        markets = amenity_counts.get('markets', 0)
        
        # Estimated agents (heuristic: banks + markets * 0.5)
        estimated_agents = banks + markets * 0.5
        
        density = amenity_counts.get('density_per_km2', 0)
        agent_density = estimated_agents / max(amenity_counts.get('total', 1), 1) * density
        
        return {
            'estimated_agents': float(estimated_agents),
            'agent_density_per_km2': float(agent_density),
            'classification': 'high' if agent_density > 2 else 'medium' if agent_density > 0.5 else 'low'
        }
    
    def _classify_adoption(self, score: float) -> str:
        """Classify mobile money adoption level."""
        if score > 0.7:
            return "high_adoption"
        elif score > 0.5:
            return "medium_adoption"
        elif score > 0.3:
            return "emerging"
        else:
            return "low_adoption"
    
    def _assess_potential(self, score: float) -> str:
        """Assess growth potential."""
        if score > 0.7:
            return "mature_market"
        elif score > 0.5:
            return "good_potential"
        elif score > 0.3:
            return "high_potential"
        else:
            return "developing_market"
    
    def compute_financial_inclusion_index(self, mobile_money_score: Dict,
                                         infrastructure_data: Dict) -> Dict:
        """
        Compute comprehensive financial inclusion index.
        
        Args:
            mobile_money_score: Mobile money score
            infrastructure_data: Infrastructure data
            
        Returns:
            Financial inclusion metrics
        """
        mm_score = mobile_money_score.get('score', 0)
        
        # Traditional banking access
        amenity_counts = infrastructure_data.get('amenity_counts', {})
        banks = amenity_counts.get('banks', 0)
        bank_access = min(banks / 5, 1.0)  # Normalize
        
        # Combined financial inclusion
        # Mobile money can compensate for lack of traditional banking
        inclusion_score = max(mm_score, bank_access)
        
        return {
            'financial_inclusion_score': float(inclusion_score),
            'mobile_money_component': float(mm_score),
            'banking_access_component': float(bank_access),
            'classification': self._classify_inclusion(inclusion_score)
        }
    
    def _classify_inclusion(self, score: float) -> str:
        """Classify financial inclusion level."""
        if score > 0.7:
            return "highly_included"
        elif score > 0.5:
            return "moderately_included"
        elif score > 0.3:
            return "partially_included"
        else:
            return "financially_excluded"


def compute_mobile_money_score(infrastructure_data: Dict,
                               population_data: Dict = None,
                               nightlights_data: Dict = None) -> Dict:
    """
    Convenience function to compute mobile money score.
    
    Args:
        infrastructure_data: Infrastructure data
        population_data: Optional population data
        nightlights_data: Optional nightlights data
        
    Returns:
        Dictionary with mobile money metrics
    """
    scorer = MobileMoneyScorer()
    
    # Compute main score
    result = scorer.compute_mobile_money_score(
        infrastructure_data,
        population_data,
        nightlights_data
    )
    
    # Add financial inclusion index
    inclusion = scorer.compute_financial_inclusion_index(
        result,
        infrastructure_data
    )
    result['financial_inclusion'] = inclusion
    
    return result
