import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Residential Energy Consumption Analyzer", layout="centered")

st.markdown("""
    <style>
        .main {
            background-color: #f4f4f9;
        }
        .css-1v3fvcr {
            font-size: 1.5rem;
            color: #4a90e2;
        }
        .css-15tx938 {
            color: #4a90e2;
            font-weight: bold;
        }
        .header {
            background-color: #4a90e2;
            color: white;
            padding: 10px;
            text-align: center;
        }
        .stRadio>div>label {
            font-size: 16px;
            color: #4a90e2;
        }
    </style>
""", unsafe_allow_html=True)

st.title("Residential Energy Consumption Analyzer 🔋")

st.subheader("Select how you would like to enter consumption data:")

input_method = st.radio("Input Method:", ("CSV Upload", "Manual Entry"), key="input_method")

data = pd.DataFrame()

if input_method == "CSV Upload":
    uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])
    if uploaded_file:
        try:
            data = pd.read_csv(uploaded_file)
            st.success("Data uploaded successfully! ✅")
            st.write(data)

            if 'Date' not in data.columns:
                st.error("Error: The CSV file does not contain a 'Date' column.")
            else:
                data['Day'] = pd.to_datetime(data['Date'], errors='coerce').dt.date
                data['Hour'] = pd.to_datetime(data['Time'], errors='coerce').dt.hour

        except Exception as e:
            st.error(f"Error reading the CSV file: {e}")

else:
    st.info("Please enter data manually.")
    num_rows = st.number_input("Number of entries:", min_value=1, step=1)

    dates = []
    hours = []
    consumptions = []
    costs = []

    for i in range(num_rows):
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            date = st.date_input(f"Date:", key=f"date_{i}")
            dates.append(date)
        with col2:
            hour = st.time_input(f"Time:", key=f"time_{i}")
            hours.append(hour)
        with col3:
            consumption = st.number_input(f"Energy Consumption (kWh):", min_value=0.0, step=0.1,
                                          key=f"consumption_{i}")
            consumptions.append(consumption)
        with col4:
            cost = st.number_input(f"Total Cost:", min_value=0.0, step=0.1, key=f"cost_{i}")
            costs.append(cost)

    data = pd.DataFrame({
        "Date": dates,
        "Time": hours,
        "Energy Consumption (kWh)": consumptions,
        "Total Cost ($)": costs
    })

    data['Date/Time'] = pd.to_datetime(data['Date'].astype(str) + ' ' + data['Time'].astype(str))
    data['Day'] = data['Date/Time'].dt.date
    data['Hour'] = data['Date/Time'].dt.hour

    st.success("Data created successfully! ✅")

if not data.empty:
    if 'Date' in data.columns:
        total_consumption = data['Energy Consumption (kWh)'].sum()
        total_cost = data['Total Cost ($)'].sum()

        st.subheader("Summary Statistics 📊 ")
        st.write(f"**Total Consumption (kWh):** {total_consumption}")
        st.write(f"**Total Cost ($):** {total_cost:.2f}")

        daily_data = data.groupby('Day')['Energy Consumption (kWh)'].sum().reset_index()
        max_day = daily_data.loc[daily_data['Energy Consumption (kWh)'].idxmax()]

        fig_daily = px.bar(daily_data, x='Day', y='Energy Consumption (kWh)', title="Daily Total Consumption",
                           color='Energy Consumption (kWh)', color_continuous_scale="Viridis")
        fig_daily.add_annotation(x=max_day['Day'], y=max_day['Energy Consumption (kWh)'],
                                 text="Highest Consumption", showarrow=True, arrowhead=1)
        st.plotly_chart(fig_daily)

        hourly_data = data.groupby('Hour')['Energy Consumption (kWh)'].mean().reset_index()
        fig_hourly = px.line(hourly_data, x='Hour', y='Energy Consumption (kWh)', title="Average Hourly Consumption")
        st.plotly_chart(fig_hourly)

        total_peak = data[data['Hour'].between(6, 18)]['Energy Consumption (kWh)'].sum()
        total_night = data[~data['Hour'].between(6, 18)]['Energy Consumption (kWh)'].sum()

        distribution = pd.DataFrame({
            'Category': ['Peak', 'Night'],
            'Consumption (kWh)': [total_peak, total_night]
        })

        fig_pie = px.pie(distribution, names='Category', values='Consumption (kWh)', title="Consumption Distribution",
                         color_discrete_sequence=["#FF7F0E", "#1F77B4"])
        st.plotly_chart(fig_pie)

        avg_daily = daily_data['Energy Consumption (kWh)'].mean()

        st.subheader("Consumption Comparisons 📉")
        st.write(f"**Average Daily Consumption (Dataset):** {avg_daily:.2f} kWh")

        filter_option = st.radio("Filter data by period:", ("None", "Day", "Week", "Month"))

        if filter_option != "None":
            if filter_option == "Day":
                selected_day = st.date_input("Select a day to filter by:", min_value=data['Day'].min(), max_value=data['Day'].max())
                filtered_data = data[data['Day'] == pd.to_datetime(selected_day).date()]
            elif filter_option == "Week":
                selected_week = st.date_input("Select a week start date:", min_value=data['Day'].min(), max_value=data['Day'].max())
                start_date = pd.to_datetime(selected_week)
                end_date = start_date + pd.DateOffset(days=6)
                filtered_data = data[(data['Day'] >= start_date.date()) & (data['Day'] <= end_date.date())]
            elif filter_option == "Month":
                selected_month = st.selectbox("Select a month to filter by:", pd.to_datetime(data['Day']).dt.month.unique())
                filtered_data = data[pd.to_datetime(data['Day']).dt.month == selected_month]

            if not filtered_data.empty:
                st.write(f"Showing data for the selected {filter_option.lower()}:")
                st.write(filtered_data)

                total_filtered_consumption = filtered_data['Energy Consumption (kWh)'].sum()
                total_filtered_cost = filtered_data['Total Cost ($)'].sum()

                st.write(f"**Total Consumption (kWh) in selected period:** {total_filtered_consumption}")
                st.write(f"**Total Cost ($) in selected period:** {total_filtered_cost:.2f}")

                avg_filtered_daily = filtered_data.groupby('Day')['Energy Consumption (kWh)'].sum().mean()
                st.write(f"**Average Daily Consumption in selected period:** {avg_filtered_daily:.2f} kWh")

                fig_filtered = px.bar(filtered_data.groupby('Day')['Energy Consumption (kWh)'].sum().reset_index(), 
                                      x='Day', y='Energy Consumption (kWh)', title=f"Total Consumption in Selected {filter_option}",
                                      color='Energy Consumption (kWh)', color_continuous_scale="Viridis")
                st.plotly_chart(fig_filtered)
            else:
                st.warning(f"No data found for the selected {filter_option.lower()} period.")
        else:
            st.write("No period filter selected.")
else:
    st.warning("Please enter valid data for analysis. ⚠️")
