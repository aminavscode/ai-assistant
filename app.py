import os
import streamlit as st
from dotenv import load_dotenv
from groq import Groq

# Load environment variables from .env file
load_dotenv()

# Page Config
st.set_page_config(page_title="SmartStudy AI", page_icon="📚", layout="centered")

# Custom Styling
st.markdown("""
    <style>
    .stApp { background-color: #f8f9fa; }
    .main-header { color: #4A4E69; text-align: center; font-weight: 700; }
    .sub-header { color: #6C5CE7; text-align: center; margin-bottom: 20px; }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1 class='main-header'>📚 SmartStudy AI</h1>", unsafe_allow_html=True)
st.markdown("<p class='sub-header'>Paste your study topic or notes below to generate instant summaries, definitions, and quizzes!</p>", unsafe_allow_html=True)

# Fetch API key from .env file first, or sidebar as fallback
api_key = os.getenv("GROQ_API_KEY") or st.sidebar.text_input("Enter Groq API Key:", type="password")

# Input Area
user_input = st.text_area("Paste study notes or topics here:", height=150, placeholder="e.g. Mass Spectroscopy, Photosynthesis, Cell Division...")

if st.button("Generate Study Plan & Quiz", type="primary"):
    if not api_key:
        st.error("Error: Groq API Key nahi mili! `.env` file checks karein ya Sidebar mein daalein.")
    elif not user_input.strip():
        st.warning("Please enter a topic or notes first.")
    else:
        try:
            client = Groq(api_key=api_key)
            
            prompt = f"""
            You are an expert AI tutor. Analyze the following content and provide a response in clear Markdown format with three sections:
            
            1. ## Concise Summary
            Provide a clear, easy-to-understand 3-4 sentence summary of the topic.
            
            2. ## Key Definitions
            List 3 key terms from the topic with short, bold definitions.
            
            3. ## 5-Question Quiz
            Create a 5-question Multiple Choice Quiz (MCQ) based on the topic. For each question, list 4 options (A, B, C, D) and specify the Correct Answer with a brief 1-line explanation.
            
            Topic/Notes provided:
            {user_input}
            """
            
            with st.spinner("SmartStudy AI aap ke notes generate kar raha hai..."):
                response = client.chat.completions.create(
                    messages=[{"role": "user", "content": prompt}],
                    model="openai/gpt-oss-120b"
                )
                
                st.success("Tayar ho gaya!")
                st.markdown(response.choices[0].message.content)
                
        except Exception as e:
            st.error(f"Error aaya hai: {e}")