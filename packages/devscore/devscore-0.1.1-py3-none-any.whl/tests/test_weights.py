"""
Test suite for dynamic weighting methods.
Run with: pytest tests/test_weights.py -v
"""

import pytest
import numpy as np
import pandas as pd
from devscore.scoring.weights import (
    WeightCalculator,
    AHPWeightCalculator,
    determine_optimal_weights
)


class TestWeightCalculator:
    """Test dynamic weight calculation methods."""
    
    def test_equal_weights(self):
        """Test equal weighting method."""
        data = pd.DataFrame({
            'a': [1, 2, 3, 4, 5],
            'b': [2, 4, 6, 8, 10],
            'c': [1, 1, 1, 1, 1]
        })
        
        calculator = WeightCalculator()
        weights = calculator.calculate_weights(data, method='equal')
        
        # All weights should be equal
        assert len(weights) == 3
        assert all(abs(w - 1/3) < 0.001 for w in weights.values())
        assert abs(sum(weights.values()) - 1.0) < 0.001
    
    def test_entropy_weights(self):
        """Test entropy weighting method."""
        # Create data with controlled variation levels
        np.random.seed(42)
        data = pd.DataFrame({
            'high_variation': np.random.uniform(0, 1, 50),
            'low_variation': np.full(50, 0.5),  # Constant = zero variation
            'medium_variation': np.random.uniform(0.4, 0.6, 50)
        })
        
        calculator = WeightCalculator()
        weights = calculator.calculate_weights(data, method='entropy')
        
        # Check weights sum to 1
        assert abs(sum(weights.values()) - 1.0) < 0.001
        
        # High variation should have higher weight than constant (low variation)
        assert weights['high_variation'] > weights['low_variation']
        assert weights['medium_variation'] > weights['low_variation']
    
    def test_pca_weights(self):
        """Test PCA-based weighting."""
        np.random.seed(42)
        data = pd.DataFrame({
            'a': np.random.randn(100),
            'b': np.random.randn(100),
            'c': np.random.randn(100)
        })
        
        calculator = WeightCalculator()
        weights = calculator.calculate_weights(data, method='pca')
        
        # Check weights sum to 1
        assert abs(sum(weights.values()) - 1.0) < 0.001
        
        # All weights should be positive
        assert all(w > 0 for w in weights.values())
    
    def test_cv_weights(self):
        """Test coefficient of variation weighting."""
        data = pd.DataFrame({
            'stable': [5, 5.1, 4.9, 5, 5.1],  # Low CV
            'variable': [1, 5, 2, 8, 3]  # High CV
        })
        
        calculator = WeightCalculator()
        weights = calculator.calculate_weights(data, method='cv')
        
        # Variable should have higher weight
        assert weights['variable'] > weights['stable']
        assert abs(sum(weights.values()) - 1.0) < 0.001
    
    def test_critic_weights(self):
        """Test CRITIC weighting method."""
        np.random.seed(42)
        data = pd.DataFrame({
            'a': np.random.randn(50),
            'b': np.random.randn(50),
            'c': np.random.randn(50)
        })
        
        calculator = WeightCalculator()
        weights = calculator.calculate_weights(data, method='critic')
        
        # Check weights sum to 1
        assert abs(sum(weights.values()) - 1.0) < 0.001
        
        # All weights should be positive
        assert all(w > 0 for w in weights.values())
    
    def test_correlation_weights(self):
        """Test correlation-based weighting."""
        np.random.seed(42)
        # Create correlated and independent variables
        base = np.random.randn(100)
        data = pd.DataFrame({
            'correlated1': base + np.random.randn(100) * 0.1,
            'correlated2': base + np.random.randn(100) * 0.1,
            'independent': np.random.randn(100)
        })
        
        calculator = WeightCalculator()
        weights = calculator.calculate_weights(data, method='correlation')
        
        # Independent variable should have higher weight
        assert weights['independent'] > weights['correlated1']
        assert abs(sum(weights.values()) - 1.0) < 0.001
    
    def test_robust_weights(self):
        """Test robust weight averaging."""
        np.random.seed(42)
        data = pd.DataFrame({
            'a': np.random.randn(100),
            'b': np.random.randn(100),
            'c': np.random.randn(100)
        })
        
        calculator = WeightCalculator()
        weights = calculator.calculate_robust_weights(data)
        
        # Check weights sum to 1
        assert abs(sum(weights.values()) - 1.0) < 0.001
        
        # All weights should be positive
        assert all(w > 0 for w in weights.values())


class TestAHPWeightCalculator:
    """Test AHP weight calculation."""
    
    def test_ahp_consistent_matrix(self):
        """Test AHP with a consistent comparison matrix."""
        # Perfectly consistent matrix
        matrix = np.array([
            [1,   2,   4],
            [1/2, 1,   2],
            [1/4, 1/2, 1]
        ])
        
        calculator = AHPWeightCalculator()
        weights, cr = calculator.calculate_weights_from_matrix(matrix)
        
        # Check weights sum to 1
        assert abs(weights.sum() - 1.0) < 0.001
        
        # Consistency ratio should be very low for consistent matrix
        assert cr < 0.01
        
        # Weights should be in descending order
        assert weights[0] > weights[1] > weights[2]
    
    def test_ahp_development_weights(self):
        """Test AHP weights for development score components."""
        calculator = AHPWeightCalculator()
        weights = calculator.get_development_weights_ahp()
        
        # Check we have all 5 components
        assert len(weights) == 5
        assert 'poverty' in weights
        assert 'market_access' in weights
        assert 'infrastructure' in weights
        assert 'food_security' in weights
        assert 'mobile_money' in weights
        
        # Check weights sum to 1
        assert abs(sum(weights.values()) - 1.0) < 0.001
        
        # All weights should be positive
        assert all(w > 0 for w in weights.values())
        
        # Poverty should typically have highest weight in development context
        assert weights['poverty'] == max(weights.values())
    
    def test_ahp_custom_matrix(self):
        """Test AHP with custom priorities."""
        # Custom matrix emphasizing food security
        matrix = np.array([
            [1,   2,   2,   1/2, 3],
            [1/2, 1,   1,   1/3, 2],
            [1/2, 1,   1,   1/3, 2],
            [2,   3,   3,   1,   4],
            [1/3, 1/2, 1/2, 1/4, 1]
        ])
        
        calculator = AHPWeightCalculator()
        weights, cr = calculator.calculate_weights_from_matrix(matrix)
        
        # Food security (index 3) should have highest weight
        assert weights[3] == max(weights)
        
        # Check consistency
        assert cr < 0.15  # Allow some inconsistency for custom matrix


class TestDetermineOptimalWeights:
    """Test high-level weight determination function."""
    
    def test_determine_optimal_weights_entropy(self):
        """Test optimal weights with entropy method."""
        np.random.seed(42)
        component_scores = {
            'poverty': list(np.random.beta(2, 5, 30)),
            'market_access': list(np.random.beta(3, 3, 30)),
            'infrastructure': list(np.random.beta(4, 3, 30)),
            'food_security': list(np.random.uniform(0.3, 0.8, 30)),
            'mobile_money': list(np.random.beta(5, 2, 30))
        }
        
        weights = determine_optimal_weights(component_scores, method='entropy')
        
        # Check basic properties
        assert len(weights) == 5
        assert abs(sum(weights.values()) - 1.0) < 0.001
        assert all(w > 0 for w in weights.values())
    
    def test_determine_optimal_weights_auto(self):
        """Test optimal weights with auto method."""
        np.random.seed(42)
        component_scores = {
            'poverty': list(np.random.beta(2, 5, 50)),
            'market_access': list(np.random.beta(3, 3, 50)),
            'infrastructure': list(np.random.beta(4, 3, 50)),
            'food_security': list(np.random.uniform(0.3, 0.8, 50)),
            'mobile_money': list(np.random.beta(5, 2, 50))
        }
        
        weights = determine_optimal_weights(component_scores, method='auto')
        
        # Check basic properties
        assert len(weights) == 5
        assert abs(sum(weights.values()) - 1.0) < 0.001
        assert all(w > 0 for w in weights.values())
    
    def test_determine_optimal_weights_ahp(self):
        """Test optimal weights with AHP method."""
        component_scores = {
            'poverty': [0.5, 0.6, 0.7],
            'market_access': [0.6, 0.7, 0.8],
            'infrastructure': [0.7, 0.8, 0.9],
            'food_security': [0.4, 0.5, 0.6],
            'mobile_money': [0.8, 0.85, 0.9]
        }
        
        weights = determine_optimal_weights(component_scores, method='ahp')
        
        # AHP doesn't use data, so should return default AHP weights
        assert len(weights) == 5
        assert abs(sum(weights.values()) - 1.0) < 0.001
        assert weights['poverty'] == max(weights.values())
    
    def test_insufficient_data(self):
        """Test handling of insufficient data."""
        component_scores = {
            'poverty': [0.5, 0.6],
            'market_access': [0.6, 0.7],
            'infrastructure': [0.7, 0.8],
            'food_security': [0.4, 0.5],
            'mobile_money': [0.8, 0.85]
        }
        
        weights = determine_optimal_weights(component_scores, method='entropy')
        
        # Should fall back to equal weights
        assert len(weights) == 5
        assert abs(sum(weights.values()) - 1.0) < 0.001


class TestWeightIntegration:
    """Integration tests for weighting system."""
    
    def test_all_methods_produce_valid_weights(self):
        """Test that all methods produce valid weights."""
        np.random.seed(42)
        data = pd.DataFrame({
            'a': np.random.randn(100),
            'b': np.random.randn(100),
            'c': np.random.randn(100),
            'd': np.random.randn(100),
            'e': np.random.randn(100)
        })
        
        calculator = WeightCalculator()
        
        for method in calculator.methods:
            weights = calculator.calculate_weights(data, method=method)
            
            # All methods should produce valid weights
            assert len(weights) == 5, f"{method} failed: wrong number of weights"
            assert abs(sum(weights.values()) - 1.0) < 0.001, f"{method} failed: weights don't sum to 1"
            assert all(w >= 0 for w in weights.values()), f"{method} failed: negative weights"
            assert all(w <= 1 for w in weights.values()), f"{method} failed: weights > 1"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
