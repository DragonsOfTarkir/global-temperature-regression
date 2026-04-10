#!/usr/bin/env python3
"""
Model Development Script
Trains regression models to predict temperature anomaly
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
import xgboost as xgb
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

data_dir = Path('data')
reports_dir = Path('reports')
reports_dir.mkdir(exist_ok=True)

def load_processed_data():
    """Load the processed climate data"""
    filepath = data_dir / 'processed_climate_data.csv'
    df = pd.read_csv(filepath, index_col='date', parse_dates=True)
    return df

def prepare_features_target(df):
    """Prepare features and target for modeling"""
    # Drop rows with missing target
    df = df.dropna(subset=['anomaly'])

    # Features: all columns except anomaly
    feature_cols = [col for col in df.columns if col != 'anomaly']
    X = df[feature_cols]
    y = df['anomaly']

    # Fill missing features with mean
    X = X.fillna(X.mean())

    return X, y

def train_models(X_train, X_test, y_train, y_test):
    """Train multiple regression models"""
    models = {
        'Linear Regression': LinearRegression(),
        'Random Forest': RandomForestRegressor(n_estimators=100, random_state=42),
        'XGBoost': xgb.XGBRegressor(n_estimators=100, random_state=42)
    }

    results = {}

    for name, model in models.items():
        # Train
        model.fit(X_train, y_train)

        # Predict
        y_pred_train = model.predict(X_train)
        y_pred_test = model.predict(X_test)

        # Metrics
        mse_train = mean_squared_error(y_train, y_pred_train)
        mse_test = mean_squared_error(y_test, y_pred_test)
        r2_train = r2_score(y_train, y_pred_train)
        r2_test = r2_score(y_test, y_pred_test)

        results[name] = {
            'model': model,
            'mse_train': mse_train,
            'mse_test': mse_test,
            'r2_train': r2_train,
            'r2_test': r2_test,
            'y_pred_test': y_pred_test
        }

        print(f"{name}:")
        print(".4f")
        print(".4f")
        print()

    return results

def plot_feature_importance(model, feature_names, model_name):
    """Plot feature importance for tree-based models"""
    if hasattr(model, 'feature_importances_'):
        importances = model.feature_importances_
        indices = np.argsort(importances)[::-1]

        plt.figure(figsize=(10, 6))
        plt.title(f'Feature Importances - {model_name}')
        plt.bar(range(len(importances)), importances[indices])
        plt.xticks(range(len(importances)), [feature_names[i] for i in indices], rotation=45, ha='right')
        plt.tight_layout()
        plt.savefig(reports_dir / f'feature_importance_{model_name.lower().replace(" ", "_")}.png')
        plt.close()

def plot_coefficients(model, feature_names):
    """Plot standardized coefficients for linear regression"""
    if hasattr(model, 'coef_'):
        coef = model.coef_
        indices = np.argsort(np.abs(coef))[::-1]

        plt.figure(figsize=(10, 6))
        plt.title('Standardized Coefficients - Linear Regression')
        plt.bar(range(len(coef)), coef[indices])
        plt.xticks(range(len(coef)), [feature_names[i] for i in indices], rotation=45, ha='right')
        plt.tight_layout()
        plt.savefig(reports_dir / 'linear_regression_coefficients.png')
        plt.close()

def main():
    # Load data
    df = load_processed_data()
    print(f"Loaded data with {len(df)} samples")

    # Prepare features and target
    X, y = prepare_features_target(df)
    print(f"Features: {list(X.columns)}")
    print(f"Target: temperature anomaly")

    # Train/test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42, shuffle=False)

    # Train models
    results = train_models(X_train, X_test, y_train, y_test)

    # Feature importance plots
    for name, result in results.items():
        if name in ['Random Forest', 'XGBoost']:
            plot_feature_importance(result['model'], list(X.columns), name)

    # Coefficients for linear regression
    plot_coefficients(results['Linear Regression']['model'], list(X.columns))

    # Save results
    results_df = pd.DataFrame({
        model: {
            'MSE_Train': res['mse_train'],
            'MSE_Test': res['mse_test'],
            'R2_Train': res['r2_train'],
            'R2_Test': res['r2_test']
        } for model, res in results.items()
    }).T

    results_df.to_csv(reports_dir / 'model_results.csv')
    print("Model results saved to reports/model_results.csv")

if __name__ == "__main__":
    main()