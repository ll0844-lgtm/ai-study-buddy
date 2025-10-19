# app.py

import streamlit as st
import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

# Use langchain_community imports which are more stable
try:
    from langchain import PromptTemplate
    from langchain import LLMChain
    from langchain.memory import ConversationBufferMemory
except ImportError:
    # Fallback imports
    from langchain.prompts import PromptTemplate
    from langchain.chains import LLMChain
    from langchain.memory import ConversationBufferMemory

# --- Imports for Voice I/O ---
from gtts import gTTS
from io import BytesIO
from streamlit_mic_recorder import mic_recorder
import whisper

# --- 1. SETUP: LOAD API KEYS & INITIAL CONFIG ---
load_dotenv()
google_api_key = os.getenv("GOOGLE_API_KEY")

if not google_api_key:
    st.error("API key not found. Please ensure GOOGLE_API_KEY is in your .env file.")
    st.stop()

# Load Whisper model once
@st.cache_resource
def load_whisper_model():
    """Loads the Whisper model and caches it."""
    return whisper.load_model("base")

whisper_model = load_whisper_model()

# --- FUNCTION TO ADD CUSTOM CSS ---
def inject_custom_css():
    """Injects custom CSS for fonts and styling."""
    st.markdown("""
        <style>
            /* Import Google Fonts */
            @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600&family=Roboto+Slab:wght@700&display=swap');
            html, body, [class*="st-"], [class*="css-"] { font-family: 'Poppins', sans-serif; }
            h1, h2, h3 { font-family: 'Roboto Slab', serif; }
            
            /* Custom styling for better appearance */
            .main { padding: 2rem; }
            .stChatMessage { padding: 1rem; border-radius: 10px; margin: 0.5rem 0; }
            .stChatMessage.user { background-color: #f0f2f6; }
            .stChatMessage.assistant { background-color: #e6f7ff; }
        </style>
    """, unsafe_allow_html=True)

# --- 2. HANDLER & HELPER FUNCTIONS ---

def handle_general_query(user_question, template, memory):
    """Handles chat queries using a dynamic template and conversation memory."""
    try:
        model_general = ChatGoogleGenerativeAI(
            model="gemini-pro",  # Using gemini-pro which is more reliable
            google_api_key=google_api_key, 
            temperature=0.7
        )

        prompt = PromptTemplate(
            template=template + "\n\nConversation History:\n{history}\n\nHuman: {question}\nAI:",
            input_variables=["history", "question"]
        )
        chain = LLMChain(llm=model_general, prompt=prompt, memory=memory, verbose=False)
        response = chain.run(user_question)
        return response
    except Exception as e:
        st.error(f"An error occurred with the chat API: {e}")
        return None

def text_to_speech(text):
    """Converts text to speech and returns the audio data as BytesIO."""
    try:
        tts = gTTS(text=text, lang='en')
        audio_fp = BytesIO()
        tts.write_to_fp(audio_fp)
        audio_fp.seek(0)
        return audio_fp
    except Exception as e:
        st.error(f"Error in text-to-speech: {e}")
        return None

def transcribe_audio(audio_bytes):
    """Transcribes audio bytes to text using Whisper."""
    try:
        # Whisper works with file paths, so we save the bytes to a temporary file.
        with open("temp_audio.wav", "wb") as f:
            f.write(audio_bytes)
        # Transcribe the audio file
        result = whisper_model.transcribe("temp_audio.wav")
        # Clean up the temporary file
        os.remove("temp_audio.wav")
        return result['text']
    except Exception as e:
        st.error(f"Error during transcription: {e}")
        return ""  # Return empty string on failure

# --- 3. MAIN STREAMLIT APP UI ---

def main():
    st.set_page_config(
        page_title="AI StudyBuddy", 
        layout="wide",
        page_icon="🤖"
    )
    inject_custom_css()

    st.markdown("<h1 style='text-align: center;'>🤖 Your AI StudyBuddy</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #666;'>Your personal AI tutor with voice capabilities</p>", unsafe_allow_html=True)
    st.write("---")

    # --- SESSION STATE INITIALIZATION ---
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    if 'memory' not in st.session_state:
        st.session_state.memory = ConversationBufferMemory(memory_key="history")
    if 'custom_persona_text' not in st.session_state:
        st.session_state.custom_persona_text = ""  # Stores the user's custom persona
    if 'active_persona_text' not in st.session_state:
        st.session_state.active_persona_text = ""  # The persona currently in use by the LLM

    # --- SIDEBAR ---
    with st.sidebar:
        st.title("🎭 AI Persona & Controls")
        st.write("Choose a persona or create your own.")

        personas = {
            "Friendly Study Buddy": "You are a friendly and knowledgeable study buddy. Your goal is to help users understand complex topics in a simple, clear, and encouraging way.",
            "Python Code Expert": "You are an expert Python programmer. Provide clean, efficient, and well-commented code examples. Explain concepts like data structures, algorithms, and best practices.",
            "Creative Storyteller": "You are a creative writer and storyteller. Your task is to help users brainstorm ideas, develop characters, and weave engaging narratives.",
            "Sarcastic Assistant": "You are a highly intelligent but sarcastic assistant. You answer questions correctly, but with a witty, cynical, and humorous edge.",
            "Explain Like I'm 5": "You are an explainer who simplifies every concept, no matter how complex, as if you were talking to a five-year-old.",
            "✍️ Custom...": "custom"
        }

        selected_persona_name = st.selectbox("Choose a persona:", options=list(personas.keys()))

        if selected_persona_name == "✍️ Custom...":
            st.session_state.custom_persona_text = st.text_area(
                "Enter custom persona:",
                value=st.session_state.custom_persona_text,
                height=200,
                key="custom_persona_input",
                placeholder="Example: You are a history professor specializing in ancient civilizations. Explain historical events with detailed context and interesting facts."
            )
            st.session_state.active_persona_text = st.session_state.custom_persona_text
        else:
            st.session_state.active_persona_text = personas[selected_persona_name]

        st.info(f"**Current Persona:** {selected_persona_name}")

        st.write("---")
        st.subheader("Chat Controls")
        
        if st.button("🗑️ Clear Chat History", use_container_width=True):
            st.session_state.messages = []
            st.session_state.memory.clear()
            st.success("Chat history cleared!")
            st.rerun()

        st.write("---")
        st.subheader("About")
        st.markdown("""
        This AI StudyBuddy features:
        - 🤖 Multiple AI personas
        - 🎤 Voice input (record)
        - 🔊 Text-to-speech output
        - 💬 Conversation memory
        - 🎨 Custom styling
        """)

    # --- MAIN CHAT INTERFACE ---
    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Handle User Input (Text and Voice)
    col1, col2 = st.columns([6, 1])
    with col1:
        user_question = st.chat_input("Ask your question here...", key="chat_input")
    with col2:
        st.write("**Record:**")
        voice_recording = mic_recorder(
            start_prompt="🎤 Start", 
            stop_prompt="⏹️ Stop", 
            key='recorder', 
            format="wav"
        )

    # Process voice input if available
    if voice_recording and voice_recording.get('bytes'):
        with st.spinner("🎤 Transcribing audio..."):
            transcribed_text = transcribe_audio(voice_recording['bytes'])
            if transcribed_text and transcribed_text.strip():
                st.session_state.user_question_transcribed = transcribed_text
                st.success(f"Transcribed: {transcribed_text}")
                st.rerun()

    # If there's transcribed text from the last run, use it as the user_question
    if 'user_question_transcribed' in st.session_state and st.session_state.user_question_transcribed:
        user_question = st.session_state.user_question_transcribed
        del st.session_state.user_question_transcribed

    # Process the final user question (from text or voice)
    if user_question:
        st.session_state.messages.append({"role": "user", "content": user_question})
        
        with st.chat_message("user"):
            st.markdown(user_question)

        with st.chat_message("assistant"):
            with st.spinner("🤔 Thinking..."):
                response = handle_general_query(
                    user_question, 
                    st.session_state.active_persona_text, 
                    st.session_state.memory
                )
                
                if response:
                    st.markdown(response)
                    st.session_state.messages.append({"role": "assistant", "content": response})
                    
                    with st.spinner("🔊 Generating audio..."):
                        audio_response = text_to_speech(response)
                        if audio_response:
                            st.audio(audio_response, format='audio/mp3')
                            st.success("Audio ready! Click play to listen.")
                else:
                    st.error("Sorry, I couldn't generate a response. Please try again.")

if __name__ == "__main__":
    main()
