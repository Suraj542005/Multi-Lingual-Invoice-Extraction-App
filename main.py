from dotenv import load_dotenv
load_dotenv()
import streamlit as st
import os
from PIL import Image
import google.generativeai as genai

# Configure Gemini
genai.configure(api_key=os.getenv("API_KEY"))
model = genai.GenerativeModel('gemini-1.5-flash')


# ----- Helper Functions -----
def get_gemini_response(input_prompt, image, user_prompt):
    response = model.generate_content([input_prompt, image[0], user_prompt])
    return response.text


def input_image_details(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        image_parts = [{
            "mime_type": uploaded_file.type,
            "data": bytes_data
        }]
        return image_parts
    else:
        raise FileNotFoundError("No file Uploaded")


# ----- Streamlit UI -----
st.set_page_config(page_title="Invoice AI", page_icon="🧾", layout="wide")

# Minimal CSS for a clean look
st.markdown("""
    <style>
        .main {
            background-color: #f8f9fa;
        }
        .block-container {
            padding-top: 2rem;
        }
        .card {
            background-color: white;
            padding: 25px;
            border-radius: 12px;
            box-shadow: 0px 4px 12px rgba(0,0,0,0.05);
            margin-bottom: 20px;
        }
        .stTextInput > div > div > input {
            border-radius: 8px;
            padding: 8px;
        }
        .stFileUploader {
            border-radius: 8px;
        }
        .stButton > button {
            background-color: #4f46e5;
            color: white;
            border-radius: 8px;
            padding: 8px 18px;
            font-size: 16px;
            border: none;
        }
        .stButton > button:hover {
            background-color: #4338ca;
        }
        .result-box {
            background-color: #f1f5f9;
            padding: 15px;
            border-radius: 8px;
            margin-top: 10px;
            color: #1e293b;
            font-size: 15px;
        }
    </style>
""", unsafe_allow_html=True)


# ----- App Content -----
st.title("🧾 Invoice AI Assistant")
st.markdown("Upload an invoice image and ask questions about it. The AI will analyze the invoice and extract details for you.")

# Layout: Left (inputs) | Right (preview)
col1, col2 = st.columns([1,1])

with col1:
    user_question = st.text_input("💬 Ask something about the invoice:", key="input")
    uploaded_file = st.file_uploader("📂 Upload Invoice Image", type=["jpg", "jpeg", "png"])
    submit = st.button("🔍 Get Answer")
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="📄 Uploaded Invoice", width='stretch')
        st.markdown("</div>", unsafe_allow_html=True)

# System Prompt
input_prompt = """You are an expert in analyzing invoices. 
We will upload an invoice image and you must answer any questions 
based on the uploaded invoice image in detail and accurately."""

# Handle Response
if submit:
    if uploaded_file is None:
        st.warning("⚠️ Please upload an invoice image first!")
    else:
        image_data = input_image_details(uploaded_file)
        response = get_gemini_response(input_prompt, image_data, user_question)

        st.subheader("✅ Response")
        st.markdown(f"<div class='result-box'>{response}</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
