from dotenv import load_dotenv
load_dotenv()

import os
import google.generativeai as genai 
import streamlit as st

genai.configure(api_key=os.getenv("OOGLE_API_KEY"))
model=genai.GenerativeModel("gemini-pro")
chat=model.start_chat(history=[])

def get_gemini_response(question):
    response=chat.send_message(question,stram=True)
    return response

st.set_page_config("Q&A Chatbot")
st.header("conversational chatbot")

if 'chat_history' not in st.session_state:
    st.session_state['chat_history']=[]

input=st.text_input("input: ",key="input")
submit=st.button("send")

if input and submit:
    response=get_gemini_response(input)
    st.session_state['chat_history'].append(("you",input))
    st.subheader("response:")
    for chunk in response:
        st.write(chunk.text)
        st.response_state['chat_history'].append(("response",chunk.text))

st.subheader("chat history:")
for role, response in st.session_state['chat_history']:
    st.write(f"{role}:{response}")
