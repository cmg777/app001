import streamlit as st

# This must be the very first Streamlit command
st.set_page_config(page_title="Data Analysis Dashboard", layout="wide")

import pandas as pd
import numpy as np
import random

# Title and introduction
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

# Create visualizations using Streamlit's built-in chart functions
col1, col2 = st.columns(2)

with col1:
    st.subheader("Age Distribution")
    # Calculate histogram data manually
    age_counts = filtered_df['Age'].value_counts().sort_index().reset_index()
    age_counts.columns = ['Age', 'Count']
    st.bar_chart(age_counts.set_index('Age'))

    st.subheader("City Distribution")
    city_counts = filtered_df['City'].value_counts().reset_index()
    city_counts.columns = ['City', 'Count']
    st.bar_chart(city_counts.set_index('City'))

with col2:
    st.subheader("Income vs. Purchase Amount")
    chart_data = filtered_df[['Income', 'PurchaseAmount']]
    st.scatter_chart(chart_data, x='Income', y='PurchaseAmount')

    st.subheader("Purchase Amount by Product Category")
    # Calculate stats for each product category
    product_stats = filtered_df.groupby('ProductCategory')['PurchaseAmount'].agg(['mean', 'median', 'min', 'max']).reset_index()
    for col in product_stats.columns[1:]:
        product_stats[col] = product_stats[col].round(2)
    st.dataframe(product_stats)

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
corr = numeric_df.corr().round(2)
st.dataframe(corr)

# Add purchase trends over age groups
st.header("Purchase Trends by Age Group")
# Create age bins
filtered_df['AgeGroup'] = pd.cut(filtered_df['Age'], 
                               bins=[18, 25, 35, 45, 55, 70], 
                               labels=['18-25', '26-35', '36-45', '46-55', '56-70'])

# Group by age group and product category
age_product_data = filtered_df.groupby(['AgeGroup', 'ProductCategory'])['PurchaseAmount'].mean().reset_index()

# Pivot the data for easier reading
pivot_data = age_product_data.pivot(index='AgeGroup', columns='ProductCategory', values='PurchaseAmount').reset_index()
st.dataframe(pivot_data.round(2))

# Additional user engagement
st.header("Explore Your Data")
exploration_tab1, exploration_tab2 = st.tabs(["Data by City", "Data by Product"])

with exploration_tab1:
    selected_city_explore = st.selectbox("Select a city to explore:", filtered_df['City'].unique())
    city_data = filtered_df[filtered_df['City'] == selected_city_explore]
    
    st.subheader(f"Summary Statistics for {selected_city_explore}")
    st.write(f"Number of customers: {len(city_data)}")
    st.write(f"Average age: {city_data['Age'].mean():.1f}")
    st.write(f"Average purchase: ${city_data['PurchaseAmount'].mean():.2f}")
    st.write(f"Average income: ${city_data['Income'].mean():.2f}")
    
    # Product distribution for selected city
    st.subheader(f"Product Categories in {selected_city_explore}")
    product_dist = city_data['ProductCategory'].value_counts().reset_index()
    product_dist.columns = ['Product Category', 'Count']
    st.bar_chart(product_dist.set_index('Product Category'))

with exploration_tab2:
    selected_product = st.selectbox("Select a product category to explore:", filtered_df['ProductCategory'].unique())
    product_data = filtered_df[filtered_df['ProductCategory'] == selected_product]
    
    st.subheader(f"Summary Statistics for {selected_product}")
    st.write(f"Number of purchases: {len(product_data)}")
    st.write(f"Average purchase amount: ${product_data['PurchaseAmount'].mean():.2f}")
    st.write(f"Highest purchase amount: ${product_data['PurchaseAmount'].max():.2f}")
    
    # City distribution for selected product
    st.subheader(f"City Distribution for {selected_product}")
    city_dist = product_data['City'].value_counts().reset_index()
    city_dist.columns = ['City', 'Count']
    st.bar_chart(city_dist.set_index('City'))

# Add footer
st.markdown("---")
st.markdown("Data Analysis Dashboard | Created with Streamlit")