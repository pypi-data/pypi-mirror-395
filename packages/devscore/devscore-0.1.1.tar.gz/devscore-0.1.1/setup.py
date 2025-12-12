from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="devscore",
    version="0.1.1",
    author="Idriss Olivier Bado",
    author_email="idriss.bado@example.com",
    description="Automatically compute Development Score for any geographic area using open data",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/idrissbado/devscore",
    project_urls={
        "Bug Tracker": "https://github.com/idrissbado/devscore/issues",
        "Documentation": "https://github.com/idrissbado/devscore/blob/main/README.md",
        "Source Code": "https://github.com/idrissbado/devscore",
    },
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Developers",
        "Topic :: Scientific/Engineering :: GIS",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
    ],
    keywords="development economics poverty gis geospatial satellite remote-sensing machine-learning sdg",
    python_requires=">=3.8",
    install_requires=[
        "numpy>=1.21.0",
        "pandas>=1.3.0",
        "geopandas>=0.10.0",
        "rasterio>=1.2.0",
        "osmnx>=1.2.0",
        "scikit-learn>=1.0.0",
        "xgboost>=1.5.0",
        "requests>=2.26.0",
        "h3>=3.7.0",
        "shapely>=1.8.0",
        "pyproj>=3.2.0",
        "matplotlib>=3.4.0",
        "seaborn>=0.11.0",
    ],
    extras_require={
        "earthengine": ["earthengine-api>=0.1.300"],
        "dev": ["pytest>=7.0.0", "black>=22.0.0", "flake8>=4.0.0"],
    },
    package_data={
        "devscore": ["models/*.pkl", "data/*.geojson"],
    },
)
