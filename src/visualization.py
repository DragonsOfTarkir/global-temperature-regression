#!/usr/bin/env python3
"""
Visualization Script
Creates plots for the climate analysis
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

data_dir = Path('data')
reports_dir = Path('reports')
reports_dir.mkdir(exist_ok=True)

# Set style
plt.style.use('seaborn-v0_8')
sns.set_palette('husl')

def load_processed_data():
    """Load the processed climate data"""
    filepath = data_dir / 'processed_climate_data.csv'
    df = pd.read_csv(filepath, index_col='date', parse_dates=True)
    return df

def plot_time_series(df):
    """Plot time series of key variables"""
    fig, axes = plt.subplots(3, 1, figsize=(12, 10), sharex=True)

    # Temperature anomaly
    axes[0].plot(df.index, df['anomaly'], color='red', linewidth=2)
    axes[0].set_title('Global Temperature Anomaly (°C)')
    axes[0].set_ylabel('Anomaly (°C)')
    axes[0].grid(True, alpha=0.3)

    # Greenhouse gases
    ax2 = axes[1]
    ax2.plot(df.index, df['co2_ppm'], label='CO₂ (ppm)', color='blue')
    ax2.set_ylabel('CO₂ (ppm)', color='blue')
    ax2.tick_params(axis='y', labelcolor='blue')
    ax2.grid(True, alpha=0.3)

    ax2_twin = ax2.twinx()
    ax2_twin.plot(df.index, df['ch4_ppb'], label='CH₄ (ppb)', color='green', linestyle='--')
    ax2_twin.set_ylabel('CH₄ (ppb)', color='green')
    ax2_twin.tick_params(axis='y', labelcolor='green')

    lines1, labels1 = ax2.get_legend_handles_labels()
    lines2, labels2 = ax2_twin.get_legend_handles_labels()
    ax2.legend(lines1 + lines2, labels1 + labels2, loc='upper left')

    # Solar irradiance and other factors
    ax3 = axes[2]
    if 'irradiance' in df.columns:
        ax3.plot(df.index, df['irradiance'], label='Solar Irradiance', color='orange')
    if 'Annual CO₂ emissions' in df.columns:
        ax3_twin = ax3.twinx()
        ax3_twin.plot(df.index, df['Annual CO₂ emissions'], label='CO₂ Emissions', color='purple', linestyle='--')
        ax3_twin.set_ylabel('CO₂ Emissions', color='purple')
        ax3_twin.tick_params(axis='y', labelcolor='purple')

    ax3.set_title('Solar Irradiance and CO₂ Emissions')
    ax3.set_xlabel('Year')
    ax3.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(reports_dir / 'time_series_analysis.png', dpi=300, bbox_inches='tight')
    plt.close()

def plot_correlations(df):
    """Plot correlation matrix"""
    # Select key variables
    key_vars = ['anomaly', 'co2_ppm', 'ch4_ppb', 'n2o_ppb']
    if 'irradiance' in df.columns:
        key_vars.append('irradiance')
    if 'Annual CO₂ emissions' in df.columns:
        key_vars.append('Annual CO₂ emissions')

    corr_df = df[key_vars].corr()

    plt.figure(figsize=(10, 8))
    sns.heatmap(corr_df, annot=True, cmap='coolwarm', center=0, fmt='.2f',
                square=True, cbar_kws={'shrink': 0.8})
    plt.title('Correlation Matrix of Climate Variables')
    plt.tight_layout()
    plt.savefig(reports_dir / 'correlation_matrix.png', dpi=300, bbox_inches='tight')
    plt.close()

def plot_scatter_top_features(df):
    """Plot scatter plots for top features vs temperature"""
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))

    # CO2 vs Temperature
    axes[0,0].scatter(df['co2_ppm'], df['anomaly'], alpha=0.6, color='blue')
    axes[0,0].set_xlabel('CO₂ (ppm)')
    axes[0,0].set_ylabel('Temperature Anomaly (°C)')
    axes[0,0].set_title('CO₂ vs Temperature Anomaly')
    axes[0,0].grid(True, alpha=0.3)

    # CH4 vs Temperature
    axes[0,1].scatter(df['ch4_ppb'], df['anomaly'], alpha=0.6, color='green')
    axes[0,1].set_xlabel('CH₄ (ppb)')
    axes[0,1].set_ylabel('Temperature Anomaly (°C)')
    axes[0,1].set_title('CH₄ vs Temperature Anomaly')
    axes[0,1].grid(True, alpha=0.3)

    # Solar irradiance vs Temperature
    if 'irradiance' in df.columns:
        axes[1,0].scatter(df['irradiance'], df['anomaly'], alpha=0.6, color='orange')
        axes[1,0].set_xlabel('Solar Irradiance (W/m²)')
        axes[1,0].set_ylabel('Temperature Anomaly (°C)')
        axes[1,0].set_title('Solar Irradiance vs Temperature Anomaly')
        axes[1,0].grid(True, alpha=0.3)

    # CO2 emissions vs Temperature
    if 'Annual CO₂ emissions' in df.columns:
        axes[1,1].scatter(df['Annual CO₂ emissions'], df['anomaly'], alpha=0.6, color='purple')
        axes[1,1].set_xlabel('Annual CO₂ Emissions')
        axes[1,1].set_ylabel('Temperature Anomaly (°C)')
        axes[1,1].set_title('CO₂ Emissions vs Temperature Anomaly')
        axes[1,1].grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(reports_dir / 'scatter_plots.png', dpi=300, bbox_inches='tight')
    plt.close()

def main():
    # Load data
    df = load_processed_data()
    print("Creating visualizations...")

    # Time series plots
    plot_time_series(df)

    # Correlation matrix
    plot_correlations(df)

    # Scatter plots
    plot_scatter_top_features(df)

    print("Visualizations saved to reports/ directory")

if __name__ == "__main__":
    main()