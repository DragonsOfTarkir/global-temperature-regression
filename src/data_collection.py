#!/usr/bin/env python3
"""
Data Collection Script
Downloads data from NOAA, NASA GISS, and Our World in Data
"""

import requests
import os
from pathlib import Path

# Create data directory if not exists
data_dir = Path('data')
data_dir.mkdir(exist_ok=True)

# URLs for data sources
data_urls = {
    # NOAA Greenhouse Gases
    'co2_monthly': 'https://gml.noaa.gov/webdata/ccgg/trends/co2/co2_mm_mlo.txt',
    'ch4_monthly': 'https://gml.noaa.gov/webdata/ccgg/trends/ch4/ch4_mm_gl.txt',
    'n2o_monthly': 'https://gml.noaa.gov/webdata/ccgg/trends/n2o/n2o_mm_gl.txt',

    # NASA GISS Temperature
    'temperature_anomaly': 'https://data.giss.nasa.gov/gistemp/tabledata_v4/GLB.Ts+dSST.txt',

    # Solar Irradiance (NOAA)
    'solar_irradiance': 'https://www.ncei.noaa.gov/data/total-solar-irradiance/access/',

    # Our World in Data
    'co2_emissions': 'https://raw.githubusercontent.com/owid/co2-data/master/owid-co2-data.csv',
    'energy_consumption': 'https://raw.githubusercontent.com/owid/energy-data/master/owid-energy-data.csv',
    'land_use_emissions': 'https://raw.githubusercontent.com/owid/co2-data/master/owid-co2-data.csv'  # Same file has land use
}

def download_file(url, filename):
    """Download a file from URL to data directory"""
    try:
        response = requests.get(url)
        response.raise_for_status()
        filepath = data_dir / filename
        with open(filepath, 'wb') as f:
            f.write(response.content)
        print(f"Downloaded {filename}")
    except Exception as e:
        print(f"Error downloading {filename}: {e}")

if __name__ == "__main__":
    for name, url in data_urls.items():
        filename = f"{name}.txt" if not url.endswith('.csv') else f"{name}.csv"
        download_file(url, filename)