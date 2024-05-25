import pymongo
import requests
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

MONGO_URI = os.getenv("MONGO_URL")
hf_token = os.getenv("HF_TOKEN")
embedding_url = "https://api-inference.huggingface.co/pipeline/feature-extraction/sentence-transformers/all-MiniLM-L6-v2"


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
    directory = "out"

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
    for text,title in zip(pdf_texts,titles):
        new_entry = {"text": text, "title": title, "plot_embedding_hf": generate_embedding(text)}
        collection.insert_one(new_entry)
        # print(text + "\n")






# new_entry = {"text": "12,000 GDP", "title": "BE500", "plot_embedding_hf": generate_embedding("12,000 GDP")}
# collection.insert_one(new_entry)

# new_entry = {"text": "some text here", "title": 'BE440', "plot_embedding_hf": generate_embedding("some text here")}
# collection.insert_one(new_entry)


  

# collection.delete_many({})
# getDocsFromTxts()

# query = "45.4 m3/day production:"

query = """
- 45.4 m3/day production:
- 99.5%% salt rejection
- maximum operating pressure of 600 psi
- 8-inch diameter
- pH range of 2-11
"""
print("Query: ", query)
results = collection.aggregate(
    [
        {
            "$vectorSearch": {
                "queryVector": generate_embedding(query),
                "path": "plot_embedding_hf",
                "numCandidates": 100,
                "limit": 2,
                "index": "vector_index",
            }
        }
    ]
)


for document in results:
    print("Document title: " , document.get("title"))
    # print("Document text: " , document.get("text"))
