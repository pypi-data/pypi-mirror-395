"""
devscore: Development Score Calculator for Geographic Areas

A Python package for computing multi-dimensional development scores using
open geospatial, satellite, and survey-based indicators.
"""

__version__ = "0.1.0"
__author__ = "Your Name"
__email__ = "your.email@example.com"

from .scoring.final_score import compute_development_score, DevelopmentScoreCalculator
from .scoring import (
    compute_poverty_score,
    compute_market_access_score,
    compute_infrastructure_score,
    compute_food_security_score,
    compute_mobile_money_score
)

from .data import (
    get_satellite_features,
    get_nightlights,
    get_infrastructure_data,
    get_population_density,
    load_dhs_training_data
)

__all__ = [
    # Main function
    'compute_development_score',
    'DevelopmentScoreCalculator',
    # Component scores
    'compute_poverty_score',
    'compute_market_access_score',
    'compute_infrastructure_score',
    'compute_food_security_score',
    'compute_mobile_money_score',
    # Data collection
    'get_satellite_features',
    'get_nightlights',
    'get_infrastructure_data',
    'get_population_density',
    'load_dhs_training_data',
]
