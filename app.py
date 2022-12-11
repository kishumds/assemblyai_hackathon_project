from Audio_Transcription import audio_transcription
from Text_Summarization import text_summarization
from Text_to_Image import text_to_image
import streamlit as st

PAGES = {
        "Text to Image": text_to_image,
        "Audio Transcription": audio_transcription,
        "Text Summarization": text_summarization
        }

st.sidebar.title("AssemblyAI | $50K AI Winter Hackathon")
st.sidebar.write("Created 3 different AI task below listed. Select to use them.")

selection = st.sidebar.radio("Use", list(PAGES.keys()))
page = PAGES[selection]
page.app()