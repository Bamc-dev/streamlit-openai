import streamlit as st
from main import Processing
from audio_recorder_streamlit import audio_recorder

chatty = Processing(st.secrets["OPENAIKEY"])
audio_bytes = audio_recorder(pause_threshold=10.0)
translate = st.toggle("Translate")
if audio_bytes:
    with st.chat_message("assistant"):
        if translate:
            st.markdown(f"{chatty.openai_translate_audio(audio_bytes)}")
        else:
            st.markdown(f"{chatty.openai_transcribe(audio_bytes)}")