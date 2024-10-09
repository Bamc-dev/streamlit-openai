import streamlit as st
from main import Processing
import time

st.set_page_config(page_title="OpenAI - WebApp", page_icon=":sunglasses:")

st.header("Welcome on my own ChatGPT")

chatty = Processing(st.secrets["OPENAIKEY"])
options = st.selectbox(
    "Select the model",
    ("Translate", "Summary", "Text Generator", "Code Helper"),
    index=None,
)
@st.dialog("Format of prompts : ", width="large")
def notify():
    st.header("Use this : ")
    st.text("Theme : Describe the theme, Content : Describe the content")
if(options == "Text Generator"):
    notify()
prompt = st.chat_input("Say something")
if prompt:
    with st.chat_message("user"):
        st.markdown(prompt)
    match options:
        case "Translate":
            with st.chat_message("assistant"):
                st.markdown(chatty.openai_translate(prompt))
        case "Summary":
            with st.chat_message("assistant"):
                st.markdown(chatty.openai_text_summary(prompt))
        case "Text Generator":
             with st.chat_message("assistant"):
                st.markdown(chatty.openai_text_gen(prompt))
        case "Code helper":
            with st.chat_message("assistant"):
                st.markdown(chatty.openai_codex(prompt))

