import streamlit as st
from main import Processing
st.set_page_config(page_title="OpenAI - WebApp", page_icon=":sunglasses:")

st.header("Welcome on my own ChatGPT")

chatty = Processing(st.secrets["OPENAIKEY"])

options = st.selectbox(
    "Select the model",
    ("Model1", "Model2", "Model3", "Model4"),
    index=None,
)
