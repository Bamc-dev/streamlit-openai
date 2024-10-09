import streamlit as st
from main import Processing

chatty = Processing(st.secrets["OPENAIKEY"])
prompt = st.chat_input("Say something")
if prompt:
    with st.chat_message("user"):
        st.markdown(prompt)
    with st.chat_message("assistant"):
        st.markdown(f"![Result]({chatty.openai_create_image(prompt)})")