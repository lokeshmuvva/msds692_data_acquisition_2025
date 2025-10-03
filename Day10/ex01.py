import os
from dotenv import load_dotenv

import streamlit as st
import google.generativeai as genai

load_dotenv(
    dotenv_path="/Users/lokeshmuvva/Documents/F25_1/msds692_data_acquisition_2025/Day10/.env"
    )

model = genai.GenerativeModel("gemini-2.5-flash")
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
chat = model.start_chat()

st.set_page_config(page_title="Chatbot")
st.title("Interactive Chatbot with Google GenAI")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display existing messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])


prompt = st.chat_input("Ask me something...")
if prompt:
    # Save user message
    st.session_state.messages.append({"role": "user",
                                      "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Stream assistant response
    with st.chat_message("assistant"):
        placeholder = st.empty()
        RESPONSE_TEXT = " "

        # Streaming from API
        response = chat.send_message(prompt, stream=True)

    for chunk in response:
        RESPONSE_TEXT += chunk.text
        placeholder.markdown(RESPONSE_TEXT)

    # Save assistant message
    st.session_state.messages.append(
        {"role": "assistant", "content": RESPONSE_TEXT})
