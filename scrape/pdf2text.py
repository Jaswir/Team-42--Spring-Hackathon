import os

import pdfplumber
import pandas as pd


def extract_text_and_tables(pdf_path):
    text_content = []
    tables_content = []

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            # Extract text
            text = page.extract_text()
            if text:
                text_content.append(text)

            # Extract tables
            tables = page.extract_tables()
            for table in tables:
                # Convert table to DataFrame for better handling
                df = pd.DataFrame(table[1:], columns=table[0])
                tables_content.append(df)

    return text_content, tables_content