import streamlit as st
from assistant import get_response
import pyttsx3

# Initialize TTS engine
engine = pyttsx3.init()

st.set_page_config(page_title="Eva - Voice Assistant", page_icon="🎧")
st.title("🎙️ Eva - Your AI Voice Assistant")
st.markdown("Ask Eva anything — from weather to jokes to reminders!")

# User input
user_input = st.text_input("🗨️ Type your question or command for Eva:")

if st.button("Ask Eva"):
    if user_input:
        with st.spinner("Eva is thinking..."):
            response = get_response(user_input)
            st.success("Eva says:")
            st.write(response)

            # Speak the response
            engine.say(response)
            engine.runAndWait()
    else:
        st.warning("Please enter a message for Eva.")
