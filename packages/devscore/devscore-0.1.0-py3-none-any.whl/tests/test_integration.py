"""
Integration tests for devscore package.
Tests end-to-end data collection and scoring.
"""

import pytest
import numpy as np
from devscore.data import (
    get_satellite_features,
    get_nightlights,
    get_infrastructure_data,
    get_population_density
)
from devscore.scoring import (
    compute_poverty_score,
    compute_market_access_score,
    compute_infrastructure_score,
    compute_food_security_score,
    compute_mobile_money_score
)
from devscore import compute_development_score


class TestDataCollection:
    """Test actual data collection."""
    
    @pytest.fixture
    def test_location(self):
        """Test location: Nairobi, Kenya."""
        return -1.2921, 36.8219
    
    def test_satellite_features_collection(self, test_location):
        """Test satellite feature collection."""
        lat, lon = test_location
        features = get_satellite_features(lat, lon, buffer_km=1)
        
        assert isinstance(features, dict)
        assert 'ndvi' in features
        assert 'ndbi' in features
        assert 'buildup_index' in features
        
        # Check value ranges
        assert -1 <= features['ndvi'] <= 1
        assert -1 <= features['ndbi'] <= 1
        assert 0 <= features['buildup_index'] <= 1
    
    def test_nightlights_collection(self, test_location):
        """Test nightlights data collection."""
        lat, lon = test_location
        lights = get_nightlights(lat, lon, year=2023)
        
        assert isinstance(lights, dict)
        assert 'intensity' in lights
        assert 'intensity_normalized' in lights
        assert 'classification' in lights
        
        # Check value ranges
        assert lights['intensity'] >= 0
        assert 0 <= lights['intensity_normalized'] <= 1
        assert lights['classification'] in ['no_light', 'rural', 'suburban', 'urban', 'dense_urban']
    
    def test_infrastructure_collection(self, test_location):
        """Test infrastructure data collection."""
        lat, lon = test_location
        infra = get_infrastructure_data(lat, lon, dist=5000)
        
        assert isinstance(infra, dict)
        assert 'amenity_counts' in infra
        assert 'road_network' in infra
        assert 'nearest' in infra
        
        amenities = infra['amenity_counts']
        assert 'schools' in amenities
        assert 'health' in amenities
        assert 'markets' in amenities
        assert 'banks' in amenities
    
    def test_population_collection(self, test_location):
        """Test population data collection."""
        lat, lon = test_location
        pop = get_population_density(lat, lon, year=2020)
        
        assert isinstance(pop, dict)
        assert 'population_density' in pop
        assert 'classification' in pop
        
        # Check value
        assert pop['population_density'] >= 0
        assert pop['classification'] in ['very_low', 'low', 'medium', 'high', 'very_high']


class TestScoringCalculations:
    """Test scoring calculations."""
    
    @pytest.fixture
    def sample_data(self):
        """Create sample data for testing."""
        return {
            'satellite': {
                'ndvi': 0.4,
                'ndbi': 0.2,
                'buildup_index': 0.3,
                'vegetation_health': 'moderate_vegetation'
            },
            'nightlights': {
                'intensity': 50,
                'intensity_normalized': 0.5,
                'classification': 'suburban'
            },
            'infrastructure': {
                'amenity_counts': {
                    'schools': 5,
                    'health': 3,
                    'markets': 2,
                    'banks': 1,
                    'total': 11,
                    'density_per_km2': 5.0
                },
                'road_network': {
                    'total_length_km': 20,
                    'density_km_per_km2': 2.5,
                    'num_segments': 50
                },
                'nearest': {
                    'hospital': {'found': True, 'distance_m': 2000, 'distance_km': 2.0},
                    'school': {'found': True, 'distance_m': 1000, 'distance_km': 1.0},
                    'market': {'found': True, 'distance_m': 1500, 'distance_km': 1.5}
                }
            },
            'population': {
                'population_density': 500,
                'classification': 'medium'
            }
        }
    
    def test_poverty_score_calculation(self, sample_data):
        """Test poverty score calculation."""
        result = compute_poverty_score(sample_data)
        
        assert isinstance(result, dict)
        assert 'poverty_score' in result
        assert 'wealth_index' in result
        assert 'classification' in result
        
        # Check ranges
        assert 0 <= result['poverty_score'] <= 1
        assert 0 <= result['wealth_index'] <= 1
        assert result['poverty_score'] + result['wealth_index'] == pytest.approx(1.0, abs=0.01)
    
    def test_market_access_calculation(self, sample_data):
        """Test market access calculation."""
        result = compute_market_access_score(
            -1.2921, 36.8219,
            sample_data['infrastructure'],
            sample_data['population']
        )
        
        assert isinstance(result, dict)
        assert 'score' in result
        assert 'classification' in result
        
        # Check ranges
        assert 0 <= result['score'] <= 1
        assert result['classification'] in ['very_poor', 'poor', 'moderate', 'good', 'excellent']
    
    def test_infrastructure_score_calculation(self, sample_data):
        """Test infrastructure score calculation."""
        result = compute_infrastructure_score(
            sample_data['infrastructure'],
            sample_data['population'],
            buffer_km=5.0
        )
        
        assert isinstance(result, dict)
        assert 'overall_score' in result
        assert 'amenity_score' in result
        assert 'road_score' in result
        
        # Check ranges
        assert 0 <= result['overall_score'] <= 1
        assert 0 <= result['amenity_score'] <= 1
        assert 0 <= result['road_score'] <= 1
    
    def test_food_security_calculation(self, sample_data):
        """Test food security calculation."""
        result = compute_food_security_score(
            sample_data['satellite'],
            sample_data['population']
        )
        
        assert isinstance(result, dict)
        assert 'score' in result
        assert 'ndvi' in result
        assert 'classification' in result
        
        # Check ranges
        assert 0 <= result['score'] <= 1
        assert result['classification'] in ['food_secure', 'moderately_secure', 'at_risk', 'food_insecure']
    
    def test_mobile_money_calculation(self, sample_data):
        """Test mobile money score calculation."""
        result = compute_mobile_money_score(
            sample_data['infrastructure'],
            sample_data['population'],
            sample_data['nightlights']
        )
        
        assert isinstance(result, dict)
        assert 'score' in result
        assert 'classification' in result
        
        # Check ranges
        assert 0 <= result['score'] <= 1
        assert result['classification'] in ['low_adoption', 'emerging', 'medium_adoption', 'high_adoption']


class TestEndToEnd:
    """End-to-end integration tests."""
    
    def test_complete_development_score(self):
        """Test complete development score calculation."""
        # Test location: Nairobi
        lat, lon = -1.2921, 36.8219
        
        result = compute_development_score(lat, lon, buffer_km=5, year=2023)
        
        # Check structure
        assert isinstance(result, dict)
        assert 'overall' in result
        assert 'components' in result
        assert 'classification' in result
        assert 'detailed_results' in result
        
        # Check overall score
        assert 0 <= result['overall'] <= 1
        
        # Check components
        components = result['components']
        assert 'poverty' in components
        assert 'market_access' in components
        assert 'infrastructure' in components
        assert 'food_security' in components
        assert 'mobile_money' in components
        
        # All components should be in valid range
        for component, score in components.items():
            assert 0 <= score <= 1, f"{component} score out of range: {score}"
        
        # Check classification
        valid_classifications = [
            'underdeveloped', 'developing', 'moderately_developed',
            'well_developed', 'highly_developed'
        ]
        assert result['classification'] in valid_classifications
    
    def test_multiple_locations(self):
        """Test scoring multiple locations."""
        locations = [
            (-1.2921, 36.8219),  # Nairobi
            (0.0, 37.0),         # Central Kenya
        ]
        
        scores = []
        for lat, lon in locations:
            result = compute_development_score(lat, lon, buffer_km=3)
            scores.append(result['overall'])
            
            assert 0 <= result['overall'] <= 1
        
        # All scores should be valid
        assert len(scores) == len(locations)
        assert all(0 <= s <= 1 for s in scores)


class TestErrorHandling:
    """Test error handling and edge cases."""
    
    def test_invalid_coordinates(self):
        """Test handling of invalid coordinates."""
        from devscore.utils.geospatial import validate_coordinates
        
        assert validate_coordinates(100, 0) == False
        assert validate_coordinates(0, 200) == False
    
    def test_empty_data_handling(self):
        """Test handling of empty/missing data."""
        empty_data = {
            'satellite': {},
            'nightlights': {},
            'infrastructure': {},
            'population': {}
        }
        
        # Should not crash, return valid structure
        result = compute_poverty_score(empty_data)
        assert isinstance(result, dict)
        assert 'poverty_score' in result


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
