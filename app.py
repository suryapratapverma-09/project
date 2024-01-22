from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os
from PIL import Image  # Python image library
import google.generativeai as genai

genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))

model = genai.GenerativeModel('gemini-pro-vision')


def get_gemini_response(input, image_data, user_prompt):
    response = model.generate_content([input, image_data[0], user_prompt])
    return response.text


def input_image_details(upload_file):
    if uploaded_file is not None:
        try:
            bytes_data = uploaded_file.getvalue()
            image_parts = [{
                'mime_type': uploaded_file.type,
                'data': bytes_data
            }]
            return image_parts
        except Exception as e:
            st.error(f"Error processing the uploaded file: {str(e)}")
            return None
    else:
        st.warning('Please upload an image.')
        return None


st.header('Multilanguage invoice Extractor')

input = st.text_input('Input Prompt', key='input')
uploaded_file = st.file_uploader('Image', type=['jpg', 'jpeg', 'png'])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='uploaded File', use_column_width=True)

sub = st.button('Tell me about the invoice')

input_prompt = """you are expert in understanding invoices.
we will upload an image as an invoice and you will have to answer any
questions based on the uploaded invoice image."""

if sub:
    with st.spinner('Wait'):
        image_data = input_image_details(uploaded_file)
        if image_data:
            response = get_gemini_response(input_prompt, image_data, input)
            st.subheader('The response is')
            st.text_area(label="", value=response, height=500)

