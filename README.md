# 🛒 Retail Sales Analysis & Forecasting
### Capstone Project 1
**Tools: Python · SQL · Power BI**

---

## 📌 Project Overview
End-to-end retail sales analytics on the Superstore Sales dataset covering:
- Data extraction and cleaning with Python (Pandas)
- SQL-based analysis with GROUP BY, JOINs, and subqueries
- Exploratory Data Analysis with Matplotlib & Seaborn
- Sales Forecasting using ARIMA and Facebook Prophet
- Interactive Dashboards in Power BI

---

## 📁 Project Structure
```
retail-sales-capstone/
├── data/
│   ├── cleaned_superstore.csv
├── sql/
│   └── retail_sales_queries.sql
├── outputs/
│   ├── 01_monthly_sales_trend.png
│   ├── 02_sales_by_category.png
│   ├── 03_sales_by_region.png
│   ├── 04_profit_vs_sales.png
│   ├── 05_seasonal_patterns.png
│   ├── 06_top_subcategories.png
│   ├── 07_discount_vs_profit.png
│   ├── 08_correlation_heatmap.png
│   ├── 09_arima_forecast.png
│   ├── 10_prophet_forecast.png
│   ├── 11_prophet_components.png
│   ├── arima_forecast.csv
│   └── prophet_forecast.csv
├── part1_data_extraction_cleaning.py
├── part2a_eda_visualization.py
├── part2b_sql_loader.py
├── part3_forecasting.py
├── requirements.txt
└── README.md
```

---

## 📊 Dataset
**Superstore Sales Dataset** — Kaggle

🔗 https://www.kaggle.com/datasets/vivek468/superstore-dataset-final

Place downloaded file as: `data/Sample - Superstore.csv`

---

## ⚙️ Installation

```bash
git clone https://github.com/ranjanadevi1802/retail-sales-capstone.git
cd retail-sales-capstone
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

---

## 🚀 How to Run

```bash
# Step 1 - Clean data
python part1_data_extraction_cleaning.py

# Step 2 - EDA charts
python part2a_eda_visualization.py

# Step 3 - Load to SQL
python part2b_sql_loader.py

# Step 4 - Forecasting
python part3_forecasting.py
```

---

## 📈 Key Findings

| Metric | Value |
|---|---|
| Total Revenue | ~$2.3M |
| Total Profit | ~$286K |
| Profit Margin | ~12.4% |
| Top Category | Technology |
| Top Region | West |
| Loss-Making Sub-Category | Tables |
| Best Forecast Model | Prophet (RMSE: $19,401) |

### Insights
- Q4 consistently records highest sales every year
- Tables sub-category is loss-making due to heavy discounts
- High discounts above 40% almost always lead to negative profit
- Prophet outperformed ARIMA with significantly lower RMSE

---

## 🛠️ Tech Stack

| Tool | Purpose |
|---|---|
| Python 3.x | Data processing & forecasting |
| Pandas | Data cleaning |
| Matplotlib / Seaborn | Visualization |
| SQLAlchemy | Python–SQL bridge |
| SQLite | Local database |
| statsmodels | ARIMA forecasting |
| Prophet | Seasonality-aware forecasting |
| Power BI | Interactive dashboards |

---

## 👩‍💻 Author
**Ranjana Devi**
B.Tech Information Science Engineering
Women's Engineering College, Puducherry










