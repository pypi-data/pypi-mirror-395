# devscore 🌍

**devscore** is a Python package that computes a multi-dimensional Development Score using open geospatial, satellite, and survey-based indicators. It is inspired by cutting-edge development economics research from MIT, Oxford, and the World Bank.

It helps researchers, governments, and NGOs estimate local well-being and market access for any region in Africa.

## Features

- **Poverty Prediction**: ML-based poverty estimation using satellite imagery, nightlights, and infrastructure data
- **Market Access**: Distance and travel time calculations to economic centers, markets, and key services
- **Infrastructure Mapping**: Density analysis of schools, hospitals, roads, and financial services from OSM
- **Food Security Assessment**: NDVI-based vegetation and agricultural productivity analysis
- **Night-time Lights**: Economic activity proxy using VIIRS satellite data
- **Mobile Money Potential**: Financial inclusion indicators

## Installation

```bash
pip install devscore
```

### Anaconda/Conda Installation (Recommended)

For better compatibility with geospatial dependencies, especially on Windows:

```bash
conda create -n devscore python=3.10 -y
conda activate devscore
conda install -c conda-forge geopandas rasterio osmnx scikit-learn xgboost -y
pip install h3 earthengine-api devscore
```

See [CONDA_INSTALLATION.md](CONDA_INSTALLATION.md) for detailed conda setup instructions.

### Install from Source

```bash
git clone https://github.com/idrissbado/devscore.git
cd devscore
pip install -e .
```

## Dependencies

```bash
pip install numpy pandas geopandas rasterio earthengine-api osmnx scikit-learn xgboost requests h3 shapely
```

## Quick Start

```python
from devscore import compute_development_score

# Compute development score for a location
lat, lon = -1.2921, 36.8219  # Nairobi, Kenya
score = compute_development_score(lat, lon)

print(f"Development Score: {score['overall']:.3f}")
print(f"  - Poverty Score: {score['poverty']:.3f}")
print(f"  - Market Access: {score['market_access']:.3f}")
print(f"  - Infrastructure: {score['infrastructure']:.3f}")
print(f"  - Food Security: {score['food_security']:.3f}")
print(f"  - Mobile Money: {score['mobile_money']:.3f}")
```

### Using Dynamic Weights

Instead of fixed weights, use data-driven or expert-based methods:

```python
from devscore.scoring.final_score import DevelopmentScoreCalculator

# Method 1: AHP (Analytical Hierarchy Process) - Expert-based
calculator = DevelopmentScoreCalculator(weight_method='ahp')
result = calculator.compute_development_score(lat, lon)

# Method 2: Entropy - Data-driven, based on variation
calculator = DevelopmentScoreCalculator(weight_method='entropy')

# Method 3: Auto - Robust average of multiple methods
calculator = DevelopmentScoreCalculator(weight_method='auto')

# Method 4: Custom weights
custom_weights = {
    'poverty': 0.40,
    'market_access': 0.25,
    'infrastructure': 0.20,
    'food_security': 0.10,
    'mobile_money': 0.05
}
calculator = DevelopmentScoreCalculator(custom_weights=custom_weights)
```

See `examples/dynamic_weights.py` for comprehensive examples.

## Data Sources

All data sources are open and freely accessible:

- **Satellite Imagery**: Sentinel-2 (AWS Open Data), Landsat 8/9
- **Night-time Lights**: NOAA VIIRS DNB
- **Infrastructure**: OpenStreetMap via OSMnx
- **Population**: WorldPop
- **Wealth Data**: DHS (Demographic and Health Surveys)

## Methodology

The package implements a weighted aggregation of five key development indicators.

**Weighting Methods:**

The package supports multiple approaches to determine indicator weights:

1. **Fixed Weights** (Legacy): Traditional research-based weights
2. **AHP (Analytical Hierarchy Process)**: Expert judgment-based (default)
3. **Entropy Method**: Data-driven, based on information content
4. **PCA (Principal Component Analysis)**: Variance-based weighting
5. **CRITIC**: Combines variability and correlation structure
6. **Auto**: Robust average of multiple methods

**Default AHP Formula:**
```
Development Score = w₁ × Poverty + w₂ × Market Access + 
                   w₃ × Infrastructure + w₄ × Food Security + 
                   w₅ × Mobile Money
```

Where weights (w) are determined using AHP based on development economics research consensus. For fixed weights: w₁=0.35, w₂=0.20, w₃=0.20, w₄=0.15, w₅=0.10.

Each component is normalized to a 0-1 scale where 1 indicates highest development.

### Components

1. **Poverty Score**: Machine learning model trained on DHS wealth index, using features like nightlights, NDVI, built-up area, population density, and road density

2. **Market Access**: Exponential decay function based on distance to markets, roads, hospitals, and economic centers

3. **Infrastructure Index**: Density of amenities (schools, clinics, markets, banks) per km²

4. **Food Security**: NDVI-based vegetation health indicator

5. **Mobile Money**: Financial inclusion proxy based on agent density and connectivity

## Research Background

This package is inspired by academic research from:

- World Bank Development Economics (DEC)
- MIT Poverty Lab
- Oxford Centre for the Study of African Economies (CSAE)
- LSE International Growth Centre (IGC)
- Harvard Growth Lab
- Nature papers on satellite-based poverty prediction

**Read the full methodology paper:** [PAPER.md](PAPER.md) - A comprehensive article explaining the theoretical framework, algorithms, validation results, and practical applications.

## Citation

If you use this package in your research, please cite:

```bibtex
@software{devscore2025,
  title={DevScore: An Open-Source Framework for Multi-Dimensional Development Assessment Using Geospatial Data},
  author={Bado, Idriss Olivier},
  year={2025},
  url={https://github.com/idrissbado/devscore}
}
```

## License

MIT License

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

## Acknowledgments

Thanks to the open data community and organizations providing free access to geospatial data for development research.
