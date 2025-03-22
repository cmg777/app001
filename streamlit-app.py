import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import random

# Page configuration
st.set_page_config(page_title="Data Analysis Dashboard", layout="wide")
st.title("Interactive Data Analysis Dashboard")
st.write("Explore customer data with interactive filters")

# Simulate Dataset
@st.cache_data
def simulate_dataset(num_rows=1000):
    data = {
        'CustomerID': range(1, num_rows + 1),
        'Age': np.random.randint(18, 70, num_rows),
        'Income': np.random.normal(50000, 15000, num_rows),
        'PurchaseAmount': np.random.uniform(10, 500, num_rows),
        'City': [random.choice(['New York', 'London', 'Tokyo', 'Paris', 'Sydney']) for _ in range(num_rows)],
        'ProductCategory': [random.choice(['Electronics', 'Clothing', 'Books', 'Home', 'Food']) for _ in range(num_rows)]
    }
    return pd.DataFrame(data)

# Generate the dataset
df = simulate_dataset()

# Display raw data in an expander
with st.expander("View Raw Data"):
    st.dataframe(df)

# Sidebar for filters
st.sidebar.header("Filter Options")

# Age slider
age_range = st.sidebar.slider(
    "Select Age Range:",
    min_value=18,
    max_value=70,
    value=(20, 60)
)

# City selection
city_options = ["All", "New York", "London", "Tokyo", "Paris", "Sydney"]
selected_city = st.sidebar.selectbox("Select City:", city_options)

# Product category selection
product_options = ["All", "Electronics", "Clothing", "Books", "Home", "Food"]
product_category = st.sidebar.selectbox("Select Product Category:", product_options)

# Apply filters
filtered_df = df[(df['Age'] >= age_range[0]) & (df['Age'] <= age_range[1])]

if selected_city != "All":
    filtered_df = filtered_df[filtered_df['City'] == selected_city]

if product_category != "All":
    filtered_df = filtered_df[filtered_df['ProductCategory'] == product_category]

# Display filter summary and filtered data count
st.write(f"Showing data for ages {age_range[0]}-{age_range[1]}, " +
         f"City: {selected_city}, Product Category: {product_category}")
st.write(f"Filtered data contains {len(filtered_df)} records")

# Create visualizations in a 2x2 grid
col1, col2 = st.columns(2)

with col1:
    # Age Distribution
    st.subheader("Age Distribution")
    fig_age = px.histogram(filtered_df, x='Age', title='Age Distribution')
    st.plotly_chart(fig_age, use_container_width=True)

    # City Distribution
    st.subheader("City Distribution")
    city_counts = filtered_df['City'].value_counts().reset_index()
    city_counts.columns = ['City', 'Count']
    fig_city = px.bar(city_counts, x='City', y='Count', title='City Distribution')
    st.plotly_chart(fig_city, use_container_width=True)

with col2:
    # Income vs. Purchase Amount
    st.subheader("Income vs. Purchase Amount")
    fig_income_purchase = px.scatter(filtered_df, x='Income', y='PurchaseAmount', 
                                     color='City', title='Income vs. Purchase Amount')
    st.plotly_chart(fig_income_purchase, use_container_width=True)

    # Purchase Amount by Product Category (Box Plot)
    st.subheader("Purchase Amount by Product Category")
    fig_purchase_category = px.box(filtered_df, x='ProductCategory', y='PurchaseAmount', 
                                  title='Purchase Amount by Product Category')
    st.plotly_chart(fig_purchase_category, use_container_width=True)

# Add statistics section
st.header("Data Statistics")
col3, col4, col5 = st.columns(3)

with col3:
    st.metric("Average Age", f"{filtered_df['Age'].mean():.1f}")
    st.metric("Average Income", f"${filtered_df['Income'].mean():.2f}")

with col4:
    st.metric("Average Purchase", f"${filtered_df['PurchaseAmount'].mean():.2f}")
    st.metric("Total Purchases", f"${filtered_df['PurchaseAmount'].sum():.2f}")

with col5:
    st.metric("Highest Purchase", f"${filtered_df['PurchaseAmount'].max():.2f}")
    st.metric("Most Common City", filtered_df['City'].value_counts().index[0] if not filtered_df.empty else "N/A")

# Add correlation heatmap
st.header("Correlation Analysis")
numeric_df = filtered_df.select_dtypes(include=['float64', 'int64'])
corr = numeric_df.corr()
fig_corr = px.imshow(corr, text_auto=True, aspect="auto", title="Correlation Heatmap")
st.plotly_chart(fig_corr, use_container_width=True)

# Add footer
st.markdown("---")
st.markdown("Data Analysis Dashboard | Created with Streamlit")
