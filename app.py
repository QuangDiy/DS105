import streamlit as st

from prediction_page import prediction_page
from chart_page import chart_page

st.set_page_config(page_title="Laptop Price Predictor", page_icon="💻", layout="wide")

# sidebar = st.sidebar
# sidebar.title("Navigation")
# page = sidebar.radio("Go to", ("Prediction", "Chart"))

# if page == "Prediction":
#     prediction_page()
# else:
#     chart_page()

prediction_page()