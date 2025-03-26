import streamlit as st
import google.generativeai as genai
import io
import os
import docx
from google.cloud import texttospeech
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class AIVoiceAssistant:
    def __init__(self, gemini_key_path=None, gcp_key_path=None):
        def read_key_from_docx(file_path):
            try:
                doc = docx.Document(file_path)
                return ''.join([para.text for para in doc.paragraphs]).strip()
            except Exception as e:
                st.error(f"Error reading DOCX file: {e}")
                return None

        # Prioritize environment variables or passed parameters
        gemini_key_path = gemini_key_path or os.getenv('GEMINI_KEY_PATH')
        gcp_key_path = gcp_key_path or os.getenv('GCP_KEY_PATH')

        # Validate key paths
        if not gemini_key_path or not gcp_key_path:
            st.error("Please configure Gemini and GCP key paths in environment or provide them directly.")
            st.stop()

        # Read Gemini key from DOCX
        gemini_key = read_key_from_docx(gemini_key_path)
        
        if not gemini_key:
            st.error("Failed to read Gemini API key.")
            st.stop()

        # Set GCP credentials
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = gcp_key_path
        
        # Configure Gemini API
        try:
            genai.configure(api_key=gemini_key)
            self.model = genai.GenerativeModel('gemini-1.5-pro')
        except Exception as e:
            st.error(f"Gemini API configuration failed: {e}")
            st.stop()
        
        # Initialize Text-to-Speech client
        try:
            self.tts_client = texttospeech.TextToSpeechClient()
        except Exception as e:
            st.error(f"Text-to-Speech client initialization failed: {e}")
            st.stop()

    def generate_response(self, question):
        system_prompt = """
        You are Donga Sai Venkata Sri Harsha, an AI assistant with a unique perspective. 
        Respond to interview questions authentically, sharing personal insights and experiences.

        Key Attributes:
        - Superpower: Persistent curiosity and deep exploration of interests
        - Growth Areas: AI, Astronomy, Generative AI, Machine Learning
        - Work Philosophy: Passion-driven learning, not just hard work
        - Personal Motto: When intrigued, push boundaries to understand deeply
        """
        
        full_prompt = f"{system_prompt}\n\nQuestion: {question}"
        
        try:
            response = self.model.generate_content(full_prompt)
            return response.text
        except Exception as e:
            st.error(f"Response generation error: {e}")
            return "I'm experiencing some technical difficulties. Could you please try again?"

    def text_to_speech(self, text):
        try:
            synthesis_input = texttospeech.SynthesisInput(text=text)
            voice = texttospeech.VoiceSelectionParams(
                language_code="en-US", 
                ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
            )
            audio_config = texttospeech.AudioConfig(
                audio_encoding=texttospeech.AudioEncoding.MP3
            )
            response = self.tts_client.synthesize_speech(
                input=synthesis_input, voice=voice, audio_config=audio_config
            )
            return io.BytesIO(response.audio_content)
        except Exception as e:
            st.error(f"Text-to-speech conversion error: {e}")
            return None

def main():
    # Streamlit page configuration
    st.set_page_config(
        page_title="Harsha: AI Voice Assistant", 
        page_icon="🤖", 
        layout="centered"
    )

    # Custom CSS for enhanced styling
    st.markdown("""
    <style>
    .stApp {
        background-color: #f0f2f6;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #45a049;
        transform: scale(1.05);
    }
    </style>
    """, unsafe_allow_html=True)

    # Title and introduction
    st.title("🎙️ Interview with Harsha: AI Assistant")
    st.markdown("**Discover the unique perspective of an AI with boundless curiosity**")

    # Interview questions
    interview_questions = [
        "What should we know about your life story in a few sentences?",
        "What's your #1 superpower?", 
        "What are the top 3 areas you'd like to grow in?",
        "What misconception do your coworkers have about you?",
        "How do you push your boundaries and limits?"
    ]
    
    # Key configuration paths (optional fallback)
    GEMINI_KEY_PATH = os.getenv('GEMINI_KEY_PATH', '/home/harsha/Downloads/Gemini -API.docx')
    GCP_KEY_PATH = os.getenv('GCP_KEY_PATH', '/home/harsha/Downloads/verbal-trainer-72cf5f972e42.json')

    try:
        # Initialize assistant
        assistant = AIVoiceAssistant(GEMINI_KEY_PATH, GCP_KEY_PATH)
    except Exception as e:
        st.error(f"Assistant initialization failed: {e}")
        st.stop()
    
    # Question selection
    selected_question = st.selectbox(
        "Choose an Interview Question", 
        interview_questions,
        help="Select a question to explore Harsha's unique perspective"
    )
    
    # Response columns
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📄 Get Text Response"):
            with st.spinner('Generating response...'):
                response = assistant.generate_response(selected_question)
                st.write(response)
    
    with col2:
        if st.button("🔊 Listen to Response"):
            with st.spinner('Generating audio...'):
                response = assistant.generate_response(selected_question)
                audio_bytes = assistant.text_to_speech(response)
                if audio_bytes:
                    st.audio(audio_bytes, format='audio/mp3')
                    st.download_button(
                        "⬇️ Download Audio", 
                        audio_bytes, 
                        file_name="harsha_response.mp3", 
                        mime="audio/mp3"
                    )

    # Footer
    st.markdown("---")
    st.markdown("*Powered by Google Gemini & Text-to-Speech APIs*")

if __name__ == "__main__":
    main()
