import streamlit as st
from db_connection import get_connection, release_connection, close_all_connections

# Function to execute queries
def execute_query(query):
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()
        return rows
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
    "SELECT category, sub_category, product_id, round (cast (sum(total_sales)as numeric), 2) FROM retail_sales GROUP BY category, sub_category, product_id ORDER BY tot_sales DESC limit 10;",
    "SELECT * FROM table2 LIMIT 10;",
    "SELECT * FROM table3 LIMIT 10;",
    "SELECT * FROM table4 LIMIT 10;",
    "SELECT * FROM table5 LIMIT 10;",
    "SELECT * FROM table6 LIMIT 10;",
    "SELECT * FROM table7 LIMIT 10;",
    "SELECT * FROM table8 LIMIT 10;",
    "SELECT * FROM table9 LIMIT 10;",
    "SELECT * FROM table10 LIMIT 10;"
]

# Render sections dynamically
for i, query in enumerate(queries, start=1):
    with st.expander(f"Section {i}"):
        st.subheader(f"Query Results for Section {i}")
        data = execute_query(query)
        if data:
            st.write(data)

# Clean up connections when the app shuts down
st.on_event("shutdown", close_all_connections)
