import pandas as pd
import numpy as np
import os
import warnings
warnings.filterwarnings('ignore')

def load_data(filepath='data/Sample - Superstore.csv'):
    df = pd.read_csv(filepath, encoding='latin-1')
    print(f"✅ Data loaded: {df.shape[0]} rows, {df.shape[1]} columns")
    print("\n--- Columns ---")
    print(df.columns.tolist())
    return df

def data_overview(df):
    print("\n===== DATA OVERVIEW =====")
    print(df.info())
    print("\n--- First 5 Rows ---")
    print(df.head())
    print("\n--- Missing Values ---")
    print(df.isnull().sum())
    print("\n--- Duplicates ---")
    print(f"Duplicates: {df.duplicated().sum()}")

def clean_data(df):
    print("\n===== DATA CLEANING =====")
    df = df.drop_duplicates()
    df['Order Date'] = pd.to_datetime(df['Order Date'])
    df['Ship Date']  = pd.to_datetime(df['Ship Date'])

    for col in df.select_dtypes(include='object').columns:
        df[col] = df[col].fillna('Unknown')
    for col in df.select_dtypes(include='number').columns:
        df[col] = df[col].fillna(df[col].median())

    df['Order Year']    = df['Order Date'].dt.year
    df['Order Month']   = df['Order Date'].dt.month
    df['Order Quarter'] = df['Order Date'].dt.quarter
    df['Ship Duration'] = (df['Ship Date'] - df['Order Date']).dt.days
    df['Profit Margin'] = (df['Profit'] / df['Sales']).round(4)
    df['Sales Normalized'] = (
        (df['Sales'] - df['Sales'].min()) /
        (df['Sales'].max() - df['Sales'].min())
    ).round(4)

    df.columns = [col.replace(' ', '_').replace('-', '_') for col in df.columns]
    print("✅ Cleaning complete. Shape:", df.shape)
    return df

def save_cleaned_data(df, output_path='data/cleaned_superstore.csv'):
    os.makedirs('data', exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"✅ Saved to '{output_path}'")

if __name__ == "__main__":
    print("=" * 50)
    print(" PART 1: DATA EXTRACTION & CLEANING")
    print("=" * 50)
    df_raw     = load_data()
    data_overview(df_raw)
    df_cleaned = clean_data(df_raw)
    save_cleaned_data(df_cleaned)
    print("\n✅ Part 1 complete!")
