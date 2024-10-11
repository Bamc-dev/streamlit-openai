import streamlit as st
from main import Processing

chatty = Processing(st.secrets["OPENAIKEY"])
chattyResponse = None
audio = st.experimental_audio_input('Traducteur automatique')
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.content_to_generate = ""
if audio:
    chattyResponse = chatty.openai_transcribe(audio.getvalue())
    st.session_state.messages.append({"role": "user", "content": chattyResponse})
    st.session_state.content_to_generate += chattyResponse
    st.session_state.messages.append({"role" : "assistant", 
                                      "content":f"![Result]({chatty.openai_create_image(chatty.generate_prompt_with_chatgpt(
                                          st.session_state.content_to_generate))})"})
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

