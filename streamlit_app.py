import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load data
df = pd.read_csv("Superstore_Sales_utf8.csv")

# Convert Order_Date to datetime format
df["Order_Date"] = pd.to_datetime(df["Order_Date"])

# Set page title
st.title("Data App Assignment")

# Display initial dataframe
st.write("### Input Data and Examples")
st.dataframe(df)

# Step 1: Dropdown for Category Selection
category_selected = st.selectbox("Select a Category", df["Category"].unique())

# Step 2: Multi-Select for Sub-Category within Selected Category
subcategories = df[df["Category"] == category_selected]["Sub_Category"].unique()
subcategories_selected = st.multiselect("Select Sub-Categories", subcategories, default=subcategories[:2])

# Filter data based on selections
filtered_df = df[(df["Category"] == category_selected) & (df["Sub_Category"].isin(subcategories_selected))]

# Step 3: Show Line Chart for Sales of Selected Sub-Categories
sales_by_date = filtered_df.groupby("Order_Date")["Sales"].sum()
st.line_chart(sales_by_date, y="Sales")

# Step 4: Calculate Metrics
total_sales = filtered_df["Sales"].sum()
total_profit = filtered_df["Profit"].sum()
profit_margin = (total_profit / total_sales) * 100 if total_sales != 0 else 0

# Step 5: Calculate Delta for Profit Margin Comparison
overall_profit_margin = (df["Profit"].sum() / df["Sales"].sum()) * 100 if df["Sales"].sum() != 0 else 0
profit_margin_delta = profit_margin - overall_profit_margin

# Display Metrics
st.metric("Total Sales", f"${total_sales:,.2f}")
st.metric("Total Profit", f"${total_profit:,.2f}")
st.metric("Profit Margin (%)", f"{profit_margin:.2f}%", delta=f"{profit_margin_delta:.2f}%")
