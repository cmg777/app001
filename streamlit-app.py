import streamlit as st
import pandas as pd
import numpy as np
import random

# Install plotly
import subprocess
import sys

# Try to install plotly
st.write("Installing required packages...")
try:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "plotly"])
    st.success("Plotly installed successfully!")
except Exception as e:
    st.error(f"Failed to install Plotly: {e}")
    st.warning("Continuing with limited functionality...")

# Now try to import plotly
try:
    import plotly.express as px
    import plotly.graph_objects as go
    PLOTLY_AVAILABLE = True
    st.success("Plotly imported successfully!")
except ImportError:
    PLOTLY_AVAILABLE = False
    st.error("Plotly could not be imported. Using alternative visualizations.")

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

# Create visualizations based on plotly availability
col1, col2 = st.columns(2)

with col1:
    st.subheader("Age Distribution")
    if PLOTLY_AVAILABLE:
        fig_age = px.histogram(filtered_df, x='Age', 
                              title='Age Distribution',
                              color_discrete_sequence=['#3366CC'])
        st.plotly_chart(fig_age, use_container_width=True)
    else:
        # Fallback to basic chart using Streamlit
        st.bar_chart(filtered_df['Age'].value_counts().sort_index())

    st.subheader("City Distribution")
    city_counts = filtered_df['City'].value_counts().reset_index()
    city_counts.columns = ['City', 'Count']
    if PLOTLY_AVAILABLE:
        fig_city = px.bar(city_counts, x='City', y='Count', 
                         title='City Distribution')
        st.plotly_chart(fig_city, use_container_width=True)
    else:
        # Fallback to table
        st.table(city_counts)

with col2:
    st.subheader("Income vs. Purchase Amount")
    if PLOTLY_AVAILABLE:
        fig_income_purchase = px.scatter(filtered_df, x='Income', y='PurchaseAmount', 
                                        color='City', 
                                        title='Income vs. Purchase Amount')
        st.plotly_chart(fig_income_purchase, use_container_width=True)
    else:
        # Fallback to basic scatter chart
        st.scatter_chart(filtered_df, x='Income', y='PurchaseAmount')

    st.subheader("Purchase Amount by Product Category")
    if PLOTLY_AVAILABLE:
        fig_purchase_category = px.box(filtered_df, x='ProductCategory', y='PurchaseAmount', 
                                      title='Purchase Amount by Product Category')
        st.plotly_chart(fig_purchase_category, use_container_width=True)
    else:
        # Group by product category
        product_stats = filtered_df.groupby('ProductCategory')['PurchaseAmount'].agg(['mean', 'median', 'min', 'max']).reset_index()
        st.table(product_stats)

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

if PLOTLY_AVAILABLE:
    fig_corr = px.imshow(corr, 
                        text_auto=True, 
                        color_continuous_scale='RdBu_r',
                        title="Correlation Heatmap")
    st.plotly_chart(fig_corr, use_container_width=True)
else:
    # Fallback to table
    st.table(corr.round(2))

# Add purchase trends over age groups
st.header("Purchase Trends by Age Group")
# Create age bins
filtered_df['AgeGroup'] = pd.cut(filtered_df['Age'], 
                               bins=[18, 25, 35, 45, 55, 70], 
                               labels=['18-25', '26-35', '36-45', '46-55', '56-70'])

# Group by age group and product category
age_product_data = filtered_df.groupby(['AgeGroup', 'ProductCategory'])['PurchaseAmount'].mean().reset_index()

if PLOTLY_AVAILABLE:
    fig_trends = px.bar(age_product_data, 
                       x='AgeGroup', 
                       y='PurchaseAmount', 
                       color='ProductCategory',
                       barmode='group',
                       title='Average Purchase Amount by Age Group and Product Category')
    st.plotly_chart(fig_trends, use_container_width=True)
else:
    # Pivot the data for easier reading
    pivot_data = age_product_data.pivot(index='AgeGroup', columns='ProductCategory', values='PurchaseAmount')
    st.table(pivot_data.round(2))

# Add footer
st.markdown("---")
st.markdown("Data Analysis Dashboard | Created with Streamlit")