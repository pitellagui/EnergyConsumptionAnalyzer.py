# Residential Energy Consumption Analyzer

## Description
This web application aims to analyze and visualize residential energy consumption, helping users understand their consumption patterns and explore suggestions for cost reduction.
- [Click Here](https://energyconsumptionanalyzerpy.streamlit.app/)

## Data Input
The app allows users to either **upload a CSV file** containing monthly energy consumption data or **enter data manually**. The CSV file should include the following columns:
- `Date`
- `Time`
- `Energy Consumption (kWh)`
- `Total Cost (or average cost per kWh)`

### Features

#### Interactive Graphs:
1. **Total Daily Consumption**:  
   A bar chart displaying the total energy consumption per day, with a highlight for the highest consumption day.
   
2. **Average Hourly Consumption**:  
   A line chart showing the average consumption per hour, identifying peak hours throughout the day.

3. **Consumption Distribution**:  
   A pie chart representing the percentage breakdown of energy consumption between **peak** (6 AM - 6 PM) and **nighttime** (6 PM - 6 AM) periods.

#### Data Filtering:
- **Filter by Period**: Allows users to filter data by specific periods such as:
  - Day
  - Week
  - Month
- The filtered data displays total consumption and cost for the selected period.

#### Summary Statistics:
- Displays the **total consumption** and **total cost** for the entire dataset or the filtered period.

#### Comparative Insights:
- **Average Daily Consumption**: Compares the overall average daily consumption against the average daily consumption for the selected period.
  
This web app provides a comprehensive view of energy usage, empowering users to make informed decisions on energy saving and cost reduction.
