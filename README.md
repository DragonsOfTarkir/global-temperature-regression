# Global Temperature Regression Analysis

This project builds a regression-based analytical pipeline to identify the most influential drivers of global temperature change. We collect data from multiple scientific sources, merge them, train regression models, and use feature importance to determine key environmental factors.

## Project Structure
- `data/`: Raw and processed datasets
- `src/`: Python scripts for data collection, preprocessing, and modeling
- `notebooks/`: Jupyter notebooks for analysis and visualization
- `reports/`: Final report and generated plots

## Data Sources
1. NOAA Global Monitoring Laboratory (CO₂, CH₄, N₂O)
2. NASA GISS (Temperature anomalies, Solar irradiance)
3. Our World in Data (Anthropogenic factors)

## Installation
```bash
pip install -r requirements.txt
```

## Usage

### Option 1: Run the complete pipeline
```bash
python src/main_pipeline.py
```

### Option 2: Run individual steps
```bash
python src/data_collection.py
python src/data_preprocessing.py
python src/model_training.py
python src/visualization.py
```

### Option 3: Interactive analysis
Open `notebooks/climate_analysis_report.ipynb` in Jupyter and run the cells.

## Results
- Model performance metrics
- Feature importance rankings
- Time series visualizations
- Correlation analysis

## Report
See `reports/final_report.md` for the complete analysis and findings.