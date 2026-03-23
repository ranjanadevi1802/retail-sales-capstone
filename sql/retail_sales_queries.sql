-- ================================================
-- CAPSTONE PROJECT 1 - Retail Sales Analysis
-- SQL Queries: Extraction + Advanced Analysis
-- ================================================

-- 1. View sample data
SELECT * FROM retail_sales LIMIT 10;

-- 2. Total records
SELECT COUNT(*) AS Total_Orders FROM retail_sales;

-- 3. Date range
SELECT MIN(Order_Date) AS Earliest, MAX(Order_Date) AS Latest
FROM retail_sales;

-- 4. Sales by Category
SELECT Category,
       ROUND(SUM(Sales), 2)  AS Total_Sales,
       ROUND(SUM(Profit), 2) AS Total_Profit
FROM retail_sales
GROUP BY Category
ORDER BY Total_Sales DESC;

-- 5. Sales by Region and Segment
SELECT Region, Segment,
       ROUND(SUM(Sales), 2)  AS Total_Sales,
       ROUND(SUM(Profit), 2) AS Total_Profit
FROM retail_sales
GROUP BY Region, Segment
ORDER BY Region, Total_Sales DESC;

-- 6. Monthly Sales Trend
SELECT Order_Year, Order_Month,
       ROUND(SUM(Sales), 2)         AS Monthly_Sales,
       ROUND(SUM(Profit), 2)        AS Monthly_Profit,
       COUNT(DISTINCT Order_ID)     AS Unique_Orders
FROM retail_sales
GROUP BY Order_Year, Order_Month
ORDER BY Order_Year, Order_Month;

-- 7. Top 10 Products by Sales
SELECT Product_Name, Category, Sub_Category,
       ROUND(SUM(Sales), 2)  AS Total_Sales,
       ROUND(SUM(Profit), 2) AS Total_Profit
FROM retail_sales
GROUP BY Product_Name, Category, Sub_Category
ORDER BY Total_Sales DESC
LIMIT 10;

-- 8. Loss-Making Sub-Categories
SELECT Sub_Category,
       ROUND(SUM(Sales), 2)  AS Total_Sales,
       ROUND(SUM(Profit), 2) AS Total_Profit
FROM retail_sales
GROUP BY Sub_Category
HAVING SUM(Profit) < 0
ORDER BY Total_Profit ASC;

-- 9. High Discount Orders with Negative Profit (Subquery)
SELECT Order_ID, Product_Name, Sales, Discount, Profit
FROM retail_sales
WHERE Discount > (
    SELECT AVG(Discount) * 1.5 FROM retail_sales
)
AND Profit < 0
ORDER BY Profit ASC;

-- 10. YoY Sales Growth
SELECT curr.Order_Year,
       curr.Total_Sales,
       prev.Total_Sales AS Prev_Year_Sales,
       ROUND((curr.Total_Sales - prev.Total_Sales) /
             prev.Total_Sales * 100, 2) AS YoY_Growth_Pct
FROM (
    SELECT Order_Year, ROUND(SUM(Sales), 2) AS Total_Sales
    FROM retail_sales GROUP BY Order_Year
) curr
LEFT JOIN (
    SELECT Order_Year, ROUND(SUM(Sales), 2) AS Total_Sales
    FROM retail_sales GROUP BY Order_Year
) prev ON curr.Order_Year = prev.Order_Year + 1
ORDER BY curr.Order_Year;

-- 11. KPI Summary
SELECT
    COUNT(DISTINCT Order_ID)                              AS Total_Orders,
    COUNT(DISTINCT Customer_ID)                           AS Unique_Customers,
    ROUND(SUM(Sales), 2)                                  AS Total_Revenue,
    ROUND(SUM(Profit), 2)                                 AS Total_Profit,
    ROUND(SUM(Profit)/SUM(Sales)*100, 2)                  AS Profit_Margin_Pct,
    ROUND(AVG(Sales), 2)                                  AS Avg_Order_Value
FROM retail_sales;