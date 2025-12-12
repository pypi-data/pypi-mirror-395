"""
Poverty prediction module.
Machine learning-based poverty estimation using satellite and geospatial features.
"""

import os
import numpy as np
import pandas as pd
from typing import Dict, Optional, List
import pickle
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, r2_score
import warnings

warnings.filterwarnings('ignore')


class PovertyPredictor:
    """
    Predicts poverty levels using satellite imagery and geospatial features.
    Based on research from MIT Poverty Lab and similar studies.
    """
    
    def __init__(self, model_dir: str = "./models"):
        self.model_dir = model_dir
        os.makedirs(model_dir, exist_ok=True)
        self.model = None
        self.scaler = None
        self.feature_names = None
        
    def prepare_features(self, data: Dict) -> np.ndarray:
        """
        Prepare feature vector from collected data.
        
        Args:
            data: Dictionary with all collected features
            
        Returns:
            Feature array
        """
        features = []
        
        # Nightlights features
        if 'nightlights' in data:
            features.append(data['nightlights'].get('intensity_normalized', 0))
            features.append(data['nightlights'].get('intensity', 0))
        else:
            features.extend([0, 0])
        
        # Satellite features
        if 'satellite' in data:
            features.append(data['satellite'].get('ndvi', 0))
            features.append(data['satellite'].get('ndbi', 0))
            features.append(data['satellite'].get('buildup_index', 0))
        else:
            features.extend([0, 0, 0])
        
        # Population density
        if 'population' in data:
            features.append(np.log1p(data['population'].get('population_density', 0)))
        else:
            features.append(0)
        
        # Infrastructure density
        if 'infrastructure' in data:
            amenities = data['infrastructure'].get('amenity_counts', {})
            features.append(amenities.get('density_per_km2', 0))
            features.append(amenities.get('schools', 0))
            features.append(amenities.get('health', 0))
            
            roads = data['infrastructure'].get('road_network', {})
            features.append(roads.get('density_km_per_km2', 0))
        else:
            features.extend([0, 0, 0, 0])
        
        # Market access
        if 'market_access' in data:
            features.append(data['market_access'].get('score', 0))
        else:
            features.append(0)
        
        return np.array(features).reshape(1, -1)
    
    def train_model(self, X: np.ndarray, y: np.ndarray, 
                   model_type: str = 'random_forest') -> Dict:
        """
        Train poverty prediction model.
        
        Args:
            X: Feature matrix
            y: Target wealth index (0-1)
            model_type: 'random_forest' or 'gradient_boosting'
            
        Returns:
            Training metrics
        """
        print(f"Training {model_type} model on {len(X)} samples...")
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        # Scale features
        self.scaler = StandardScaler()
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        # Train model
        if model_type == 'random_forest':
            self.model = RandomForestRegressor(
                n_estimators=100,
                max_depth=10,
                min_samples_split=5,
                random_state=42,
                n_jobs=-1
            )
        elif model_type == 'gradient_boosting':
            self.model = GradientBoostingRegressor(
                n_estimators=100,
                max_depth=5,
                learning_rate=0.1,
                random_state=42
            )
        else:
            raise ValueError(f"Unknown model type: {model_type}")
        
        self.model.fit(X_train_scaled, y_train)
        
        # Evaluate
        y_pred_train = self.model.predict(X_train_scaled)
        y_pred_test = self.model.predict(X_test_scaled)
        
        metrics = {
            'train_rmse': np.sqrt(mean_squared_error(y_train, y_pred_train)),
            'test_rmse': np.sqrt(mean_squared_error(y_test, y_pred_test)),
            'train_r2': r2_score(y_train, y_pred_train),
            'test_r2': r2_score(y_test, y_pred_test),
            'model_type': model_type,
            'n_samples': len(X),
            'n_features': X.shape[1]
        }
        
        print(f"Model trained - Test R²: {metrics['test_r2']:.3f}, Test RMSE: {metrics['test_rmse']:.3f}")
        
        return metrics
    
    def predict(self, features: np.ndarray) -> float:
        """
        Predict wealth index from features.
        
        Args:
            features: Feature array
            
        Returns:
            Predicted wealth index (0-1, higher is wealthier)
        """
        if self.model is None:
            raise ValueError("Model not trained. Call train_model() first.")
        
        if self.scaler is not None:
            features = self.scaler.transform(features)
        
        prediction = self.model.predict(features)[0]
        
        # Clip to valid range
        return float(np.clip(prediction, 0, 1))
    
    def predict_poverty_score(self, data: Dict) -> Dict:
        """
        Predict poverty score from collected data.
        
        Args:
            data: Dictionary with all features
            
        Returns:
            Dictionary with poverty prediction
        """
        # Prepare features
        features = self.prepare_features(data)
        
        # If model not trained, use heuristic
        if self.model is None:
            score = self._heuristic_poverty_score(data)
        else:
            # Predict wealth index
            wealth_index = self.predict(features)
            # Convert to poverty score (invert: high wealth = low poverty)
            score = 1 - wealth_index
        
        return {
            'poverty_score': float(score),
            'wealth_index': float(1 - score),
            'classification': self._classify_poverty(score),
            'confidence': 0.75 if self.model else 0.5
        }
    
    def _heuristic_poverty_score(self, data: Dict) -> float:
        """
        Compute poverty score using heuristics when model not available.
        """
        score = 0.5  # Baseline
        
        # Nightlights (strong predictor)
        if 'nightlights' in data:
            nl_intensity = data['nightlights'].get('intensity_normalized', 0)
            score -= nl_intensity * 0.3  # High lights = less poverty
        
        # NDVI (vegetation/agriculture)
        if 'satellite' in data:
            ndvi = data['satellite'].get('ndvi', 0)
            if ndvi > 0.4:
                score -= 0.1  # Good vegetation = food security
        
        # Infrastructure
        if 'infrastructure' in data:
            amenities = data['infrastructure'].get('amenity_counts', {})
            density = amenities.get('density_per_km2', 0)
            score -= min(density / 100, 0.2)  # More amenities = less poverty
        
        # Population density (U-shaped: very low and very high correlated with poverty)
        if 'population' in data:
            pop_density = data['population'].get('population_density', 0)
            if pop_density < 50 or pop_density > 10000:
                score += 0.1
        
        return float(np.clip(score, 0, 1))
    
    def _classify_poverty(self, score: float) -> str:
        """Classify poverty level."""
        if score < 0.2:
            return "low_poverty"
        elif score < 0.4:
            return "moderate_poverty"
        elif score < 0.6:
            return "high_poverty"
        else:
            return "extreme_poverty"
    
    def save_model(self, filename: str = "poverty_model.pkl"):
        """Save trained model to disk."""
        if self.model is None:
            raise ValueError("No model to save")
        
        filepath = os.path.join(self.model_dir, filename)
        
        with open(filepath, 'wb') as f:
            pickle.dump({
                'model': self.model,
                'scaler': self.scaler,
                'feature_names': self.feature_names
            }, f)
        
        print(f"Model saved: {filepath}")
    
    def load_model(self, filename: str = "poverty_model.pkl"):
        """Load trained model from disk."""
        filepath = os.path.join(self.model_dir, filename)
        
        if not os.path.exists(filepath):
            print(f"Model file not found: {filepath}")
            return False
        
        with open(filepath, 'rb') as f:
            data = pickle.load(f)
            self.model = data['model']
            self.scaler = data['scaler']
            self.feature_names = data.get('feature_names')
        
        print(f"Model loaded: {filepath}")
        return True
    
    def get_feature_importance(self) -> Dict:
        """Get feature importance from trained model."""
        if self.model is None or not hasattr(self.model, 'feature_importances_'):
            return {}
        
        importances = self.model.feature_importances_
        
        feature_names = self.feature_names or [
            'nightlights_norm', 'nightlights_raw', 'ndvi', 'ndbi', 
            'buildup', 'log_population', 'amenity_density', 
            'schools', 'health', 'road_density', 'market_access'
        ]
        
        return dict(zip(feature_names, importances))


def compute_poverty_score(data: Dict) -> Dict:
    """
    Convenience function to compute poverty score.
    
    Args:
        data: Dictionary with all collected features
        
    Returns:
        Dictionary with poverty prediction
    """
    predictor = PovertyPredictor()
    
    # Try to load pre-trained model
    predictor.load_model()
    
    return predictor.predict_poverty_score(data)
