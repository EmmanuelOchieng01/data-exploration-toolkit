"""
Utility functions — save, export, and dataset info.
"""
import pandas as pd
import io

def save_clean(df, path):
    """Save cleaned DataFrame to CSV."""
    df.to_csv(path, index=False)

def to_csv_bytes(df):
    """Return DataFrame as CSV bytes for Streamlit download."""
    return df.to_csv(index=False).encode('utf-8')

def get_dataset_info(df):
    """Return a quick summary dict about the dataset."""
    return {
        'rows':         len(df),
        'columns':      len(df.columns),
        'numeric_cols': len(df.select_dtypes(include='number').columns),
        'text_cols':    len(df.select_dtypes(include='object').columns),
        'total_nulls':  int(df.isna().sum().sum()),
        'duplicates':   int(df.duplicated().sum()),
        'memory_kb':    round(df.memory_usage(deep=True).sum() / 1024, 1),
    }
