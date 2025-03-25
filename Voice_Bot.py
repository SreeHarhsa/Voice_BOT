import streamlit as st
import google.generativeai as genai
import io
import os
import docx
from google.cloud import texttospeech

class AIVoiceAssistant:
    def __init__(self, gemini_key_path, gcp_key_path):
        def read_key_from_docx(file_path):
            try:
                doc = docx.Document(file_path)
                return ''.join([para.text for para in doc.paragraphs]).strip()
            except Exception as e:
                raise ValueError(f"Error reading DOCX file: {e}")

        # Read Gemini key from DOCX
        gemini_key = read_key_from_docx(gemini_key_path)
        
        # Set GCP key
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = gcp_key_path
        
        # Configure Gemini API
        genai.configure(api_key=gemini_key)
        self.model = genai.GenerativeModel('gemini-1.5-pro')
        
        # Initialize Text-to-Speech client
        self.tts_client = texttospeech.TextToSpeechClient()

    def generate_response(self, question):
        system_prompt = f"""
        You are Donga Sai Venkata Sri Harsha. Answer the question with your personal experiences, strengths, and insights. Be honest, reflective, and authentic. Provide examples where necessary.

        - Your superpower: If something intrigues you, you never give up on it.
        - Top 3 areas of growth: AI, Astronomy, Generative AI, and Machine Learning.
        - Common misconception: Your coworkers think you work hard, but you simply pursue your interests with passion.
        - How you push limits: When something intrigues you, you push your boundaries to explore it deeply.
        """
        full_prompt = f"{system_prompt}\n\nQuestion: {question}"
        
        try:
            response = self.model.generate_content(full_prompt)
            return response.text
        except Exception as e:
            return f"Error generating response: {e}"

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
            st.error(f"Text-to-speech error: {e}")
            return None

def main():
    st.set_page_config(page_title="AI Assistant Interview", page_icon="🤖")
    st.title("🎙️ AI Assistant Personal Interview")
    
    # Paths to API key files
    GEMINI_KEY_PATH = '/home/harsha/Downloads/Gemini -API.docx'
    GCP_KEY_PATH = '/home/harsha/Downloads/verbal-trainer-72cf5f972e42.json'
    
    try:
        assistant = AIVoiceAssistant(GEMINI_KEY_PATH, GCP_KEY_PATH)
    except Exception as e:
        st.error(f"Failed to initialize assistant: {e}")
        st.stop()
    
    # Interview questions
    interview_questions = [
        "What should we know about your life story in a few sentences?",
        "What's your #1 superpower?", 
        "What are the top 3 areas you'd like to grow in?",
        "What misconception do your coworkers have about you?",
        "How do you push your boundaries and limits?"
    ]
    
    selected_question = st.selectbox("Choose an Interview Question", interview_questions)
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Get Text Response"):
            response = assistant.generate_response(selected_question)
            st.write(response)
    
    with col2:
        if st.button("Listen to Response"):
            response = assistant.generate_response(selected_question)
            audio_bytes = assistant.text_to_speech(response)
            if audio_bytes:
                st.audio(audio_bytes, format='audio/mp3')
                st.download_button("Download Audio", audio_bytes, file_name="response.mp3", mime="audio/mp3")

if __name__ == "__main__":
    main()

