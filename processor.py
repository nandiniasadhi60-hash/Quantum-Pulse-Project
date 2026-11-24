
import polars as pl
import os

# Financial Data Processor

def load_data(file_path):
    """Load financial data from CSV."""
    if not os.path.exists(file_path):
        print("CSV file not found:", file_path)
        return pl.DataFrame()

    try:
        df = pl.read_csv(file_path)
        return df
    except Exception as e:
        print("Error loading data:", e)
        return pl.DataFrame()


def clean_data(df):
    """Clean financial data."""
    if df.is_empty():
        return df

    df = df.drop_nulls()

    return df


def calculate_statistics(df):
    """Calculate financial statistics."""
    if df.is_empty():
        return {}

    numeric_columns = [
        col for col, dtype in zip(df.columns, df.dtypes)
        if dtype.is_numeric()
    ]

    statistics = {}

    for col in numeric_columns:
        statistics[col] = {
            "mean": df[col].mean(),
            "max": df[col].max(),
            "min": df[col].min()
        }

    return statistics


def process_financial_data(file_path):
    """Complete financial data processing."""
    df = load_data(file_path)

    df = clean_data(df)

    statistics = calculate_statistics(df)

    return df, statistics
