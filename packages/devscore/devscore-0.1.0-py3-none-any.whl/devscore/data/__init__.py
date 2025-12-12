"""
Data collection modules initialization.
"""

from .satellite import get_satellite_features, SatelliteDataCollector
from .nightlights import get_nightlights, NightlightsCollector
from .osm import get_infrastructure_data, OSMDataCollector
from .worldpop import get_population_density, WorldPopCollector
from .dhs import load_dhs_training_data, DHSDataHandler

__all__ = [
    'get_satellite_features',
    'get_nightlights',
    'get_infrastructure_data',
    'get_population_density',
    'load_dhs_training_data',
    'SatelliteDataCollector',
    'NightlightsCollector',
    'OSMDataCollector',
    'WorldPopCollector',
    'DHSDataHandler',
]
