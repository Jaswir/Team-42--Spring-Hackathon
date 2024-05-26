import streamlit as st
import os
from os import environ
import json
import random
import LlamaTest


def clear_directory(directory):
    # List all files in the directory
    files = os.listdir(directory)
    
    # Iterate over each file and delete it
    for file in files:
        file_path = os.path.join(directory, file)
        os.remove(file_path)

def main():

    # Custom CSS to increase the height of the input field
    css = '''
    <style>

        .stTextArea textarea {
            height: 300px;
        }
    </style>
    '''

    # Injecting the custom CSS with markdown
    st.write(css, unsafe_allow_html=True)

    st.title("Structured Tables")

    # File uploader allows user to add file
    uploaded_file = st.file_uploader("Choose a PDF file", type='pdf')

    if uploaded_file is not None:
        save_dir = 'temp'
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
        else:
            clear_directory(save_dir)
    
        # To See details
        file_details = {"filename":uploaded_file.name, "filetype":uploaded_file.type,
                        "filesize":uploaded_file.size}
        st.write(file_details)

        # Saving upload
        with open(os.path.join(save_dir, uploaded_file.name), "wb") as f:
            f.write(uploaded_file.getbuffer())
            
    question_slot = st.empty()
    answer_slot = st.empty()

    with st.form("input_form"):
        # Place the text input and the button within the form
        col1, col2 = st.columns([5, 1])
        # with col1:
        #     question_text = "✋🏿 Ask a question:"
        #     question = st.text_area(question_text)
        with col2:
            st.write(" ")
            st.write(" ")
            submit_label = "Submit"

            submit_button = st.form_submit_button(label=submit_label)

    # Check if the form has been submitted
    if submit_button:
        if uploaded_file is not None:
            answer = LlamaTest.ParsePDFTablesToJSON(uploaded_file.name)
            st.write('answer:', answer)
        else:
            st.warning("Please upload a file")


if __name__ == "__main__":
    main()
