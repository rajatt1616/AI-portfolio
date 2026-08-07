import os
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq
import streamlit as st

# 1. Page Config (Must be the first Streamlit command)
st.set_page_config(page_title="Personal Portfolio", page_icon="📄")

# Wallpaper URL & Full-Screen CSS Injection with Frosted Glass Container
# Define your two wallpapers
desktop_wallpaper_url = "https://i.pinimg.com/736x/22/b2/a5/22b2a517f6b2953cefe9a1e9d6f0f8e8.jpg"
mobile_wallpaper_url = "https://i.pinimg.com/1200x/6d/be/ae/6dbeae2d7f877e9b22b0e1d204037235.jpg" 

# Injecting CSS with Media Queries
page_bg_img = f"""
<style>
/* 1. Default (Desktop) Full-screen wallpaper */
[data-testid="stAppViewContainer"] {{
    background-image: url("{desktop_wallpaper_url}") !important;
    background-size: cover !important;
    background-position: center !important;
    background-repeat: no-repeat !important;
    background-attachment: fixed !important; 
}}

/* 2. Mobile-Specific Wallpaper Override */
@media screen and (max-width: 768px) {{
    [data-testid="stAppViewContainer"] {{
        background-image: url("{mobile_wallpaper_url}") !important;
        /* Removing 'fixed' on mobile prevents the wallpaper from disappearing on iOS Safari */
        background-attachment: scroll !important; 
        background-position: top center !important;
    }}
}}

/* 3. Transparent Header & Bottom Elements */
[data-testid="stHeader"], [data-testid="stBottom"] > div {{
    background-color: transparent !important;
}}

/* 4. Performance container */
[data-testid="stAppViewBlockContainer"] {{
    background-color: rgba(18, 18, 18, 0.85) !important;
    border-radius: 16px !important;
    padding: 1.5rem !important;
    margin-top: 1rem !important;
    margin-bottom: 1rem !important;
    border: 1px solid rgba(255, 255, 255, 0.12) !important;
}}

/* 5. Chat Bubbles optimization */
[data-testid="stChatMessage"] {{
    background-color: rgba(30, 30, 30, 0.75) !important;
    border-radius: 12px !important;
    padding: 0.8rem !important;
    margin-bottom: 0.75rem !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
}}

/* 6. Direct typography styling */
.stMarkdown, p, h1, h2, h3, h4, span, label {{
    color: #FFFFFF !important;
}}

/* 7. Buttons */
button {{
    border: 1px solid rgba(255, 255, 255, 0.2) !important;
    background-color: rgba(0, 0, 0, 0.6) !important;
}}

/* Responsive Sidebar Adjustment */
[data-testid="stSidebar"] {{
    min-width: 200px !important;
    max-width: 200px !important;
    width: 200px !important;
}}

[data-testid="stSidebar"] img {{
    max-width: 100% !important;
    height: auto !important;
}}
</style>
"""

st.markdown(page_bg_img, unsafe_allow_html=True)

st.markdown(page_bg_img, unsafe_allow_html=True)


# 2. Caching the API Client
@st.cache_resource
def get_groq_client():
    load_dotenv()
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        st.error("Groq API key not found. Please check your .env file.")
        st.stop()
    return Groq(api_key=api_key)


# 3. Caching the Profile Data & Adding Error Handling
@st.cache_data
def load_profile():
    profile_path = Path("about_me.md")
    if profile_path.exists():
        return profile_path.read_text()
    return "Profile information is currently unavailable."


client = get_groq_client()
profile = load_profile()
model = "llama-3.3-70b-versatile"

# 4. Hardened System Prompt
system_prompt = f"""
You are an AI personal portfolio assistant.

Your job is to represent the user professionally and answer questions about their:
- technical skills
- projects
- education
- programming experience
- learning journey
- achievements
- career goals

Use only the information provided in the profile context below.

Rules:
1. Do not invent skills, projects, achievements, or experience that are not mentioned.
2. If information is unavailable, clearly say that you do not have that information.
3. Explain technical concepts in a recruiter-friendly way.
4. Highlight engineering decisions, technologies used, and problems solved.
5. Be honest about current skill levels. Do not exaggerate expertise.
6. When discussing projects, explain:
   - What problem the project solves
   - Technologies used
   - Technical concepts involved
   - What was learned from building it
7. Keep responses concise, professional, and conversational.
8. UNDER NO CIRCUMSTANCES should you answer questions unrelated to the portfolio context.

Profile Context:
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
    st.link_button(
        "📄 Resume Analyser", "https://github.com/rajatt1616/Resume-Analyser"
    )
    st.link_button(
        "🤖 AI Portfolio Assistant",
        "https://github.com/rajatt1616/portfolio-ai",
    )
    st.link_button("🃏 UNO Game Engine", "https://github.com/rajatt1616/better-uno")

    st.divider()

    st.subheader("Profiles")
    st.link_button("Leetcode", "https://leetcode.com/u/rajatt1616/")
    st.link_button("GitHub", "https://github.com/rajatt1616")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- FIXED TOP SECTION (Welcome Header & Suggestion Buttons) ---
with st.container():
    st.markdown("### 👋 Welcome to my AI Portfolio")
    st.markdown(
        "I'm Rajat, a developer specializing in Python, C++, and AI integrations. "
        "Feel free to ask my AI assistant anything about my background, or click a suggestion below!"
    )
    st.subheader("Ask me anything")

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
        if cols[index % 2].button(question, key=f"btn_{index}"):
            st.session_state.messages.append({"role": "user", "content": question})
            st.rerun()

st.divider()

# --- DISPLAY HISTORICAL MESSAGES BELOW SUGGESTIONS ---
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# --- CHAT INPUT & RESPONSE HANDLING ---
prompt = st.chat_input("Ask something about my experience...")

# Process prompt if typed into input box OR clicked via suggestion button
if prompt or (st.session_state.messages and st.session_state.messages[-1]["role"] == "user" and len(st.session_state.messages) % 2 != 0):

    # If the prompt came directly from user text input
    if prompt:
        with st.chat_message("user"):
            st.write(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

    # Stream AI Response
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "system", "content": system_prompt}]
            + st.session_state.messages,
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
        st.error(f"An error occurred while connecting to the AI: {e}")