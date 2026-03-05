import pandas as pd

def load_data(path):
    return pd.read_csv(path)

def clean_missing(df, strategy="mean"):
    for col in df.select_dtypes(include=['float', 'int']).columns:
        if strategy == "mean":
            df[col].fillna(df[col].mean(), inplace=True)
        elif strategy == "median":
            df[col].fillna(df[col].median(), inplace=True)
    df.fillna("Unknown", inplace=True)
    return df

def drop_duplicates(df):
    return df.drop_duplicates()
