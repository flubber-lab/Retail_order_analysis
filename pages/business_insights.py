# Business Insights
import streamlit as st
import pandas as pd
import plotly.express as px
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
st.title("Business Analysis")

# Define queries 
queries = [
    "select category, sub_category,product_id, sum(total_sales) as total_sale from retail_sales group by category, sub_category,product_id order by total_sale desc limit 3;",
    "select extract(month from to_date(order_date, 'DD-MM-YYYY'))as month, extract(year from to_date(order_date,'DD-MM-YYYY')) as year, round(cast(sum(total_sales) as numeric),2) as total_rev, round(cast(lag(sum (total_sales)) over (partition by extract(month from to_date(order_date,'DD-MM-YYYY')) order by extract(year from to_date(order_date, 'DD-MM-YYYY'))) as numeric),2)as previous_year_revenue, round(cast(case when lag(sum(total_sales)) over (partition by extract(month from to_date(order_date, 'DD-MM-YYYY')) order by extract(year from to_date(order_date, 'DD-MM-YYYY'))) is not null then ((sum (total_sales) -lag(sum(total_sales)) over (partition by extract(month from to_date(order_date,'DD-MM-YYYY')) order by extract(year from to_date(order_date,'DD-MM-YYYY')))) / lag(sum(total_sales)) over (partition by extract(month from to_date(order_date,'DD-MM-YYYY')) order by extract(year from to_date (order_date,'DD-MM-YYYY')))) * 100 else null end as numeric),2) as Year_on_Year_gp from retail_sales group by extract(year from to_date (order_date, 'DD-MM-YYYY')), extract(month from to_date(order_date, 'DD-MM-YYYY')) order by year desc, month;",
    "WITH product_summary AS (SELECT product_id, category, ROUND(CAST(SUM(total_sales) AS NUMERIC), 2) AS tot_rev,SUM(total_profit) AS total_margin FROM retail_sales GROUP BY product_id, category),rank_prod AS (SELECT product_id, category, tot_rev, total_margin, ROW_NUMBER() OVER (PARTITION BY category ORDER BY tot_rev DESC) AS r_rank FROM product_summary) SELECT product_id, category, tot_rev, total_margin, r_rank, CASE WHEN tot_rev > 10000 THEN 'Most Selling' ELSE 'Least Selling' END AS rev_cat FROM rank_prod WHERE tot_rev > 0 ORDER BY category, r_rank;",
    "select ro. region, round (cast (sum(rs.total_sales) as numeric), 2) as tot_sales from retail_sales rs inner join retail_orders ro on rs.order_id = ro.order_id group by ro.region order by tot_sales desc;",
    "select category,discount_percent, sum(quantity) as total_qty,round(cast(sum(total_sales) as numeric),2) as tot_sales from retail_sales where discount_percent in (0,1,2,3,4,5) group by category,discount_percent order by total_qty,tot_sales;"
]

questions = [
    "Top-Selling Products: Identify the products that generate the highest revenue based on sale prices.",
    "Monthly Sales Analysis: Compare year-over-year sales to identify growth or decline in certain months.",
    "Product Performance: Use functions like GROUP BY, HAVING, ROW_NUMBER(), and CASE WHEN to categorize and rank products by their revenue, profit margin, etc.",
    "Regional Sales Analysis: Query sales data by region to identify which areas are performing best.",
    "Discount Analysis: Identify products with discounts greater than 20% and calculate the impact of discounts on sales."
]

charts = [

    {"type": "bar", "x": "sub_category", "y": "total_sale"},
    {"type": "bar", "x": "month", "y": "total_rev"},
    {"type": "bar", "x": "category", "y": "tot_rev"},
    {"type": "pie", "labels": "region", "values": "tot_sales"},
    {"type": "bar", "x": "category", "y": "tot_sales"}
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
            chart_config = charts[i]
            chart_type = chart_config["type"] 
            # Generate charts based on type
            if chart_type == "line":
                fig = px.line(data, x=chart_config["x"], y=chart_config["y"], title="Line Chart")
                st.plotly_chart(fig)
            elif chart_type == "bar":
                fig = px.bar(data, x=chart_config["x"], y=chart_config["y"], title="Bar Chart")
                st.plotly_chart(fig)
            elif chart_type == "pie":
                fig = px.pie(data, names=chart_config["labels"], values=chart_config["values"], title="Pie Chart")
                st.plotly_chart(fig)
            else:
                st.write("Unsupported chart type.")
        else:
            st.write("No data available for this query.")


# Clean up connections when the app shuts down
st.stop()