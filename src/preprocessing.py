import pandas as pd

def load_data(path):
    return pd.read_csv(path)

def clean_data(df):
    df = df.dropna()
    return df

def add_features(df):
    df["co2_growth"] = df["co2"].diff()
    df["temp_lag1"] = df["temperature"].shift(1)
    return df
