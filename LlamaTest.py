import pymongo
import requests
from dotenv import load_dotenv
import os
from os import environ
from openai import OpenAI
import json

import nest_asyncio

nest_asyncio.apply()
from llama_parse  import LlamaParse
from llama_index.core import SimpleDirectoryReader
from llama_index.core.node_parser import MarkdownElementNodeParser
from llama_index.core import VectorStoreIndex
from llama_index.postprocessor.flag_embedding_reranker import (
    FlagEmbeddingReranker,      
)
import re

load_dotenv()
OPENAI_API_KEY = environ.get("OPENAI_API_KEY")
MONGO_URI = os.getenv("MONGO_URL")
LLAMA_CLOUD_API_KEY = os.getenv("LLAMA_CLOUD_API_KEY")


def ParsePDFToJSON(file_name):
    # Parses PDF to Json HTML
    parser = LlamaParse(verbose=True, api_key=LLAMA_CLOUD_API_KEY)
    json_objs = parser.get_json_result(f"./temp/{file_name}")
    json_list = json_objs[0]["pages"]

    print(json_list)
    return json_list


    # Extracts Tables from Json HTML
    # pattern = re.compile(r"'rows': \[.*?\]")
    # matches = pattern.findall(str(json_list))

    # print(matches)

# Parses PDF to Json HTML
parser = LlamaParse(verbose=True, api_key=LLAMA_CLOUD_API_KEY)
file_name = 'CSM-RE8040-BE440-L.pdf'
json_objs = parser.get_json_result(f"./temp/{file_name}")
pages = json_objs[0]["pages"]

items = []
for page in pages:
    for key, value in page.items():
        if key == "items":
            items.append(value)

rows = []
for item in items:
    for subitem in item:
        for key, value in subitem.items():
            if key == "rows":
                rows.append(value[0])
                print(f"Rows: {rows}" "\n")


for row in rows:
    # Convert list of lists to dictionary
    json_dict = {item[0]: item[1] for item in row}

    # Convert dictionary to JSON string with indentation for readability
    json_string = json.dumps(json_dict, indent=4)

    print(json_string)


    # print(f"Item: {item}" "\n")
    # for subitem in item:
    #     print(f"Subitem: {subitem}" "\n")
   
    # print(json_list)

# client = pymongo.MongoClient(MONGO_URI)
# db = client["spring"]
# collection = db["records"]
# collection.delete_many({})

# parser = LlamaParse(
#     api_key=LLAMA_CLOUD_API_KEY, result_type="markdown", num_workers=4, verbose=True
# )

# file_extractor = {".pdf": parser}

# documents = SimpleDirectoryReader(
#     "./small_sample_pdfs", file_extractor=file_extractor
# ).load_data()

# print(documents[0].text[:1000] + "...")




# # Converts markdown to nodes
# node_parser = MarkdownElementNodeParser(llm=OpenAI(model="gpt-3.5-turbo"), num_workers=4)
# nodes = node_parser.get_nodes_from_documents(documents=[documents[0]])
# base_nodes, objects = node_parser.get_nodes_and_objects(nodes)

# #Vector Store
# recursive_index = VectorStoreIndex(nodes=base_nodes + objects)
# raw_index = VectorStoreIndex.from_documents(documents)

# reranker = FlagEmbeddingReranker(
#     top_n=5,
#     model="BAAI/bge-reranker-large",
# )

# recursive_query_engine = recursive_index.as_query_engine(
#     similarity_top_k=15, node_postprocessors=[reranker], verbose=True
# )

# raw_query_engine = raw_index.as_query_engine(
#     similarity_top_k=15, node_postprocessors=[reranker]
# )

# print(len(nodes))

# query = "45.4 m3/day production"

# response_1 = raw_query_engine.query(query)
# print("\n***********New LlamaParse+ Basic Query Engine***********")
# print(response_1)

# response_2 = recursive_query_engine.query(query)
# print("\n***********New LlamaParse+ Recursive Retriever Query Engine***********")
# print(response_2)