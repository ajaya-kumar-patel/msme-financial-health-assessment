import joblib
import pandas as pd


def save_model(model, path):
    joblib.dump(model, path)


def load_model(path):
    return joblib.load(path)


def save_dataframe(df, path):
    df.to_csv(path, index=False)


def load_dataframe(path):
    return pd.read_csv(path)