# Own Questions
import streamlit as st
import pandas as pd
import plotly.express as px
from db_connection import get_connection, release_connection, close_all_connections

st.set_page_config(page_title = 'Own Questions', page_icon= '📈')

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
st.title("Own Questions")
st.page_link("streamlit_app.py", label = 'Home', icon = "🏠")
st.page_link("pages/business_insights.py", label = 'Business Insights', icon = "📊")
st.page_link("pages/questions-by-guvi.py", label = 'GUVI Questions', icon = "📋")

# Define queries
queries = [
    #Calculate the total profit for each product sub-category.
    "select category,sub_category, round(cast(sum(total_profit) as numeric),2) as tot_profit from retail_sales group by category,sub_category order by tot_profit desc;",
    #Determine the average discount percentage for each customer segment.
    "select ro.segment, round(avg(rs.discount_percent),2) as avg_discount from retail_sales rs join retail_orders ro on ro.order_id = rs.order_id group by segment order by avg_discount desc;",
    #Identify the 3 states with the highest total number of orders.
    "select state, count(order_id) as no_of_orders from retail_orders group by state order by no_of_orders desc limit 3;",
    #Find the month with the highest total revenue for each year.
    "with mon_rev as (select extract(year from to_date(order_date, 'DD-MM-YYYY')) as year, extract(month from to_date(order_date, 'DD-MM-YYYY')) as month, round(cast(sum(total_sales) as numeric),2) as rev from retail_sales group by year, month),ranked_rev as(select year,month,rev, rank() over (partition by year order by rev desc) as rev_rank from mon_rev) select year,month,rev from ranked_rev where rev_rank =1 order by year,month;",
    #Find the category with the lowest average sale price.
    "select category, round(cast(avg(sale_price) as numeric),2) as avg_sale_price from retail_sales group by category order by avg_sale_price limit 1;",
    #Calculate the average profit margin per product.
    "select product_id, round(cast(avg(profit_margin) as numeric),2) as avg_margin from retail_sales group by product_id order by avg_margin;",
    #Calculate the total revenue, total profit, and total discount for each year.
    "select extract(year from to_date(order_date, 'DD-MM-YYYY')) as year, round(cast(sum(total_sales) as numeric),2) as sales, round(cast(sum(total_profit) as numeric),2) as profit,round(cast(sum(discount*quantity) as numeric),2) as discount from retail_sales group by year order by sales,profit,discount",
    #Top 3 segment who placed the highest number of orders.
    "select segment, count(order_date) as orders from retail_orders group by segment order by orders desc;",
    #Determine the average order size for each product sub category.
    "select sub_category, round(cast(avg(quantity) as numeric),2) as avg_qty from retail_sales group by sub_category order by avg_qty desc;",
    #Identify the state with the lowest total profit.
    "select ro.state, round(cast(sum(rs.total_profit) as numeric),2) as profit from retail_sales rs join retail_orders ro on ro.order_id = rs.order_id group by ro.state order by profit limit 1;"
]

questions = [
    "Calculate the total profit for each product sub-category",
    "Determine the average discount percentage for each customer segment",
    "Identify the 3 states with the highest total number of orders",
    "Find the month with the highest total revenue for each year",
    "Find the category with the lowest average sale price",
    "Calculate the average profit margin per product",
    "Calculate the total revenue, total profit, and total discount for each year",
    "Top 3 segment who placed the highest number of orders",
    "Determine the average order size for each product sub category",
    "Identify the state with the lowest total profit"
]

charts = [
    {"type": "bar", "x": "sub_category", "y": "tot_profit"},
    {"type": "pie", "labels": "segment", "values": "avg_discount"},
    {"type": "choropleth", "geo_column": "state", "value_column": "no_of_orders","location_mode":"USA-States"},
    {"type": "bar", "x": "month", "y": "rev"},
    {"type": "bar", "x": "category", "y": "avg_sale_price"},
    {"type": "bar", "x": "product_id", "y": "avg_margin"},
    {"type": "bar", "x": "year", "y": ["sales","profit"]},
    {"type": "bar", "x": "segment", "y": "orders"},
    {"type": "pie", "labels": "sub_category", "values": "avg_qty"},
    {"type": "choropleth", "geo_column": "state", "value_column": "profit","location_mode":"USA-States"}

]

state_name_to_abbr = {
    "Alabama": "AL",
    "Alaska": "AK",
    "Arizona": "AZ",
    "Arkansas": "AR",
    "California": "CA",
    "Texas": "TX",
    "New York": "NY",
    "South Dakota": "SD"}

# Create tabs for sections
tabs = st.tabs([f"Questions {i}" for i in range(1, len(queries) + 1)])

# Render query results in each tab
for i, tab in enumerate(tabs, start=0):
    with tab:
        st.subheader(f"Query Results for Section {i + 1}")
        st.write(questions[i])
        data = execute_query(queries[i])
        if not data.empty:
            if "state" in data.columns:
                data["state"] = data["state"].map(state_name_to_abbr)
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
            elif chart_type == "choropleth":
                geo_column = chart_config["geo_column"]
                value_column = chart_config["value_column"]
                location_mode = chart_config.get("location_mode", "ISO-3")
                if geo_column in data.columns and value_column in data.columns:
                    # Create a Choropleth Map
                    fig = px.choropleth(
                        data,
                        locations=geo_column,  
                        locationmode="USA-states", 
                        color=value_column,
                        scope ='usa', 
                        title="Sales by States",
                        color_continuous_scale="Viridis"  
                    )
                    st.plotly_chart(fig)
                else:
                    st.error(f"Columns {geo_column} and/or {value_column} not found in data.")
            else:
                st.write("Unsupported chart type.")
        else:
            st.write("No data available for this query.")

# Clean up connections when the app shuts down
st.stop()
