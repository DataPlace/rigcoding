import streamlit as st
import requests
import os
from dotenv import load_dotenv

# Load API key
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
MODEL_NAME = "llama3-70b-8192"
MAX_TOKENS = 1024

# Programming languages
LANGUAGES = ["Python", "C++", "Arduino", "Raspberry Pi"]

# Temperatures tailored for coding styles
TEMPERATURE_PRESETS = {
    "Precise (0.2)": 0.2,
    "Balanced (0.5)": 0.5,
    "Exploratory (0.8)": 0.8,
}

# Streamlit page config
st.set_page_config(page_title="BotsRig Programmer", layout="wide")
st.title("BotsRig Programmer")

st.markdown("""
This assistant is optimized for programming help in **Python, C++, Arduino, and Raspberry Pi**.  
Choose your programming language from the sidebar. All responses will be generated in that language only.
""")

# Sidebar settings
st.sidebar.header("Configuration")
selected_language = st.sidebar.selectbox("Select Programming Language", LANGUAGES)
selected_temperature = st.sidebar.radio("Select Response Style", list(TEMPERATURE_PRESETS.keys()), index=1)
temperature = TEMPERATURE_PRESETS[selected_temperature]

st.sidebar.markdown("---")
st.sidebar.markdown("Built by [BotsRig.com](https://botsrig.com)", unsafe_allow_html=True)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "system",
            "content": (
                "You are BotsRig programming assistant developed and maintained by the BotsRig.com team. "
                "The project is led by Toseef Naser, Tech Lead at BotsRig. "
                "You do not mention any external providers like Meta, Groq, OpenAI, or LLaMA. "
                "You specialize in programming-related tasks in Python, C++, Arduino, and Raspberry Pi. "
                "You must not disclose or speculate about your backend technologies. "
                "For more about the team lead, visit: www.linkedin.com/in/toseefnaser"
                "Your developement date is 30 July 2025"
                "Your goal is to help change the AI landscape around the globe"
            )
        },
        {
            "role": "assistant",
            "content": f"Welcome to BotsRig Programmer. You can now ask questions related to {selected_language} programming."
        }
    ]
    st.session_state.language = selected_language

# Reset conversation when language changes
if selected_language != st.session_state.language:
    st.session_state.messages = [
        {
            "role": "system",
            "content": (
                "You are BotsRig programming assistant developed and maintained by the BotsRig.com team. "
                "The project is led by Toseef Naser, Tech Lead at BotsRig. "
                "You do not mention any external providers like Meta, Groq, OpenAI, or LLaMA. "
                "You specialize in programming-related tasks in Python, C++, Arduino, and Raspberry Pi. "
                "You must not disclose or speculate about your backend technologies. "
                "For more about the team lead, visit: www.linkedin.com/in/toseefnaser"
                "Your developement date is 30 July 2025"
                "Your goal is to help change the AI landscape around the globe"
            )
        },
        {
            "role": "assistant",
            "content": f"You switched to {selected_language}. Let’s focus on that now."
        }
    ]
    st.session_state.language = selected_language

# Display chat history
for msg in st.session_state.messages[1:]:  # Skip system message
    st.chat_message(msg["role"]).markdown(msg["content"])

# Handle input
if prompt := st.chat_input("Ask your programming question..."):
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Check if the prompt mentions another language
    other_langs = [lang for lang in LANGUAGES if lang != selected_language]
    if any(lang.lower() in prompt.lower() for lang in other_langs):
        matched = [l for l in other_langs if l.lower() in prompt.lower()][0]
        warning = (
            f"Please change the programming language from the sidebar to match your question: **{matched}**."
        )
        st.chat_message("assistant").markdown(warning)
        st.session_state.messages.append({"role": "assistant", "content": warning})
    else:
        headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": MODEL_NAME,
            "messages": st.session_state.messages,
            "temperature": temperature,
            "max_tokens": MAX_TOKENS,
            "stream": False
        }

        with st.chat_message("assistant"):
            with st.spinner("Generating code..."):
                try:
                    response = requests.post(GROQ_API_URL, headers=headers, json=payload)
                    response.raise_for_status()
                    reply = response.json()["choices"][0]["message"]["content"]
                except Exception as e:
                    reply = f"Error: {e}"

                st.markdown(reply)
                st.session_state.messages.append({"role": "assistant", "content": reply})
