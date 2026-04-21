#!/usr/bin/env python3
"""
Data Preprocessing Script
Loads, cleans, and merges data from multiple sources
"""

import pandas as pd
import numpy as np
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

data_dir = Path('data')

def load_noaa_gas_data(filename, gas_name):
    """Load NOAA greenhouse gas data"""
    filepath = data_dir / filename
    if not filepath.exists():
        print(f"File {filename} not found")
        return pd.DataFrame()

    # Read the file, skip header lines starting with #
    df = pd.read_csv(filepath, sep='\s+', comment='#', header=None,
                     names=['year', 'month', 'decimal_date', 'average', 'trend', 'days', 'unc1', 'unc2'])

    df['date'] = pd.to_datetime(df[['year', 'month']].assign(day=1))
    df = df[['date', 'average']].rename(columns={'average': gas_name})
    df = df.set_index('date')
    return df

def load_nasa_temperature():
    filepath = data_dir / 'temperature_anomaly.txt'
    if not filepath.exists():
        print("Temperature file not found")
        return pd.DataFrame()

    records = []

    with open(filepath, 'r') as f:
        for line in f:
            parts = line.strip().split()

            # Skip non-data lines
            if len(parts) < 13:
                continue

            # First value must be a year
            if not parts[0].isdigit():
                continue

            year = int(parts[0])

            # Extract first 12 values after year (Jan–Dec)
            months = parts[1:13]

            for i, val in enumerate(months, start=1):
                try:
                    anomaly = float(val)
                except:
                    anomaly = np.nan

                date = pd.Timestamp(year=year, month=i, day=1)
                records.append((date, anomaly))

    df = pd.DataFrame(records, columns=['date', 'anomaly'])
    df = df.set_index('date').sort_index()

    return df

def load_solar_irradiance():
    import xarray as xr

    filepath = data_dir / 'tsi_v03r00_monthly.nc'

    if not filepath.exists():
        print("Solar irradiance file not found")
        return pd.DataFrame()

    ds = xr.open_dataset(filepath)

    print(ds)  # 👈 VERY useful to inspect structure

    # Convert to pandas
    df = ds.to_dataframe().reset_index()

    print(df.head())

    # You’ll need to adjust this depending on variable names
    # Common ones are: 'time', 'TSI', etc.

    if 'time' in df.columns:
        df['date'] = pd.to_datetime(df['time'])

    # Replace 'TSI' with actual column name after inspection
    value_col = [col for col in df.columns if col not in ['time', 'date']][0]

    df = df[['date', value_col]].rename(columns={value_col: 'irradiance'})
    df = df.set_index('date')

    return df

def load_owid_data(filename, value_col):
    """Load Our World in Data CSV"""
    filepath = data_dir / filename
    if not filepath.exists():
        print(f"File {filename} not found")
        return pd.DataFrame()

    df = pd.read_csv(filepath)
    # Assume country is 'World', Year is year
    df_world = df[df['country'] == 'World'].copy()
    df_world['date'] = pd.to_datetime(df_world['Year'], format='%Y')
    df_world = df_world[['date', value_col]].set_index('date')
    return df_world

def main():
    # Load all datasets
    co2_df = load_noaa_gas_data('co2_monthly.txt', 'co2_ppm')
    ch4_df = load_noaa_gas_data('ch4_monthly.txt', 'ch4_ppb')
    n2o_df = load_noaa_gas_data('n2o_monthly.txt', 'n2o_ppb')
    temp_df = load_nasa_temperature()
    solar_df = load_solar_irradiance()

    # OWID data - need to check actual column names
    # For now, assume some columns
    co2_emissions_df = load_owid_data('co2_emissions.csv', 'co2')
    energy_df = load_owid_data('energy_consumption.csv', 'primary_energy_consumption')
    land_use_df = load_owid_data('land_use_emissions.csv', 'land_use_change_co2')

    # Merge all dataframes
    dfs = [co2_df, ch4_df, n2o_df, temp_df, solar_df, co2_emissions_df, energy_df, land_use_df]
    merged_df = pd.concat(dfs, axis=1, join='outer')

    # Forward fill missing values for greenhouse gases (they change slowly)
    gas_cols = ['co2_ppm', 'ch4_ppb', 'n2o_ppb']
    merged_df[gas_cols] = merged_df[gas_cols].ffill()

    # Interpolate temperature anomalies
    merged_df['anomaly'] = merged_df['anomaly'].interpolate()

    # For other variables, fill with mean or drop
    merged_df = merged_df.dropna(thresh=len(merged_df.columns) * 0.5)  # Keep rows with at least 50% data

    # Feature engineering
    merged_df['time_since_baseline'] = (merged_df.index - merged_df.index.min()).days / 365.25

    # Growth rates
    for col in gas_cols:
        merged_df[f'{col}_growth_rate'] = merged_df[col].pct_change(12)  # Annual growth

    # Moving averages
    merged_df['co2_ma_12'] = merged_df['co2_ppm'].rolling(12).mean()
    merged_df['temp_ma_12'] = merged_df['anomaly'].rolling(12).mean()

    # Save processed data
    merged_df.to_csv(data_dir / 'processed_climate_data.csv')
    print(f"Processed data saved with {len(merged_df)} rows and {len(merged_df.columns)} columns")
    print("Sample data:")
    print(merged_df.head())

if __name__ == "__main__":
    main()