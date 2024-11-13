import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from io import StringIO

# App Title
st.title("Residential Energy Consumption Analyzer")

# Escolha de método de entrada de dados
st.subheader("Escolha como deseja inserir os dados de consumo:")
input_method = st.radio("Método de Entrada:", ("Upload de CSV", "Entrada Manual"))

# Carregamento ou criação dos dados
if input_method == "Upload de CSV":
    uploaded_file = st.file_uploader("Faça upload de um arquivo CSV", type=["csv"])
    if uploaded_file:
        data = pd.read_csv(uploaded_file)
        st.write("Dados carregados com sucesso!")
        st.write(data.head())
else:
    # Entrada Manual
    st.write("Por favor, insira os dados manualmente.")
    num_rows = st.number_input("Número de linhas:", min_value=1, step=1)

    dates = []
    consumptions = []
    costs = []

    for i in range(num_rows):
        col1, col2, col3 = st.columns(3)
        with col1:
            date = st.date_input(f"Data (Linha {i + 1}):", key=f"date_{i}")
            dates.append(date)
        with col2:
            consumption = st.number_input(f"Consumo de Energia (kWh) (Linha {i + 1}):", min_value=0.0, step=0.1,
                                          key=f"consumption_{i}")
            consumptions.append(consumption)
        with col3:
            cost = st.number_input(f"Custo Total (Linha {i + 1}):", min_value=0.0, step=0.1, key=f"cost_{i}")
            costs.append(cost)

    # Criar DataFrame com os dados inseridos manualmente
    data = pd.DataFrame({
        "Date/Time": dates,
        "Energy Consumption (kWh)": consumptions,
        "Total Cost": costs
    })

    st.write("Dados criados com sucesso!")
    st.write(data)

# Verificação se os dados estão prontos para análise
if not data.empty:
    data['Date/Time'] = pd.to_datetime(data['Date/Time'])
    data['Day'] = data['Date/Time'].dt.date
    data['Hour'] = data['Date/Time'].dt.hour

    # Summary Statistics
    total_consumption = data['Energy Consumption (kWh)'].sum()
    total_cost = data['Total Cost'].sum()
    st.subheader("Estatísticas Resumidas")
    st.write(f"Consumo Total (kWh): {total_consumption}")
    st.write(f"Custo Total: R${total_cost}")

    # Daily Consumption Graph
    daily_data = data.groupby('Day')['Energy Consumption (kWh)'].sum().reset_index()
    max_day = daily_data.loc[daily_data['Energy Consumption (kWh)'].idxmax()]
    fig_daily = px.bar(daily_data, x='Day', y='Energy Consumption (kWh)', title="Consumo Total Diário")
    fig_daily.add_annotation(x=max_day['Day'], y=max_day['Energy Consumption (kWh)'],
                             text="Maior Consumo", showarrow=True, arrowhead=1)
    st.plotly_chart(fig_daily)

    # Average Hourly Consumption Graph
    hourly_data = data.groupby('Hour')['Energy Consumption (kWh)'].mean().reset_index()
    fig_hourly = px.line(hourly_data, x='Hour', y='Energy Consumption (kWh)', title="Consumo Médio por Hora")
    st.plotly_chart(fig_hourly)

    # Consumption Distribution Pie Chart
    total_peak = data[data['Hour'].between(6, 18)]['Energy Consumption (kWh)'].sum()
    total_night = data[~data['Hour'].between(6, 18)]['Energy Consumption (kWh)'].sum()
    distribution = pd.DataFrame({
        'Category': ['Pico', 'Noturno'],
        'Consumo (kWh)': [total_peak, total_night]
    })
    fig_pie = px.pie(distribution, names='Category', values='Consumo (kWh)', title="Distribuição de Consumo")
    st.plotly_chart(fig_pie)

    # Comparative Insights
    avg_daily = daily_data['Energy Consumption (kWh)'].mean()
    st.subheader("Comparações de Consumo")
    st.write(f"Consumo Médio Diário (Conjunto de Dados): {avg_daily:.2f} kWh")
else:
    st.write("Por favor, insira dados válidos para análise.")
