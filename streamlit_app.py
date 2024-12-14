# Welcome
import streamlit as st

st.set_page_config(page_title="Home", page_icon="🏠")

st.title("Retail Sales Order Analysis 📈")
st.subheader("Welcome to the Retail Sales Order Analysis Dashboard!")
st.write("""

This app transforms your raw sales data into actionable business insights. Key features include:

- **Data Processing**: Cleans and organizes sales data for reliable analysis.
- **Metrics & Trends**: Displays sales, orders, and customer trends at a glance.
- **Interactive Visualizations**: Explore trends, regional performance, and top products with intuitive charts.
- **Advanced Filtering**: Customize views by time, region, or product category.
- **Actionable Insights**: Identify growth opportunities and optimize strategies.

Dive in to uncover insights and make data-driven decisions with ease!
""")

st.page_link("pages/business_insights.py", label = 'Business Insights', icon = "📊")
st.page_link("pages/questions-by-guvi.py", label = 'GUVI Questions', icon = "📋")
st.page_link("pages/own_questions.py", label = 'Own Questions', icon = "📈")
