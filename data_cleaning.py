"""
Data cleaning — handles missing values, duplicates, and type inference.
"""
import pandas as pd

def load_data(file):
    """Load CSV or Excel from a file path or file-like object."""
    if hasattr(file, 'name'):
        name = file.name.lower()
    else:
        name = str(file).lower()
    if name.endswith('.csv'):
        return pd.read_csv(file)
    elif name.endswith(('.xlsx', '.xls')):
        return pd.read_excel(file)
    else:
        return pd.read_csv(file)

def clean_missing(df, strategy='mean'):
    """
    Fill missing values in numeric columns using mean or median.
    Fills remaining nulls with 'Unknown'.
    Returns cleaned df and a report dict.
    """
    report = {}
    numeric_cols = df.select_dtypes(include=['float64','int64']).columns
    for col in numeric_cols:
        n = df[col].isna().sum()
        if n > 0:
            fill = df[col].mean() if strategy == 'mean' else df[col].median()
            df[col] = df[col].fillna(fill)
            report[col] = {'filled': int(n), 'strategy': strategy, 'fill_value': round(fill, 4)}
    before = df.isna().sum().sum()
    df = df.fillna('Unknown')
    report['_text_filled'] = int(before)
    return df, report

def drop_duplicates(df):
    before = len(df)
    df = df.drop_duplicates()
    return df, before - len(df)

def get_quality_report(df):
    """Return per-column data quality metrics."""
    rows = len(df)
    report = []
    for col in df.columns:
        null_count = int(df[col].isna().sum())
        report.append({
            'column':       col,
            'dtype':        str(df[col].dtype),
            'nulls':        null_count,
            'null_pct':     round(null_count / rows * 100, 1) if rows else 0,
            'unique':       int(df[col].nunique()),
            'unique_pct':   round(df[col].nunique() / rows * 100, 1) if rows else 0,
        })
    return report
