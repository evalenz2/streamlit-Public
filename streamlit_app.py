import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import math

st.title("Data App Assignment, on Oct 7th")

st.write("### Input Data and Examples")
df = pd.read_csv("Superstore_Sales_utf8.csv", parse_dates=True)
st.dataframe(df)

# This bar chart will not have solid bars--but lines--because the detail data is being graphed independently
st.bar_chart(df, x="Category", y="Sales")

# Now let's do the same graph where we do the aggregation first in Pandas... (this results in a chart with solid bars)
st.dataframe(df.groupby("Category").sum())
# Using as_index=False here preserves the Category as a column.  If we exclude that, Category would become the dataframe index and we would need to use x=None to tell bar_chart to use the index
st.bar_chart(df.groupby("Category", as_index=False).sum(), x="Category", y="Sales", color="#04f")

# Aggregating by time
# Here we ensure Order_Date is in datetime format, then set it as an index to our dataframe
df["Order_Date"] = pd.to_datetime(df["Order_Date"])
df.set_index('Order_Date', inplace=True)
# Here the Grouper is using our newly set index to group by Month ('M')
sales_by_month = df.filter(items=['Sales']).groupby(pd.Grouper(freq='M')).sum()

st.dataframe(sales_by_month)

# Here the grouped months are the index and automatically used for the x-axis
st.line_chart(sales_by_month, y="Sales")

# ---------------- NEW FEATURES FOR THE ASSIGNMENT ----------------
st.write("## Additions")

# (1) Add a drop-down for Category
category_selected = st.selectbox("Select a Category", df["Category"].unique())

# (2) Add a multi-select for Sub_Category within the selected Category
subcategories = df[df["Category"] == category_selected]["Sub_Category"].unique()
subcategories_selected = st.multiselect("Select Sub-Categories", subcategories, default=subcategories[:2])

# Filter data based on selections
filtered_df = df[(df["Category"] == category_selected) & (df["Sub_Category"].isin(subcategories_selected))]

# (3) Show a line chart of sales for the selected Sub-Categories
sales_by_date = filtered_df.groupby("Order_Date")["Sales"].sum()
st.line_chart(sales_by_date, y="Sales")

# (4) Show three metrics: Total Sales, Total Profit, and Overall Profit Margin (%)
total_sales = filtered_df["Sales"].sum()
total_profit = filtered_df["Profit"].sum()
profit_margin = (total_profit / total_sales) * 100 if total_sales != 0 else 0

# (5) Use the delta option in the profit margin metric to compare with overall average profit margin
overall_profit_margin = (df["Profit"].sum() / df["Sales"].sum()) * 100 if df["Sales"].sum() != 0 else 0
profit_margin_delta = profit_margin - overall_profit_margin

# Display Metrics
st.metric("Total Sales", f"${total_sales:,.2f}")
st.metric("Total Profit", f"${total_profit:,.2f}")
st.metric("Profit Margin (%)", f"{profit_margin:.2f}%", delta=f"{profit_margin_delta:.2f}%")
