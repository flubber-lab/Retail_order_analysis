# Questions by GUVI
import streamlit as st
import pandas as pd
from db_connection import get_connection, release_connection, close_all_connections

# Function to execute queries
def execute_query(query):
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()
        # Retrieve column names reliably
        if cursor.description:
            columns = [desc[0] for desc in cursor.description]
        else:
            columns = []  # Fallback if no metadata
        return pd.DataFrame(rows, columns=columns)
    except Exception as e:
        st.error(f"Error executing query: {e}")
        return pd.DataFrame(columns=["Error"])
    finally:
        if conn:
            release_connection(conn)

# Streamlit App
st.title("GUVI 10 Queries")

# Define queries 
queries = [
    "SELECT category, sub_category, product_id, round (cast (sum(total_sales)as numeric), 2) as tot_sales FROM retail_sales GROUP BY category, sub_category, product_id ORDER BY tot_sales DESC limit 10;",
    "select ro.city, round(cast(avg(rs.profit_margin) *100 as numeric),2) as margin from retail_orders ro join retail_sales rs on ro.order_id = rs.order_id where rs.profit_margin is not null group by ro.city order by margin desc limit 5;",
    "select category, round(cast(sum(discount) as numeric),2) as total_discount from retail_sales group by category order by total_discount desc;",
    "select category, round(cast(avg(sale_price) as numeric), 2) as average_sale_price from retail_sales group by category order by average_sale_price",
    "select ro.region,round(cast(avg(sale_price)as numeric), 2) as average_sale_price from retail_sales rs join retail_orders ro on rs.order_id = ro.order_id group by region order by average_sale_price desc limit 1;",
    "select category, round(cast(sum(total_profit) as numeric),2) as total_profit from retail_sales group by  category order by total_profit;",
    "select ro.segment, sum(rs.quantity) as total_quantity from retail_orders ro join retail_sales rs on ro.order_id = rs.order_id group by ro.segment order by total_quantity desc limit 3;",
    "select ro.region, round(cast(avg(rs.discount_percent) as numeric),2) as avg_discount_percent from retail_orders ro join retail_sales rs on ro.order_id = rs.order_id group by ro.region order by avg_discount_percent desc;",
    "select category, round (cast (sum(total_profit)as numeric), 2) as tp from retail_sales group by category order by tp desc limit 1;",
    "select extract(year from to_date(order_date, 'DD-MM-YYYY')) as year, round(cast(sum(total_sales) as numeric),2) as revenue from retail_sales group by extract(year from to_date(order_date, 'DD-MM-YYYY')) order by year;"
]
questions = [
    "Find top 10 highest revenue generating products",
    "Find the top 5 cities with the highest profit margins",
    "Calculate the total discount given for each category",
    "Find the average sale price per product category",
    "Find the region with the highest average sale price",
    "Find the total profit per category",
    "Identify the top 3 segments with the highest quantity of orders",
    "Determine the average discount percentage given per region",
    "Find the product category with the highest total profit",
    "Calculate the total revenue generated per year"
]

# Create tabs for sections
tabs = st.tabs([f"Question {i}" for i in range(1, len(queries) + 1)])

# Render query results in each tab
for i, tab in enumerate(tabs, start=0):
    with tab:
        st.subheader(f"Query Results for Section {i + 1}")
        st.write(questions[i])
        data = execute_query(queries[i])
        if not data.empty:
            st.dataframe(data, use_container_width= True)
        else:
            st.write("No data available for this query.")


# Clean up connections when the app shuts down
st.stop()