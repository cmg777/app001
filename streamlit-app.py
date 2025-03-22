import streamlit as st
import pandas as pd
import numpy as np
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

# Number of rows to display
num_rows = st.sidebar.slider("Number of rows to display", 5, 50, 20)

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

# Display filtered data
st.subheader("Filtered Data")
st.dataframe(filtered_df.head(num_rows))

# Data statistics
st.header("Data Statistics")
col1, col2 = st.columns(2)

with col1:
    st.subheader("Age Statistics")
    age_stats = pd.DataFrame({
        'Statistic': ['Mean', 'Median', 'Min', 'Max', 'Standard Deviation'],
        'Value': [
            f"{filtered_df['Age'].mean():.2f}",
            f"{filtered_df['Age'].median():.2f}",
            f"{filtered_df['Age'].min():.2f}",
            f"{filtered_df['Age'].max():.2f}",
            f"{filtered_df['Age'].std():.2f}"
        ]
    })
    st.table(age_stats)
    
    st.subheader("Purchase Amount Statistics")
    purchase_stats = pd.DataFrame({
        'Statistic': ['Mean', 'Median', 'Min', 'Max', 'Standard Deviation', 'Total'],
        'Value': [
            f"${filtered_df['PurchaseAmount'].mean():.2f}",
            f"${filtered_df['PurchaseAmount'].median():.2f}",
            f"${filtered_df['PurchaseAmount'].min():.2f}",
            f"${filtered_df['PurchaseAmount'].max():.2f}",
            f"${filtered_df['PurchaseAmount'].std():.2f}",
            f"${filtered_df['PurchaseAmount'].sum():.2f}"
        ]
    })
    st.table(purchase_stats)

with col2:
    st.subheader("Income Statistics")
    income_stats = pd.DataFrame({
        'Statistic': ['Mean', 'Median', 'Min', 'Max', 'Standard Deviation'],
        'Value': [
            f"${filtered_df['Income'].mean():.2f}",
            f"${filtered_df['Income'].median():.2f}",
            f"${filtered_df['Income'].min():.2f}",
            f"${filtered_df['Income'].max():.2f}",
            f"${filtered_df['Income'].std():.2f}"
        ]
    })
    st.table(income_stats)
    
    # City distribution
    st.subheader("City Distribution")
    city_counts = filtered_df['City'].value_counts().reset_index()
    city_counts.columns = ['City', 'Count']
    st.table(city_counts)

# Group data by product category
st.header("Product Category Analysis")
product_analysis = filtered_df.groupby('ProductCategory').agg({
    'PurchaseAmount': ['mean', 'median', 'min', 'max', 'sum', 'count']
}).reset_index()

# Flatten the multi-level columns
product_analysis.columns = ['ProductCategory', 'Mean Purchase', 'Median Purchase', 
                           'Min Purchase', 'Max Purchase', 'Total Revenue', 'Transaction Count']

# Format currency columns
for col in product_analysis.columns[1:6]:
    product_analysis[col] = product_analysis[col].apply(lambda x: f"${x:.2f}")

st.dataframe(product_analysis)

# Correlation Analysis
st.header("Correlation Analysis")
numeric_df = filtered_df.select_dtypes(include=['float64', 'int64'])
corr = numeric_df.corr().round(2)
st.dataframe(corr)

# Top Customers
st.header("Top Customers by Purchase Amount")
top_customers = filtered_df.sort_values('PurchaseAmount', ascending=False).head(10)
st.dataframe(top_customers)

# Add footer
st.markdown("---")
st.markdown("Data Analysis Dashboard | Created with Streamlit")