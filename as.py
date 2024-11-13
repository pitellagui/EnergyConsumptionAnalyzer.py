import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime

# App Title
st.title("Residential Energy Consumption Analyzer")

# File Upload Section
st.subheader("Upload your energy consumption data")
uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

if uploaded_file:
    data = pd.read_csv(uploaded_file)

    # Assuming CSV columns: Date/Time, Energy Consumption (kWh), and Total Cost
    data['Date/Time'] = pd.to_datetime(data['Date/Time'])
    data['Day'] = data['Date/Time'].dt.date
    data['Hour'] = data['Date/Time'].dt.hour

    st.subheader("Uploaded Data Preview")
    st.write(data.head())

    # Data Filtering Section
    st.sidebar.subheader("Filter Data")
    date_range = st.sidebar.date_input("Select Date Range", [data['Day'].min(), data['Day'].max()])
    filtered_data = data[(data['Day'] >= date_range[0]) & (data['Day'] <= date_range[1])]

    # Summary Statistics
    total_consumption = filtered_data['Energy Consumption (kWh)'].sum()
    total_cost = filtered_data['Total Cost'].sum()
    st.subheader("Summary Statistics")
    st.write(f"Total Consumption (kWh): {total_consumption}")
    st.write(f"Total Cost: ${total_cost}")

    # Daily Consumption
    daily_data = filtered_data.groupby('Day')['Energy Consumption (kWh)'].sum().reset_index()
    max_day = daily_data.loc[daily_data['Energy Consumption (kWh)'].idxmax()]
    fig_daily = px.bar(daily_data, x='Day', y='Energy Consumption (kWh)', title="Total Daily Consumption")
    fig_daily.add_annotation(x=max_day['Day'], y=max_day['Energy Consumption (kWh)'],
                             text="Highest Consumption", showarrow=True, arrowhead=1)
    st.plotly_chart(fig_daily)

    # Average Hourly Consumption
    hourly_data = filtered_data.groupby('Hour')['Energy Consumption (kWh)'].mean().reset_index()
    fig_hourly = px.line(hourly_data, x='Hour', y='Energy Consumption (kWh)', title="Average Hourly Consumption")
    st.plotly_chart(fig_hourly)

    # Consumption Distribution
    total_peak = filtered_data[filtered_data['Hour'].between(6, 18)]['Energy Consumption (kWh)'].sum()
    total_night = filtered_data[~filtered_data['Hour'].between(6, 18)]['Energy Consumption (kWh)'].sum()
    distribution = pd.DataFrame({
        'Category': ['Peak', 'Nighttime'],
        'Consumption (kWh)': [total_peak, total_night]
    })
    fig_pie = px.pie(distribution, names='Category', values='Consumption (kWh)', title="Consumption Distribution")
    st.plotly_chart(fig_pie)

    # Comparative Insights
    avg_daily = daily_data['Energy Consumption (kWh)'].mean()
    selected_avg = filtered_data.groupby('Day')['Energy Consumption (kWh)'].mean().mean()
    st.subheader("Comparative Insights")
    st.write(f"Average Daily Consumption (Entire Dataset): {avg_daily:.2f} kWh")
    st.write(f"Average Daily Consumption (Selected Period): {selected_avg:.2f} kWh")

else:
    st.write("Please upload a CSV file to begin analysis.")
