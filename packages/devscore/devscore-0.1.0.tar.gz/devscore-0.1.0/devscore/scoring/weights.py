"""
Dynamic weighting methods for development score components.
Implements multiple methods to determine optimal weights rather than using fixed values.
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Tuple
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA


class WeightCalculator:
    """
    Calculate dynamic weights for development score components using various methods.
    """
    
    def __init__(self):
        self.methods = [
            'equal',
            'entropy',
            'pca',
            'correlation',
            'cv',  # Coefficient of Variation
            'critic',  # CRITIC method
        ]
    
    def calculate_weights(self, data: pd.DataFrame, method: str = 'entropy') -> Dict[str, float]:
        """
        Calculate weights for indicators using specified method.
        
        Args:
            data: DataFrame with columns as indicators and rows as observations
            method: Weighting method ('equal', 'entropy', 'pca', 'correlation', 'cv', 'critic')
            
        Returns:
            Dictionary mapping indicator names to weights (sum = 1.0)
        """
        if method == 'equal':
            return self._equal_weights(data)
        elif method == 'entropy':
            return self._entropy_weights(data)
        elif method == 'pca':
            return self._pca_weights(data)
        elif method == 'correlation':
            return self._correlation_weights(data)
        elif method == 'cv':
            return self._cv_weights(data)
        elif method == 'critic':
            return self._critic_weights(data)
        else:
            raise ValueError(f"Unknown method: {method}. Available: {self.methods}")
    
    def _equal_weights(self, data: pd.DataFrame) -> Dict[str, float]:
        """Equal weights for all indicators."""
        n = len(data.columns)
        weight = 1.0 / n
        return {col: weight for col in data.columns}
    
    def _entropy_weights(self, data: pd.DataFrame) -> Dict[str, float]:
        """
        Entropy weighting method.
        Higher entropy = lower weight (less information content).
        
        Based on information theory - indicators with more variation carry more information.
        """
        # Normalize data to [0, 1]
        data_norm = (data - data.min()) / (data.max() - data.min() + 1e-10)
        
        # Replace zeros to avoid log(0)
        data_norm = data_norm.replace(0, 1e-10)
        
        n, m = data_norm.shape  # n=samples, m=indicators
        
        # Calculate probability matrix
        p = data_norm / data_norm.sum(axis=0)
        
        # Calculate entropy for each indicator
        entropy = -(1 / np.log(n)) * (p * np.log(p)).sum(axis=0)
        
        # Calculate diversity (1 - entropy)
        diversity = 1 - entropy
        
        # Calculate weights (normalize diversity)
        weights = diversity / diversity.sum()
        
        return {col: float(w) for col, w in zip(data.columns, weights)}
    
    def _pca_weights(self, data: pd.DataFrame) -> Dict[str, float]:
        """
        PCA-based weighting.
        Uses variance explained by first principal component.
        """
        # Standardize data
        scaler = StandardScaler()
        data_scaled = scaler.fit_transform(data)
        
        # Apply PCA
        pca = PCA(n_components=1)
        pca.fit(data_scaled)
        
        # Use absolute loadings as weights
        loadings = np.abs(pca.components_[0])
        
        # Normalize to sum to 1
        weights = loadings / loadings.sum()
        
        return {col: float(w) for col, w in zip(data.columns, weights)}
    
    def _correlation_weights(self, data: pd.DataFrame) -> Dict[str, float]:
        """
        Correlation-based weighting.
        Lower average correlation with other indicators = higher weight (more unique information).
        """
        # Calculate correlation matrix
        corr_matrix = data.corr().abs()
        
        # Calculate average correlation for each indicator (excluding self-correlation)
        avg_corr = (corr_matrix.sum(axis=0) - 1) / (len(data.columns) - 1)
        
        # Inverse correlation (lower correlation = higher weight)
        inverse_corr = 1 - avg_corr
        
        # Normalize
        weights = inverse_corr / inverse_corr.sum()
        
        return {col: float(w) for col, w in zip(data.columns, weights)}
    
    def _cv_weights(self, data: pd.DataFrame) -> Dict[str, float]:
        """
        Coefficient of Variation (CV) weighting.
        Higher variability = higher weight (more discriminating power).
        """
        # Calculate coefficient of variation for each indicator
        cv = data.std() / (data.mean().abs() + 1e-10)
        
        # Handle negative or NaN values
        cv = cv.fillna(0).abs()
        
        # Normalize
        if cv.sum() > 0:
            weights = cv / cv.sum()
        else:
            # Fallback to equal weights if all CVs are zero
            weights = pd.Series(1.0 / len(data.columns), index=data.columns)
        
        return {col: float(w) for col, w in zip(data.columns, weights)}
    
    def _critic_weights(self, data: pd.DataFrame) -> Dict[str, float]:
        """
        CRITIC (CRiteria Importance Through Intercriteria Correlation) method.
        Combines standard deviation with correlation structure.
        
        Higher weight for indicators with:
        - High variability (high std)
        - Low correlation with others (unique information)
        """
        # Normalize data to [0, 1]
        data_norm = (data - data.min()) / (data.max() - data.min() + 1e-10)
        
        # Calculate standard deviation
        std = data_norm.std()
        
        # Calculate correlation matrix
        corr_matrix = data_norm.corr().abs()
        
        # Calculate conflict (sum of 1 - correlation)
        conflict = (1 - corr_matrix).sum(axis=0) - 1  # Subtract 1 for self-correlation
        
        # CRITIC score = std * conflict
        critic_score = std * conflict
        
        # Normalize
        weights = critic_score / critic_score.sum()
        
        return {col: float(w) for col, w in zip(data.columns, weights)}
    
    def calculate_robust_weights(self, data: pd.DataFrame, 
                                 methods: List[str] = None) -> Dict[str, float]:
        """
        Calculate robust weights by averaging multiple methods.
        
        Args:
            data: DataFrame with indicators
            methods: List of methods to use (default: ['entropy', 'pca', 'critic'])
            
        Returns:
            Dictionary of averaged weights
        """
        if methods is None:
            methods = ['entropy', 'pca', 'critic']
        
        # Calculate weights using each method
        all_weights = []
        for method in methods:
            try:
                weights = self.calculate_weights(data, method)
                all_weights.append(pd.Series(weights))
            except Exception as e:
                print(f"Warning: {method} failed with error: {e}")
                continue
        
        if not all_weights:
            # Fallback to equal weights
            return self._equal_weights(data)
        
        # Average weights across methods
        avg_weights = pd.concat(all_weights, axis=1).mean(axis=1)
        
        # Normalize to ensure sum = 1
        avg_weights = avg_weights / avg_weights.sum()
        
        return avg_weights.to_dict()


class AHPWeightCalculator:
    """
    Analytical Hierarchy Process (AHP) for expert-based weighting.
    Useful when historical data is limited but expert knowledge is available.
    """
    
    def __init__(self):
        self.consistency_threshold = 0.1
    
    def calculate_weights_from_matrix(self, comparison_matrix: np.ndarray) -> Tuple[Dict[str, float], float]:
        """
        Calculate weights from pairwise comparison matrix using AHP.
        
        Args:
            comparison_matrix: n×n matrix where element (i,j) represents 
                             importance of criterion i relative to j
                             Scale: 1=equal, 3=moderate, 5=strong, 7=very strong, 9=extreme
            
        Returns:
            Tuple of (weights dict, consistency ratio)
        """
        n = comparison_matrix.shape[0]
        
        # Calculate eigenvalues and eigenvectors
        eigenvalues, eigenvectors = np.linalg.eig(comparison_matrix)
        
        # Find principal eigenvector (corresponds to largest eigenvalue)
        max_eigenvalue_idx = np.argmax(eigenvalues.real)
        principal_eigenvector = eigenvectors[:, max_eigenvalue_idx].real
        
        # Normalize to get weights
        weights = principal_eigenvector / principal_eigenvector.sum()
        
        # Calculate consistency ratio
        lambda_max = eigenvalues[max_eigenvalue_idx].real
        ci = (lambda_max - n) / (n - 1)  # Consistency Index
        
        # Random Index (RI) values for different matrix sizes
        ri_values = {1: 0, 2: 0, 3: 0.58, 4: 0.90, 5: 1.12, 6: 1.24, 
                    7: 1.32, 8: 1.41, 9: 1.45, 10: 1.49}
        ri = ri_values.get(n, 1.49)
        
        cr = ci / ri if ri > 0 else 0  # Consistency Ratio
        
        return weights, cr
    
    def get_development_weights_ahp(self, expert_matrix: np.ndarray = None) -> Dict[str, float]:
        """
        Get weights for development score components using AHP.
        
        Args:
            expert_matrix: 5×5 comparison matrix for [poverty, market_access, 
                          infrastructure, food_security, mobile_money]
                          If None, uses default research-based matrix
                          
        Returns:
            Dictionary of weights
        """
        components = ['poverty', 'market_access', 'infrastructure', 
                     'food_security', 'mobile_money']
        
        if expert_matrix is None:
            # Default matrix based on development economics literature
            # Poverty is most important, followed by infrastructure and market access
            expert_matrix = np.array([
                [1,   3,   2,   4,   5],  # poverty vs others
                [1/3, 1,   1,   2,   3],  # market_access vs others
                [1/2, 1,   1,   2,   3],  # infrastructure vs others
                [1/4, 1/2, 1/2, 1,   2],  # food_security vs others
                [1/5, 1/3, 1/3, 1/2, 1],  # mobile_money vs others
            ])
        
        weights, cr = self.calculate_weights_from_matrix(expert_matrix)
        
        if cr > self.consistency_threshold:
            print(f"Warning: Consistency ratio {cr:.3f} exceeds threshold {self.consistency_threshold}")
            print("Matrix may be inconsistent. Consider revising pairwise comparisons.")
        
        return {comp: float(w) for comp, w in zip(components, weights)}


def determine_optimal_weights(component_scores: Dict[str, List[float]], 
                             method: str = 'auto') -> Dict[str, float]:
    """
    Determine optimal weights from historical component scores.
    
    Args:
        component_scores: Dictionary mapping component names to lists of historical scores
                         Example: {'poverty': [0.5, 0.6, ...], 'market_access': [0.7, 0.8, ...]}
        method: Weighting method ('auto', 'entropy', 'pca', 'critic', 'ahp', etc.)
        
    Returns:
        Dictionary of optimal weights
    """
    # Convert to DataFrame
    df = pd.DataFrame(component_scores)
    
    # Remove any rows with missing values
    df = df.dropna()
    
    if len(df) < 5:
        print("Warning: Insufficient data for reliable weight estimation. Using equal weights.")
        calculator = WeightCalculator()
        return calculator._equal_weights(df)
    
    calculator = WeightCalculator()
    
    if method == 'auto':
        # Use robust averaging of multiple methods
        weights = calculator.calculate_robust_weights(df, methods=['entropy', 'critic', 'pca'])
    elif method == 'ahp':
        ahp_calc = AHPWeightCalculator()
        weights = ahp_calc.get_development_weights_ahp()
    else:
        weights = calculator.calculate_weights(df, method)
    
    return weights
