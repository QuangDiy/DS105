import streamlit as st
import pandas as pd
import plotly.express as px

def plot_histogram(file_path, x_column, color_column):
    df = pd.read_csv(file_path)

    fig = px.histogram(df, x=x_column, color=color_column)
    fig.update_layout(title='Count plot')

    st.plotly_chart(fig)

def chart_page():
    st.title("Laptop Price Chart 📊")
    
    file_path = "data/ds105.csv"
    x_column = "Laptop Brand"
    color_column = "Laptop Brand"

    col1, col2 = st.columns(2)

    with col1:
        plot_histogram(file_path, x_column, color_column)

    with col2:
        plot_histogram(file_path, x_column, color_column)