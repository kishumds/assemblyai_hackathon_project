import requests
import time
import streamlit as st
from configure import assemblyaai_api_key
import base64

def get_base64(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def app():
    bin_str = get_base64("background/audio.png")
    page_bg_img = '''
        <style>
        .stApp {
        background-image: url("data:image/jpg;base64,%s");
        background-size: cover;;        
        }
        </style>
        ''' % bin_str

    st.title("Audio Transcription")

    st.markdown("Audio Transcription using AssemblyAI API.")

    st.markdown(page_bg_img, unsafe_allow_html=True)

    upload_endpoint = "https://api.assemblyai.com/v2/upload"
    transcription_endpoint = "https://api.assemblyai.com/v2/transcript"

    headers = {"authorization": assemblyaai_api_key}

    def read_file(filename, chunk_size = 5242880):
        with open(filename, 'rb') as _file:
            while True:
                data = _file.read(chunk_size)
                if not data:
                    break
                yield data

    filename = st.file_uploader("Choose Audio file")

    st.write("Click on Submit button to get transcription")
    button = st.button("Submit")

    if button:
        if filename is None:
            st.warning("Select audio file...")
            st.stop()

        input = st.empty()
        input.text_input("Status", "Processing...", disabled=True)

        upload_response = requests.post(upload_endpoint, headers=headers, data=read_file(f'Audio_Transcription/{filename.name}'))
        audio_url = upload_response.json()['upload_url']

        json = {"audio_url":audio_url,
                "language_detection":True}

        transcription_response = requests.post(transcription_endpoint, headers=headers, json=json)
        transcription_id = transcription_response.json()['id']

        polling_endpoint = transcription_endpoint + "/" + transcription_id

        while True:
            polling_response = requests.get(polling_endpoint, headers=headers)
            status = polling_response.json()['status']

            if status == "completed":
                input.text_input("Status", "Done...", disabled=True)
                st.subheader("Trancription:")
                st.write(polling_response.json()['text'])
                break

            elif status == "error":
                st.write('Error')
                break

            else:
                time.sleep(2)
                continue