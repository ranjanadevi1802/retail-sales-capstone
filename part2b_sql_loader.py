import pandas as pd
from sqlalchemy import create_engine, text

def load_to_sqlite(csv_path='data/cleaned_superstore.csv',
                   db_path='data/retail_sales.db',
                   table_name='retail_sales'):
    print("=" * 50)
    print(" LOADING DATA INTO SQLITE DATABASE")
    print("=" * 50)

    df = pd.read_csv(csv_path)
    print(f"✅ CSV loaded: {df.shape[0]} rows")

    engine = create_engine(f'sqlite:///{db_path}')
    df.to_sql(table_name, con=engine, if_exists='replace', index=False)
    print(f"✅ Data written to table '{table_name}'")

    with engine.connect() as conn:
        result = conn.execute(text(f"SELECT COUNT(*) FROM {table_name}"))
        count  = result.scalar()
    print(f"✅ Verified: {count} rows in database")
    return engine

def run_analysis_queries(engine):
    print("\n===== SQL ANALYSIS RESULTS =====\n")

    queries = {
        "Sales by Category": """
            SELECT Category,
                   ROUND(SUM(Sales), 2)  AS Total_Sales,
                   ROUND(SUM(Profit), 2) AS Total_Profit
            FROM retail_sales
            GROUP BY Category
            ORDER BY Total_Sales DESC
        """,
        "Sales by Region": """
            SELECT Region,
                   ROUND(SUM(Sales), 2)  AS Total_Sales,
                   ROUND(SUM(Profit), 2) AS Total_Profit
            FROM retail_sales
            GROUP BY Region
            ORDER BY Total_Sales DESC
        """,
        "Top 5 Customers": """
            SELECT Customer_Name,
                   ROUND(SUM(Sales), 2) AS Total_Sales
            FROM retail_sales
            GROUP BY Customer_Name
            ORDER BY Total_Sales DESC
            LIMIT 5
        """,
        "Loss-Making Sub-Categories": """
            SELECT Sub_Category,
                   ROUND(SUM(Profit), 2) AS Total_Profit
            FROM retail_sales
            GROUP BY Sub_Category
            HAVING SUM(Profit) < 0
            ORDER BY Total_Profit ASC
        """,
        "KPI Summary": """
            SELECT
                COUNT(DISTINCT Order_ID)       AS Total_Orders,
                ROUND(SUM(Sales), 2)           AS Total_Revenue,
                ROUND(SUM(Profit), 2)          AS Total_Profit,
                ROUND(AVG(Sales), 2)           AS Avg_Order_Value
            FROM retail_sales
        """,
    }

    with engine.connect() as conn:
        for title, query in queries.items():
            print(f"--- {title} ---")
            df_result = pd.read_sql(text(query), conn)
            print(df_result.to_string(index=False))
            print()

if __name__ == "__main__":
    engine = load_to_sqlite()
    run_analysis_queries(engine)
    print("✅ Part 2B complete!")
