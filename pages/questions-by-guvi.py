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
        columns = [desc[0] for desc in cursor.description]
        return pd.DataFrame(rows, columns=columns)  
    except Exception as e:
        st.error(f"Error executing query: {e}")
        return []
    finally:
        if conn:
            release_connection(conn)

# Streamlit App
st.title("GUVI 10 Queries")

# Define queries (you can replace these with your actual queries)
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

# Create tabs for sections
tabs = st.tabs([f"Section {i}" for i in range(1, len(queries) + 1)])

# Render query results in each tab
for i, (tab, query) in enumerate(zip(tabs, queries), start=1):
    with tab:
        st.subheader(f"Query Results for Section {i}")
        data = execute_query(query)
        if data:
            st.dataframe(data)
        else:
            st.write("No data available for this query.")

# Clean up connections when the app shuts down
st.on_event("shutdown", close_all_connections)
