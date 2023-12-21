import streamlit as st

from prediction_page import prediction_page
from chart_page import chart_page

st.set_page_config(page_title="Laptop Price Predictor", page_icon="💻", layout="wide")

prediction_page()