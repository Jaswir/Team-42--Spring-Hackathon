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
paths = []
dir = "C:/Users/deepa/Downloads/Vectara_Sample/"
for file in os.listdir(dir):
    paths.append([dir,file])
# Specify the path to your PDF file

for path in paths:
    pdf_path = path[0]+path[1]

    # Extract content
    text_content, tables_content = extract_text_and_tables(pdf_path)


    with open('out/'+path[1].rstrip('.pdf')+'.txt', 'w',encoding='utf8') as f:
        for page_text in text_content:
            f.write(page_text)
            f.write('\n')
        # # Save tables to CSV files
        # for i, table in enumerate(tables_content):
        #     pass
