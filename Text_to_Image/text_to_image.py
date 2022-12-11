import streamlit as st
from configure import stablility_ai_api_key
from stability_sdk import client
import stability_sdk.interfaces.gooseai.generation.generation_pb2 as generation
import io
import warnings
from PIL import Image
import random
import base64

def get_base64(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def app():
    bin_str = get_base64("background/text2image.png")
    page_bg_img = '''
        <style>
        .stApp {
        background-image: url("data:image/jpg;base64,%s");
        background-size: cover;
        }
        </style>
        ''' % bin_str

    st.markdown(page_bg_img, unsafe_allow_html=True)

    st.title("Text to Image")

    st.markdown("Text to Image generation using Stability AI API.")

    text = st.text_input("Input Prompt")

    col1, col2 = st.columns(2)

    number = st.text_input("Number of Image", 1)

    st.text("Recommanded number of image 1")

    st.write("Click on Submit to generate image.")
    button = st.button("Submit")

    if button:
        if text == "":
            st.warning("Enter Input...")
            st.stop() 

        input = st.empty()

        status = input.text_input("Status", "Processing...", disabled=True)

        stability_api = client.StabilityInference(
            key=stablility_ai_api_key,
            verbose=True,
            engine="stable-diffusion-v1-5",
        )
        
        answers = stability_api.generate(
            prompt=text,
            seed=random.randint(1,1000000),
            steps=30,
            cfg_scale=8.0,
            width=512,
            height=512,
            samples=int(number),
            sampler=generation.SAMPLER_K_DPMPP_2M
        )
        
        for resp in answers:
            for artifact in resp.artifacts:
                if artifact.finish_reason == generation.FILTER:
                    warnings.warn(
                        "Your request activated the API's safety filters and could not be processed."
                        "Please modify the prompt and try again.")
                if artifact.type == generation.ARTIFACT_IMAGE:
                    img = Image.open(io.BytesIO(artifact.binary))
                    input.text_input("Status", "Done...", disabled=True)
                    st.image(img)