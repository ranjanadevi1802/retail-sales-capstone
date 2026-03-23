import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
import os
import warnings
warnings.filterwarnings('ignore')

sns.set_theme(style="whitegrid")
plt.rcParams['figure.dpi'] = 120
COLORS = sns.color_palette("Blues_d", 8)
os.makedirs('outputs', exist_ok=True)

def load_cleaned():
    df = pd.read_csv('data/cleaned_superstore.csv', parse_dates=['Order_Date', 'Ship_Date'])
    print(f"✅ Loaded: {df.shape}")
    return df

def plot_sales_trend(df):
    monthly = df.groupby(['Order_Year', 'Order_Month'])['Sales'].sum().reset_index()
    monthly['Period'] = pd.to_datetime(
        monthly['Order_Year'].astype(str) + '-' + monthly['Order_Month'].astype(str), format='%Y-%m')
    monthly = monthly.sort_values('Period')
    fig, ax = plt.subplots(figsize=(14, 5))
    ax.plot(monthly['Period'], monthly['Sales'], marker='o', color=COLORS[3], linewidth=2)
    ax.fill_between(monthly['Period'], monthly['Sales'], alpha=0.15, color=COLORS[3])
    ax.set_title('Monthly Sales Trend', fontsize=15, fontweight='bold')
    ax.set_xlabel('Month')
    ax.set_ylabel('Total Sales ($)')
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'${x:,.0f}'))
    plt.tight_layout()
    plt.savefig('outputs/01_monthly_sales_trend.png')
    plt.close()
    print("✅ Saved: 01_monthly_sales_trend.png")

def plot_sales_by_category(df):
    cat_sales = df.groupby('Category')['Sales'].sum().sort_values(ascending=False)
    fig, ax = plt.subplots(figsize=(8, 5))
    bars = ax.bar(cat_sales.index, cat_sales.values, color=COLORS[:len(cat_sales)], edgecolor='white')
    for bar in bars:
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 2000,
                f'${bar.get_height():,.0f}', ha='center', fontsize=10)
    ax.set_title('Total Sales by Category', fontsize=14, fontweight='bold')
    ax.set_ylabel('Sales ($)')
    plt.tight_layout()
    plt.savefig('outputs/02_sales_by_category.png')
    plt.close()
    print("✅ Saved: 02_sales_by_category.png")

def plot_sales_by_region(df):
    region_sales = df.groupby('Region')['Sales'].sum().sort_values(ascending=False)
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.pie(region_sales, labels=region_sales.index, autopct='%1.1f%%',
           colors=sns.color_palette("Blues", len(region_sales)), startangle=140)
    ax.set_title('Sales by Region', fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.savefig('outputs/03_sales_by_region.png')
    plt.close()
    print("✅ Saved: 03_sales_by_region.png")

def plot_profit_vs_sales(df):
    fig, ax = plt.subplots(figsize=(10, 6))
    segments = df['Segment'].unique()
    palette  = sns.color_palette("Set2", len(segments))
    for seg, color in zip(segments, palette):
        subset = df[df['Segment'] == seg]
        ax.scatter(subset['Sales'], subset['Profit'], alpha=0.4, s=20, label=seg, color=color)
    ax.axhline(0, color='red', linestyle='--', linewidth=0.8, label='Break-even')
    ax.set_title('Profit vs Sales by Segment', fontsize=14, fontweight='bold')
    ax.set_xlabel('Sales ($)')
    ax.set_ylabel('Profit ($)')
    ax.legend()
    plt.tight_layout()
    plt.savefig('outputs/04_profit_vs_sales.png')
    plt.close()
    print("✅ Saved: 04_profit_vs_sales.png")

def plot_seasonal_patterns(df):
    quarterly = df.groupby(['Order_Year', 'Order_Quarter'])['Sales'].sum().reset_index()
    fig, ax = plt.subplots(figsize=(10, 5))
    for year in quarterly['Order_Year'].unique():
        subset = quarterly[quarterly['Order_Year'] == year]
        ax.plot(subset['Order_Quarter'], subset['Sales'], marker='s', label=str(year), linewidth=2)
    ax.set_title('Quarterly Sales by Year', fontsize=14, fontweight='bold')
    ax.set_xlabel('Quarter')
    ax.set_ylabel('Sales ($)')
    ax.set_xticks([1, 2, 3, 4])
    ax.set_xticklabels(['Q1', 'Q2', 'Q3', 'Q4'])
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'${x:,.0f}'))
    ax.legend(title='Year')
    plt.tight_layout()
    plt.savefig('outputs/05_seasonal_patterns.png')
    plt.close()
    print("✅ Saved: 05_seasonal_patterns.png")

def plot_top_subcategories(df):
    sub_sales = df.groupby('Sub_Category')['Sales'].sum().sort_values(ascending=True).tail(10)
    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.barh(sub_sales.index, sub_sales.values, color=COLORS[2], edgecolor='white')
    for bar in bars:
        ax.text(bar.get_width() + 500, bar.get_y() + bar.get_height()/2,
                f'${bar.get_width():,.0f}', va='center', fontsize=9)
    ax.set_title('Top 10 Sub-Categories by Sales', fontsize=14, fontweight='bold')
    ax.set_xlabel('Sales ($)')
    plt.tight_layout()
    plt.savefig('outputs/06_top_subcategories.png')
    plt.close()
    print("✅ Saved: 06_top_subcategories.png")

def plot_discount_vs_profit(df):
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.scatter(df['Discount'], df['Profit'], alpha=0.3, s=15, color=COLORS[4])
    ax.axhline(0, color='red', linestyle='--', linewidth=0.8)
    ax.set_title('Discount vs Profit', fontsize=14, fontweight='bold')
    ax.set_xlabel('Discount Rate')
    ax.set_ylabel('Profit ($)')
    plt.tight_layout()
    plt.savefig('outputs/07_discount_vs_profit.png')
    plt.close()
    print("✅ Saved: 07_discount_vs_profit.png")

def plot_correlation_heatmap(df):
    num_cols = ['Sales', 'Quantity', 'Discount', 'Profit', 'Ship_Duration', 'Profit_Margin']
    corr = df[num_cols].corr()
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.heatmap(corr, annot=True, fmt='.2f', cmap='Blues', linewidths=0.5, ax=ax)
    ax.set_title('Correlation Heatmap', fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.savefig('outputs/08_correlation_heatmap.png')
    plt.close()
    print("✅ Saved: 08_correlation_heatmap.png")

if __name__ == "__main__":
    print("=" * 50)
    print(" PART 2A: EXPLORATORY DATA ANALYSIS")
    print("=" * 50)
    df = load_cleaned()
    plot_sales_trend(df)
    plot_sales_by_category(df)
    plot_sales_by_region(df)
    plot_profit_vs_sales(df)
    plot_seasonal_patterns(df)
    plot_top_subcategories(df)
    plot_discount_vs_profit(df)
    plot_correlation_heatmap(df)
    print("\n✅ Part 2A complete! Check your outputs/ folder for charts.")

