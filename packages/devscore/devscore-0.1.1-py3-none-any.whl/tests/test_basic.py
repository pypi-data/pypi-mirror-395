"""
Test suite for devscore package.
Run with: pytest tests/
"""

import pytest
import numpy as np
from devscore.utils.geospatial import (
    haversine_distance,
    validate_coordinates,
    calculate_bbox
)
from devscore.utils.preprocessing import (
    normalize_features,
    handle_missing_values,
    clip_outliers
)


class TestGeospatialUtils:
    """Test geospatial utility functions."""
    
    def test_haversine_distance(self):
        """Test distance calculation between two points."""
        # Nairobi to Mombasa (approximate)
        lat1, lon1 = -1.2921, 36.8219  # Nairobi
        lat2, lon2 = -4.0435, 39.6682  # Mombasa
        
        distance = haversine_distance(lat1, lon1, lat2, lon2)
        
        # Should be approximately 440km
        assert 400000 < distance < 500000
    
    def test_validate_coordinates_valid(self):
        """Test coordinate validation with valid coordinates."""
        assert validate_coordinates(-1.2921, 36.8219) == True
        assert validate_coordinates(0, 0) == True
    
    def test_validate_coordinates_invalid(self):
        """Test coordinate validation with invalid coordinates."""
        assert validate_coordinates(91, 0) == False
        assert validate_coordinates(0, 181) == False
        assert validate_coordinates(-91, 0) == False
    
    def test_get_bounding_box(self):
        """Test bounding box calculation."""
        lat, lon = 0, 0
        bbox = calculate_bbox(lat, lon, buffer_km=10)
        
        min_lat, min_lon, max_lat, max_lon = bbox
        
        assert min_lat < lat < max_lat
        assert min_lon < lon < max_lon


class TestPreprocessingUtils:
    """Test preprocessing utility functions."""
    
    def test_normalize_features_minmax(self):
        """Test min-max normalization."""
        data = np.array([[1, 2], [3, 4], [5, 6]])
        normalized, scaler = normalize_features(data, method='minmax')
        
        assert normalized.min() == 0.0
        assert normalized.max() == 1.0
        assert normalized.shape == data.shape
    
    def test_normalize_features_standard(self):
        """Test standard normalization."""
        data = np.array([[1, 2], [3, 4], [5, 6]])
        normalized, scaler = normalize_features(data, method='standard')
        
        # Mean should be close to 0
        assert abs(normalized.mean()) < 0.1
        assert normalized.shape == data.shape
    
    def test_handle_missing_values(self):
        """Test missing value handling."""
        import pandas as pd
        
        df = pd.DataFrame({
            'a': [1, 2, np.nan, 4],
            'b': [5, np.nan, 7, 8]
        })
        
        # Test mean imputation
        df_filled = handle_missing_values(df, strategy='mean')
        assert df_filled.isna().sum().sum() == 0
        
        # Test zero imputation
        df_zero = handle_missing_values(df, strategy='zero')
        assert df_zero.isna().sum().sum() == 0
        assert df_zero.loc[2, 'a'] == 0
    
    def test_clip_outliers(self):
        """Test outlier clipping."""
        data = np.array([1, 2, 3, 4, 5, 100])  # 100 is outlier
        clipped = clip_outliers(data, n_std=2)
        
        # Outlier should be clipped
        assert clipped.max() < 100


class TestDataCollection:
    """Test data collection modules."""
    
    def test_satellite_features_import(self):
        """Test satellite module imports."""
        from devscore.data import get_satellite_features
        assert callable(get_satellite_features)
    
    def test_nightlights_import(self):
        """Test nightlights module imports."""
        from devscore.data import get_nightlights
        assert callable(get_nightlights)
    
    def test_infrastructure_import(self):
        """Test OSM module imports."""
        from devscore.data import get_infrastructure_data
        assert callable(get_infrastructure_data)
    
    def test_population_import(self):
        """Test population module imports."""
        from devscore.data import get_population_density
        assert callable(get_population_density)


class TestScoringModules:
    """Test scoring calculation modules."""
    
    def test_poverty_scorer_import(self):
        """Test poverty module imports."""
        from devscore.scoring import compute_poverty_score
        assert callable(compute_poverty_score)
    
    def test_market_access_import(self):
        """Test market access module imports."""
        from devscore.scoring import compute_market_access_score
        assert callable(compute_market_access_score)
    
    def test_infrastructure_scorer_import(self):
        """Test infrastructure scoring imports."""
        from devscore.scoring import compute_infrastructure_score
        assert callable(compute_infrastructure_score)
    
    def test_food_security_import(self):
        """Test food security module imports."""
        from devscore.scoring import compute_food_security_score
        assert callable(compute_food_security_score)
    
    def test_mobile_money_import(self):
        """Test mobile money module imports."""
        from devscore.scoring import compute_mobile_money_score
        assert callable(compute_mobile_money_score)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
