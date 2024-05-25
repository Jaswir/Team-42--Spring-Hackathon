import pymongo
import requests
from dotenv import load_dotenv
import os
from os import environ
from openai import OpenAI

import nest_asyncio

nest_asyncio.apply()
from llama_parse  import LlamaParse
from llama_index.core import SimpleDirectoryReader
from llama_index.core.node_parser import MarkdownElementNodeParser
from llama_index.core import VectorStoreIndex
from llama_index.postprocessor.flag_embedding_reranker import (
    FlagEmbeddingReranker,      
)

load_dotenv()
OPENAI_API_KEY = environ.get("OPENAI_API_KEY")
MONGO_URI = os.getenv("MONGO_URL")
LLAMA_CLOUD_API_KEY = os.getenv("LLAMA_CLOUD_API_KEY")


# client = pymongo.MongoClient(MONGO_URI)
# db = client["spring"]
# collection = db["records"]
# collection.delete_many({})

parser = LlamaParse(verbose=True, api_key=LLAMA_CLOUD_API_KEY)
json_objs = parser.get_json_result("./small_sample_pdfs/CSM-RE8040-BE-L.pdf")
json_list = json_objs[0]["pages"]

print(json_list)

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