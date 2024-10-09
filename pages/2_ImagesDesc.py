import streamlit as st
from main import Processing

chatty = Processing(st.secrets["OPENAIKEY"])
uploaded_file = st.file_uploader("Choose an image")
if uploaded_file is not None:
    with st.chat_message("assistant"):
        st.markdown(f"{chatty.vision_analyze_image(uploaded_file.getvalue())}")