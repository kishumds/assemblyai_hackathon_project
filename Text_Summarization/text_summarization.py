import streamlit as st
import torch

def app():
    st.title("Text Summarization")

    text = st.text_area("Enter text")

    def load_model():
        model = torch.load('Text_Summarization/summarizer.pt')
        return model

    st.text("Length of Text must be more than max_length. \nIncreasing Text take longer time to generate summary.")
    st.write(f"<h6 style='text-align:right'>Input Length: {len(text.split())}</h6>", unsafe_allow_html=True)

    st.write("<h5>Approximate Maximum and Minimum Length of Summary</h5>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        max_length = st.text_input("max_length", 100)
    
    with col2:
        min_length = st.text_input("min_length", 32)

    st.write("Click on Submit to generate Summary")

    button = st.button("Submit")

    if button:
        if text is "":
            st.warning("Enter Input...")
            st.stop()

        input = st.empty()
        input.text_input("Status", "Processing...", disabled=True)

        model = load_model()

        # parameters for text generation out of model
        params = {
                "max_length": int(max_length),
                "min_length": int(min_length),
                "do_sample": False,
                "early_stopping": True,
                "no_repeat_ngram_size": 3,
                }

        result = model(text, **params)

        input.text_input("Status", "Done...", disabled=True)

        st.subheader("Summary:")
        st.write(result[0]['summary_text']) 