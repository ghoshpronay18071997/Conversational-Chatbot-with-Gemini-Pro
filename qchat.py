from dotenv import load_dotenv
load_dotenv()
import os
import streamlit as st
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

model = genai.GenerativeModel(os.getenv("MODEL_NAME"))
chat = model.start_chat(history=[])

def get_gemini_response(question):
    """Get response from Gemini Pro model based on the user question given"""
    response = chat.send_message(question, stream=True)
    return response

st.header("Gemini LLM Application")

# We are creating session so that we can record the chat history if it doesnt exist
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

input__ = st.text_input("Input: ", key = "input__")
submit = st.button("Ask the question")


if submit and input__:
    resp =  get_gemini_response(input__)
    ## Add a user query and response into a session chat history
    st.session_state['chat_history'].append(["You",input__])
    st.subheader("The Response is : ")
    for chunk in resp:
        st.write(chunk.text)
        st.session_state['chat_history'].append(["Bot",chunk.text])

st.subheader("The Chat history is:")

for role, text in st.session_state['chat_history']:
    st.write(f"{role}:{text}")