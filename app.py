import os
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq
import streamlit as st

# 1. Page Config
st.set_page_config(page_title="Personal Portfolio", page_icon="📄")

# Wallpaper URLs
desktop_wallpaper_url = "https://i.pinimg.com/736x/22/b2/a5/22b2a517f6b2953cefe9a1e9d6f0f8e8.jpg"
mobile_wallpaper_url = "https://i.pinimg.com/1200x/6d/be/ae/6dbeae2d7f877e9b22b0e1d204037235.jpg" 

# CSS with Desktop/Mobile Breakpoints
page_bg_img = f"""
<style>
/* ========================================================= */
/* 1. DESKTOP STYLING (min-width: 769px) */
/* ========================================================= */
[data-testid="stAppViewContainer"] {{
    background-image: url("{desktop_wallpaper_url}") !important;
    background-size: cover !important;
    background-position: center !important;
    background-repeat: no-repeat !important;
    background-attachment: fixed !important; 
}}

/* Glassy Sidebar Styling */
[data-testid="stSidebar"] {{
    background-color: rgba(18, 18, 18, 0.45) !important;
    backdrop-filter: blur(12px) saturate(160%) !important;
    -webkit-backdrop-filter: blur(12px) saturate(160%) !important;
    border-right: 1px solid rgba(255, 255, 255, 0.1) !important;
}}

/* Inner sidebar container background cleanup */
[data-testid="stSidebar"] > div:first-child {{
    background: transparent !important;
}}

/* Centered & Max-Width Card for Desktop PC */
@media screen and (min-width: 769px) {{
    [data-testid="stAppViewBlockContainer"] {{
        max-width: 800px !important;
        margin: 2rem auto !important;
        padding: 2.5rem !important;
        background-color: rgba(18, 18, 18, 0.85) !important;
        border-radius: 16px !important;
        border: 1px solid rgba(255, 255, 255, 0.12) !important;
    }}
}}

[data-testid="stHeader"], [data-testid="stBottom"] > div {{
    background-color: transparent !important;
}}

/* Chat Bubbles */
[data-testid="stChatMessage"] {{
    background-color: rgba(30, 30, 30, 0.75) !important;
    border-radius: 12px !important;
    padding: 0.8rem 1rem !important;
    margin-bottom: 0.75rem !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
}}

/* Typography & Interactive Elements */
.stMarkdown, p, h1, h2, h3, h4, span, label {{
    color: #FFFFFF !important;
}}

button {{
    border: 1px solid rgba(255, 255, 255, 0.2) !important;
    background-color: rgba(0, 0, 0, 0.6) !important;
    border-radius: 8px !important;
}}

/* Sidebar Elements */
[data-testid="stSidebar"] img {{
    max-width: 100% !important;
    height: auto !important;
}}

/* ========================================================= */
/* 2. MOBILE STYLING (max-width: 768px) */
/* ========================================================= */
@media screen and (max-width: 768px) {{
    [data-testid="stAppViewContainer"] {{
        background-image: url("{mobile_wallpaper_url}") !important;
        background-attachment: scroll !important; 
        background-position: top center !important;
    }}

    [data-testid="stAppViewBlockContainer"] {{
        padding: 1rem 0.8rem !important;
        margin-top: 0.5rem !important;
        margin-bottom: 0.5rem !important;
        background-color: rgba(18, 18, 18, 0.88) !important;
        border-radius: 12px !important;
    }}

    [data-testid="stChatMessage"] {{
        padding: 0.6rem 0.75rem !important;
        margin-bottom: 0.5rem !important;
    }}

    h3 {{
        font-size: 1.2rem !important;
    }}
    p, span, label {{
        font-size: 0.9rem !important;
    }}
}}
</style>
"""

st.markdown(page_bg_img, unsafe_allow_html=True)


# API & Data Caching
@st.cache_resource
def get_groq_client():
    load_dotenv()
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        st.error("Groq API key not found. Please check your .env file.")
        st.stop()
    return Groq(api_key=api_key)

@st.cache_data
def load_profile():
    profile_path = Path("about_me.md")
    if profile_path.exists():
        return profile_path.read_text()
    return "Profile information is currently unavailable."

client = get_groq_client()
profile = load_profile()
model = "llama-3.3-70b-versatile"

system_prompt = f"""
You are an AI personal portfolio assistant.
Represent the user professionally using only the context below:
{profile}
"""

with st.sidebar:
    st.image("profile.png", use_container_width=True)
    st.title("Rajat Tyagi")
    st.download_button(
        label="Download Resume",
        data="Your actual resume content or read from a file",
        file_name="Rajat_Tyagi_Resume.pdf",
        mime="application/pdf",
        use_container_width=True,
    )
    st.divider()
    st.subheader("Projects")
    st.link_button("📄 Resume Analyser", "https://github.com/rajatt1616/Resume-Analyser", use_container_width=True)
    st.link_button("🔗 AI Portfolio ", "https://github.com/rajatt1616/Resume-Analyser", use_container_width=True)
    st.link_button("🃏 UNO Game Engine", "https://github.com/rajatt1616/better-uno", use_container_width=True)
    st.divider()
    st.subheader("Profiles")
    st.link_button("Leetcode", "https://leetcode.com/u/rajatt1616/", use_container_width=True)
    st.link_button("GitHub", "https://github.com/rajatt1616", use_container_width=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

# --- MAIN CARD CONTAINER (GROUPS HEADER & EXPANDER TOGETHER) ---
main_container = st.container()

with main_container:
    st.markdown("### 👋 Welcome to my AI Portfolio")
    st.markdown("I'm Rajat, a developer specializing in Python, C++, and AI integrations.")

    # Clean Collapsible Suggested Questions
    with st.expander("💡 **Suggested Questions**", expanded=(len(st.session_state.messages) == 0)):
        questions = [
            "Tell me about yourself",
            "What projects have you built?",
            "What technologies do you know?",
            "Explain the Resume Analyser project",
            "What are you currently learning?",
            "What are your career goals?",
        ]
        cols = st.columns(2)
        for index, question in enumerate(questions):
            if cols[index % 2].button(question, key=f"btn_{index}", use_container_width=True):
                st.session_state.messages.append({"role": "user", "content": question})
                st.rerun()

    st.divider()

    # --- CHAT HISTORY ---
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

# --- CHAT INPUT & RESPONSE ---
prompt = st.chat_input("Ask something about my experience...")

if prompt or (st.session_state.messages and st.session_state.messages[-1]["role"] == "user" and len(st.session_state.messages) % 2 != 0):
    if prompt:
        with st.chat_message("user"):
            st.write(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

    try:
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "system", "content": system_prompt}] + st.session_state.messages,
            stream=True,
        )

        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            answer = ""
            for chunk in response:
                if chunk.choices[0].delta.content:
                    answer += chunk.choices[0].delta.content
                    message_placeholder.markdown(answer + "▌")
            message_placeholder.markdown(answer)

        st.session_state.messages.append({"role": "assistant", "content": answer})

    except Exception as e:
        st.error(f"Error: {e}")