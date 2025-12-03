import streamlit as st
from openai import OpenAI
import pandas as pd
import os
from dotenv import load_dotenv
import warnings

# Suppress warnings
warnings.filterwarnings('ignore')

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="GEEKATHON F-25 | TMUC",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for the theme
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #312e81 0%, #7e22ce 50%, #be185d 100%);
    }
    
    /* Top bar header styling */
    .top-header {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        background: rgba(255, 255, 255, 0.98);
        backdrop-filter: blur(10px);
        padding: 1rem 2rem;
        border-bottom: 3px solid #a855f7;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
        z-index: 1000;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    
    .header-left-content {
        display: flex;
        align-items: center;
        gap: 1.5rem;
    }
    
    .tmuc-logo {
        height: 50px;
        width: auto;
    }
    
    .header-title-main {
        color: #312e81;
        font-size: 1.8rem;
        font-weight: bold;
        margin: 0;
    }
    
    .header-subtitle-main {
        color: #7e22ce;
        font-size: 0.9rem;
        margin: 0;
    }
    
    .director-badge-top {
        background: linear-gradient(135deg, #8b5cf6 0%, #6366f1 100%);
        color: white;
        padding: 0.5rem 1.2rem;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.85rem;
        box-shadow: 0 4px 12px rgba(139, 92, 246, 0.3);
        white-space: nowrap;
    }
    
    /* Main content with margin for fixed header */
    .main-content {
        margin-top: 100px;
        padding: 1rem 2rem;
    }
    
    .bot-info-container {
        background: rgba(255, 255, 255, 0.12);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.25);
        border-radius: 20px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        text-align: center;
    }
    
    .bot-title {
        color: #fbbf24;
        font-size: 1.8rem;
        font-weight: bold;
        margin: 0;
        text-shadow: 0 2px 8px rgba(251, 191, 36, 0.5);
    }
    
    .bot-subtitle {
        color: #e9d5ff;
        font-size: 1rem;
        margin: 0.5rem 0 0 0;
    }
    
    .chat-container {
        background: rgba(255, 255, 255, 0.08);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        min-height: 400px;
        max-height: 450px;
        overflow-y: auto;
        border: 1px solid rgba(255, 255, 255, 0.15);
        box-shadow: inset 0 2px 10px rgba(0, 0, 0, 0.2);
    }
    
    .chat-container::-webkit-scrollbar {
        width: 8px;
    }
    
    .chat-container::-webkit-scrollbar-track {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 10px;
    }
    
    .chat-container::-webkit-scrollbar-thumb {
        background: rgba(168, 85, 247, 0.5);
        border-radius: 10px;
    }
    
    .chat-container::-webkit-scrollbar-thumb:hover {
        background: rgba(168, 85, 247, 0.7);
    }
    
    .user-message {
        background: linear-gradient(135deg, #34d399 0%, #3b82f6 100%);
        color: white;
        padding: 1.2rem;
        border-radius: 18px;
        margin: 0.8rem 0;
        margin-left: 15%;
        word-wrap: break-word;
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
        animation: slideInRight 0.3s ease-out;
    }
    
    .assistant-message {
        background: rgba(255, 255, 255, 0.12);
        border: 1px solid rgba(255, 255, 255, 0.25);
        color: white;
        padding: 1.2rem;
        border-radius: 18px;
        margin: 0.8rem 0;
        margin-right: 15%;
        word-wrap: break-word;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
        animation: slideInLeft 0.3s ease-out;
    }
    
    @keyframes slideInRight {
        from {
            opacity: 0;
            transform: translateX(20px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    @keyframes slideInLeft {
        from {
            opacity: 0;
            transform: translateX(-20px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    .stTextInput > div > div > input {
        background: rgba(255, 255, 255, 0.95) !important;
        border: 2px solid rgba(168, 85, 247, 0.3) !important;
        border-radius: 25px !important;
        color: #1f2937 !important;
        padding: 0.9rem 1.5rem !important;
        font-size: 1rem !important;
    }
    
    .stTextInput > div > div > input::placeholder {
        color: #6b7280 !important;
        opacity: 0.7 !important;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: rgba(168, 85, 247, 0.6) !important;
        box-shadow: 0 0 0 3px rgba(168, 85, 247, 0.2) !important;
    }
    
    .stButton button {
        background: linear-gradient(135deg, #a855f7 0%, #ec4899 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 25px !important;
        padding: 0.9rem 2.5rem !important;
        font-weight: bold !important;
        font-size: 1rem !important;
        transition: all 0.3s !important;
        box-shadow: 0 4px 15px rgba(168, 85, 247, 0.4) !important;
    }
    
    .stButton button:hover {
        background: linear-gradient(135deg, #9333ea 0%, #db2777 100%) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(168, 85, 247, 0.6) !important;
    }
    
    [data-testid="stHeader"] {
        background: transparent !important;
    }
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    .status-success {
        background: rgba(52, 211, 153, 0.25);
        border: 1px solid rgba(52, 211, 153, 0.6);
        color: #6ee7b7;
        padding: 0.7rem 1.2rem;
        border-radius: 12px;
        margin: 0.5rem 0;
        font-size: 0.95rem;
        font-weight: 500;
        box-shadow: 0 2px 8px rgba(52, 211, 153, 0.2);
    }
    
    .status-warning {
        background: rgba(251, 191, 36, 0.25);
        border: 1px solid rgba(251, 191, 36, 0.6);
        color: #fbbf24;
        padding: 0.7rem 1.2rem;
        border-radius: 12px;
        margin: 0.5rem 0;
        font-size: 0.95rem;
        font-weight: 500;
        box-shadow: 0 2px 8px rgba(251, 191, 36, 0.2);
    }
    
    .status-error {
        background: rgba(239, 68, 68, 0.25);
        border: 1px solid rgba(239, 68, 68, 0.6);
        color: #fca5a5;
        padding: 0.7rem 1.2rem;
        border-radius: 12px;
        margin: 0.5rem 0;
        font-size: 0.95rem;
        font-weight: 500;
        box-shadow: 0 2px 8px rgba(239, 68, 68, 0.2);
    }
    
    .custom-footer {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 1.5rem;
        text-align: center;
        margin-top: 2rem;
        border: 1px solid rgba(255, 255, 255, 0.15);
    }
    
    .footer-text {
        color: #e9d5ff;
        font-size: 1rem;
        margin: 0;
    }
    
    .footer-name {
        color: #fbbf24;
        font-weight: bold;
        font-size: 1.1rem;
    }
    
    div[data-testid="stExpander"] {
        background: rgba(255, 255, 255, 0.08);
        border: 1px solid rgba(255, 255, 255, 0.15);
        border-radius: 15px;
        backdrop-filter: blur(10px);
    }
    
    div[data-testid="stExpander"] summary {
        color: white !important;
        font-weight: 600;
    }
    
    /* Hide Streamlit warnings */
    div[data-testid="stException"] {
        display: none !important;
    }
    
    div[data-testid="stNotification"] {
        display: none !important;
    }
    
    .stAlert {
        display: none !important;
    }
</style>
""", unsafe_allow_html=True)

# Top Header Bar
st.markdown("""
<div class="top-header">
    <div class="header-left-content">
        <img src="https://tmuc.edu.pk/wp-content/uploads/2020/07/TMUC-logo.png" alt="TMUC Logo" class="tmuc-logo" onerror="this.style.display='none'">
        <div>
            <div class="header-title-main">🤖 GEEKATHON F-25</div>
            <div class="header-subtitle-main">AI-Powered Event Assistant</div>
        </div>
    </div>
    
</div>
""", unsafe_allow_html=True)

# Main content container
st.markdown('<div class="main-content">', unsafe_allow_html=True)

# Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Welcome to GEEKATHON F-25! 🎉 I'm here to help you with event details, venue information, and student project queries. How can I assist you today?"}
    ]

if 'event_details' not in st.session_state:
    st.session_state.event_details = None

if 'projects_data' not in st.session_state:
    st.session_state.projects_data = None

if 'should_process' not in st.session_state:
    st.session_state.should_process = False

if 'current_input' not in st.session_state:
    st.session_state.current_input = ""

# Load data from files
@st.cache_data
def load_event_details():
    try:
        with open('EVENT_DETAILS.txt', 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        return None

@st.cache_data
def load_projects_data():
    try:
        df = pd.read_excel('Geekathon_Project.xlsx')
        return df
    except FileNotFoundError:
        return None

# Load API key and data
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
client = None
if OPENAI_API_KEY:
    client = OpenAI(api_key=OPENAI_API_KEY)

if st.session_state.event_details is None:
    st.session_state.event_details = load_event_details()

if st.session_state.projects_data is None:
    st.session_state.projects_data = load_projects_data()

# Bot Info Section
st.markdown("""
<div class="bot-info-container">
    <div class="bot-title">🤖 GEEKATHON Assistant</div>
    <div class="bot-subtitle">Powered by M.Mujtaba Raza | Ask me about event details, venue, schedule, and student projects!</div>
</div>
""", unsafe_allow_html=True)

# Status indicators
col1, col2, col3 = st.columns(3)
with col1:
    if OPENAI_API_KEY:
        st.markdown('<div class="status-success">✓ API Key Loaded</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="status-error">⚠️ API Key not found</div>', unsafe_allow_html=True)

with col2:
    if st.session_state.event_details:
        st.markdown('<div class="status-success">✓ Event Details Loaded</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="status-warning">⚠️ EVENT_DETAILS.txt not found</div>', unsafe_allow_html=True)

with col3:
    if st.session_state.projects_data is not None:
        st.markdown('<div class="status-success">✓ Projects Data Loaded</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="status-warning">⚠️ Geekathon_Project.xlsx not found</div>', unsafe_allow_html=True)

# Chat display
st.markdown('<div class="chat-container">', unsafe_allow_html=True)
for message in st.session_state.messages:
    if message["role"] == "user":
        st.markdown(f'<div class="user-message">👤 {message["content"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="assistant-message">🤖 {message["content"]}</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Function to handle input change
def on_input_change():
    st.session_state.should_process = True
    st.session_state.current_input = st.session_state.user_input_field

# Chat input with Enter key support
col1, col2 = st.columns([5, 1])
with col1:
    user_input = st.text_input(
        "Ask me about GEEKATHON F-25...", 
        key="user_input_field",
        label_visibility="collapsed", 
        placeholder="Type your question here and press Enter...",
        on_change=on_input_change
    )
with col2:
    send_button = st.button("Send 📤")

# Process message after input or button click
if (st.session_state.should_process or send_button) and st.session_state.current_input and client:
    user_message = st.session_state.current_input
    st.session_state.messages.append({"role": "user", "content": user_message})
    
    context_info = ""
    
    if st.session_state.event_details:
        context_info += f"\n\nEvent Details:\n{st.session_state.event_details}\n"
    
    if st.session_state.projects_data is not None:
        context_info += f"\n\nStudent Projects Data:\n{st.session_state.projects_data.to_string()}\n"
    
    system_prompt = f"""You are a helpful assistant EXCLUSIVELY for GEEKATHON F-25 event at TMUC (The Millennium Universal College).

STRICT RULES:
1. ONLY answer questions related to:
   - GEEKATHON F-25 event details
   - Venue information and directions
   - Schedule and timings
   - Student project information from the provided data
   - TMUC campus-related questions
   
2. DO NOT answer questions about:
   - General knowledge topics (like products, recipes, beauty items, etc.)
   - Topics unrelated to the event
   - Personal advice
   - Any subject not in the provided event/project data

3. If asked about something unrelated, politely respond: "I can only help with GEEKATHON F-25 event information, venue details, and student projects. Please ask questions related to the event!"

{context_info}

Provide friendly, concise, and accurate responses ONLY about the event. Stay within the scope of GEEKATHON F-25."""
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                *st.session_state.messages[-6:]
            ],
            temperature=0.5,
            max_tokens=400
        )
        
        assistant_message = response.choices[0].message.content
        st.session_state.messages.append({"role": "assistant", "content": assistant_message})
        
    except Exception as e:
        error_msg = f"Sorry, I encountered an error: {str(e)}. Please check your API key and try again."
        st.session_state.messages.append({
            "role": "assistant", 
            "content": error_msg
        })
    
    # Reset states
    st.session_state.should_process = False
    st.session_state.current_input = ""
    st.rerun()

elif (st.session_state.should_process or send_button) and not client:
    st.markdown('<div class="status-error">⚠️ Please add your OPENAI_API_KEY to the .env file</div>', unsafe_allow_html=True)
    st.session_state.should_process = False

# Instructions
with st.expander("📋 Purpose of this Chatbot"):
    st.markdown("""
```bash
    **EVENT_DETAILS**:
    A Chatbot is designed for the guest to get the relevant information about the GEEKATHON F-25 event, including schedule, venue details, and other important notes.

    **Designe by:**:    
    - Muhammad Mujtaba Raza    
    """)

# Custom Footer
st.markdown("""
<div class="custom-footer">
    <p class="footer-text">Designed by <span class="footer-name">Muhammad Mujtaba Raza</span></p>
    <p class="footer-text" style="font-size: 0.9rem; margin-top: 0.5rem;">Director Computing | GEEKATHON F-25 @ TMUC</p>
</div>
""", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)