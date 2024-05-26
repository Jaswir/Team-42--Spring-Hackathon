import streamlit as st
from os import environ
import json
import random

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

    question_slot = st.empty()
    answer_slot = st.empty()

    with st.form("input_form"):
        # Place the text input and the button within the form
        col1, col2 = st.columns([5, 1])
        with col1:
            question_text = "✋🏿 Ask a question:"
            question = st.text_area(question_text)
        with col2:
            st.write(" ")
            st.write(" ")
            submit_label = "Submit"

            submit_button = st.form_submit_button(label=submit_label)

    # Check if the form has been submitted
    if submit_button:
        if question:
            st.write('answer: 42')
        else:
            st.warning("Please enter a question.")


if __name__ == "__main__":
    main()
