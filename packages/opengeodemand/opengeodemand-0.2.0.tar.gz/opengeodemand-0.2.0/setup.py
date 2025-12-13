from setuptools import setup, find_packages

setup(
    name="opengeodemand",
    version="0.2.0",  
    description="Open Source Geospatial Demand Simulation Engine",
    author="Dipit & Usman",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "geopandas>=0.10",
        "pandas>=1.3",
        "numpy",
        "shapely",
        "osmnx>=1.9",
        "scikit-learn",  
        "seaborn",       
        "matplotlib",    
        "folium",        
        "mapclassify",
        "requests",
        "pyogrio"
    ],
    python_requires='>=3.8',
)