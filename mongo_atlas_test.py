import pymongo
import requests
from dotenv import load_dotenv
import os
from os import environ
from openai import OpenAI


# Load environment variables from .env file
load_dotenv()
OPENAI_API_KEY = environ.get("OPENAI_API_KEY")
MONGO_URI = os.getenv("MONGO_URL")


hf_token = os.getenv("HF_TOKEN")
embedding_url = "https://api-inference.huggingface.co/pipeline/feature-extraction/sentence-transformers/all-MiniLM-L6-v2"


def generate_embedding_openAI(text):
    client = OpenAI()
    response = client.embeddings.create(input=text, model="text-embedding-3-small")
    return response.data[0].embedding


def generate_embedding(text: str) -> list[float]:

    response = requests.post(
        embedding_url,
        headers={"Authorization": f"Bearer {hf_token}"},
        json={"inputs": text},
    )

    if response.status_code != 200:
        raise ValueError(
            f"Request failed with status code {response.status_code}: {response.text}"
        )

    return response.json()


def query_atlas(query: str):

    results = collection.aggregate(
        [
            {
                "$vectorSearch": {
                    "queryVector": generate_embedding(query),
                    "path": "plot_embedding_hf",
                    "numCandidates": 100,
                    "limit": 4,
                    "index": "PlotSemanticSearch",
                }
            }
        ]
    )
    return results


client = pymongo.MongoClient(MONGO_URI)
db = client["spring"]
collection = db["records"]


def getDocsFromTxts():
    # Converts Txt docs into array of strings:# Directory containing the text files
    directory = "out2"

    # Initialize an empty list to store the strings
    pdf_texts = []
    titles = []

    # Iterate through the files in the directory
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        with open(file_path, "r", encoding="utf8") as file:
            file_content = file.read()
            pdf_texts.append(file_content)
            titles.append(filename)

    # Adds texts + embeddings
    for text, title in zip(pdf_texts, titles):
        new_entry = {
            "text": text,
            "title": title
        }
        collection.insert_one(new_entry)


def createEmbeddingsForDocs():
    i = 0
    for document in collection.find():
        i += 1
        document["plot_embedding_hf"] = generate_embedding_openAI('howdy')
        collection.replace_one({"_id": document["_id"]}, document)

# # new_entry = {"text": "12,000 GDP", "title": "BE500", "plot_embedding_hf": generate_embedding("12,000 GDP")}
# # collection.insert_one(new_entry)

# # new_entry = {"text": "some text here", "title": 'BE440', "plot_embedding_hf": generate_embedding("some text here")}
# # collection.insert_one(new_entry)


# # getDocsFromTxts()

# query = """
# Max. Pressure Drop / Element 15 psi (0.10 MPa)
# Max. Pressure Drop / 240” Vessel 60 psi (0.41 MPa)
# Max. Operating Pressure 600 psi (4.14 MPa)
# Max. Feed Flow Rate 75 gpm (17.0 m3/hr)
# Min. Concentrate Flow Rate 16 gpm (3.6 m3/hr)
# Max. Operating Temperature 113oF (45oC)
# Operating pH Range 2.0 – 11.0
# CIP pH Range 1.0 – 13.0
# """

# collection.delete_many({})
# getDocsFromTxts()
# createEmbeddingsForDocs()

query = """Max. Pressure Drop / Element 15 psi (0.10 MPa)
Max. Pressure Drop / 240” Vessel 60 psi (0.41 MPa)
Max. Operating Pressure 600 psi (4.14 MPa)
Max. Feed Flow Rate 75 gpm (17.0 m3/hr)
Min. Concentrate Flow Rate 16 gpm (3.6 m3/hr)
Max. Operating Temperature 113oF (45oC)
Operating pH Range 2.0 – 11.0
CIP pH Range 1.0 – 13.0"""

print("Query: ", query)
results = collection.aggregate(
    [
        {
            "$vectorSearch": {
                "queryVector": generate_embedding_openAI(query),
                "path": "plot_embedding_hf",
                "numCandidates": 100,
                "limit": 20,
                "index": "vector_index",
            }
        }
    ]
)


for document in results:
    print("Document title: ", document.get("title"))
    # print("Document text: " , document.get("text"))
