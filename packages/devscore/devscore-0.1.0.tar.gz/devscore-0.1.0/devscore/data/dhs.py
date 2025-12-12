"""
DHS (Demographic and Health Surveys) data handling module.
Loads and processes DHS wealth index data for poverty modeling.
"""

import os
import numpy as np
import pandas as pd
from typing import Dict, Optional, List
import warnings

warnings.filterwarnings('ignore')


class DHSDataHandler:
    """
    Handles DHS survey data for poverty prediction.
    DHS data must be pre-downloaded due to access restrictions.
    """
    
    def __init__(self, data_dir: str = "./data/dhs"):
        self.data_dir = data_dir
        os.makedirs(data_dir, exist_ok=True)
        
    def load_dhs_data(self, country: str, year: int) -> Optional[pd.DataFrame]:
        """
        Load pre-downloaded DHS survey data.
        
        Args:
            country: Country code (e.g., 'KE' for Kenya)
            year: Survey year
            
        Returns:
            DataFrame with DHS data or None
        """
        filename = f"DHS_{country}_{year}.csv"
        filepath = os.path.join(self.data_dir, filename)
        
        if not os.path.exists(filepath):
            print(f"DHS data not found: {filepath}")
            print("Please download DHS data from https://dhsprogram.com/")
            return None
        
        try:
            df = pd.read_csv(filepath)
            print(f"Loaded DHS data: {len(df)} records")
            return df
        except Exception as e:
            print(f"Error loading DHS data: {e}")
            return None
    
    def prepare_wealth_index_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Prepare DHS data for poverty modeling.
        
        Args:
            df: Raw DHS DataFrame
            
        Returns:
            Cleaned DataFrame with wealth index
        """
        # Expected columns (standardize based on DHS structure)
        required_cols = ['cluster_id', 'latitude', 'longitude', 'wealth_index']
        
        # Check if required columns exist
        missing = [col for col in required_cols if col not in df.columns]
        if missing:
            print(f"Warning: Missing columns: {missing}")
        
        # Clean data
        df = df.dropna(subset=['latitude', 'longitude'])
        
        # Normalize wealth index to 0-1 if needed
        if 'wealth_index' in df.columns:
            if df['wealth_index'].max() > 1:
                df['wealth_index_normalized'] = (
                    (df['wealth_index'] - df['wealth_index'].min()) /
                    (df['wealth_index'].max() - df['wealth_index'].min())
                )
            else:
                df['wealth_index_normalized'] = df['wealth_index']
        
        return df
    
    def get_wealth_categories(self, df: pd.DataFrame) -> Dict[str, int]:
        """
        Get distribution of wealth categories.
        
        Args:
            df: DHS DataFrame
            
        Returns:
            Dictionary with category counts
        """
        if 'wealth_quintile' not in df.columns:
            return {}
        
        categories = df['wealth_quintile'].value_counts().to_dict()
        return categories
    
    def create_training_dataset(self, dhs_df: pd.DataFrame, 
                               features_df: pd.DataFrame) -> pd.DataFrame:
        """
        Merge DHS data with satellite/geospatial features for training.
        
        Args:
            dhs_df: DHS survey data
            features_df: Satellite and geospatial features
            
        Returns:
            Merged training dataset
        """
        # Merge on lat/lon (with spatial tolerance)
        merged = pd.merge(
            dhs_df,
            features_df,
            on=['latitude', 'longitude'],
            how='inner'
        )
        
        print(f"Created training dataset: {len(merged)} samples")
        return merged
    
    def generate_synthetic_dhs_data(self, n_samples: int = 1000,
                                   region: str = 'kenya') -> pd.DataFrame:
        """
        Generate synthetic DHS-like data for testing.
        In production, use actual DHS data.
        
        Args:
            n_samples: Number of samples to generate
            region: Region name
            
        Returns:
            Synthetic DataFrame
        """
        print(f"Generating {n_samples} synthetic DHS samples for {region}")
        
        # Generate realistic coordinates for Kenya/East Africa
        np.random.seed(42)
        
        data = {
            'cluster_id': range(1, n_samples + 1),
            'latitude': np.random.uniform(-4.5, 4.5, n_samples),
            'longitude': np.random.uniform(34.0, 42.0, n_samples),
            'wealth_index': np.random.beta(2, 2, n_samples),  # Beta distribution 0-1
            'wealth_quintile': np.random.choice([1, 2, 3, 4, 5], n_samples),
            'urban_rural': np.random.choice(['urban', 'rural'], n_samples, p=[0.3, 0.7]),
            'household_size': np.random.randint(2, 12, n_samples),
            'education_years': np.random.randint(0, 16, n_samples),
        }
        
        df = pd.DataFrame(data)
        
        # Add some correlation with location
        # Urban areas (closer to 0, 36.8) have higher wealth
        df['distance_to_urban'] = np.sqrt(
            (df['latitude'] - 0) ** 2 + 
            (df['longitude'] - 36.8) ** 2
        )
        
        # Adjust wealth based on urbanization
        urban_boost = 0.3 * (1 - df['distance_to_urban'] / df['distance_to_urban'].max())
        df['wealth_index'] = np.clip(df['wealth_index'] + urban_boost, 0, 1)
        
        return df
    
    def save_dhs_data(self, df: pd.DataFrame, country: str, year: int):
        """
        Save DHS data to file.
        
        Args:
            df: DataFrame to save
            country: Country code
            year: Year
        """
        filename = f"DHS_{country}_{year}.csv"
        filepath = os.path.join(self.data_dir, filename)
        
        df.to_csv(filepath, index=False)
        print(f"Saved DHS data: {filepath}")
    
    def get_cluster_statistics(self, df: pd.DataFrame) -> Dict:
        """
        Compute statistics for DHS clusters.
        
        Args:
            df: DHS DataFrame
            
        Returns:
            Dictionary with statistics
        """
        stats = {
            'n_clusters': df['cluster_id'].nunique() if 'cluster_id' in df.columns else len(df),
            'n_observations': len(df),
            'mean_wealth_index': df['wealth_index'].mean() if 'wealth_index' in df.columns else None,
            'std_wealth_index': df['wealth_index'].std() if 'wealth_index' in df.columns else None,
            'urban_pct': (df['urban_rural'] == 'urban').mean() * 100 if 'urban_rural' in df.columns else None,
            'lat_range': (df['latitude'].min(), df['latitude'].max()),
            'lon_range': (df['longitude'].min(), df['longitude'].max())
        }
        
        return stats


def load_dhs_training_data(country: str = 'KE', year: int = 2020) -> pd.DataFrame:
    """
    Convenience function to load DHS training data.
    If not available, generates synthetic data.
    
    Args:
        country: Country code
        year: Survey year
        
    Returns:
        DataFrame with DHS data
    """
    handler = DHSDataHandler()
    
    # Try to load actual data
    df = handler.load_dhs_data(country, year)
    
    # If not available, generate synthetic data
    if df is None:
        print("Using synthetic DHS data for demonstration")
        df = handler.generate_synthetic_dhs_data()
    
    return handler.prepare_wealth_index_data(df)
