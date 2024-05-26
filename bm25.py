

from beir import util, LoggingHandler
from beir.retrieval.evaluation import EvaluateRetrieval
from beir.retrieval.search.lexical import BM25Search as BM25
import tqdm
import json

import pathlib, os, random
import logging

from scrape.pdf2text import extract_text_and_tables

#### Just some code to print debug information to stdout
logging.basicConfig(format='%(asctime)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    level=logging.INFO,
                    handlers=[LoggingHandler()])


def prepare_data(filename):
    text_content, _ = extract_text_and_tables(filename)
    return {"title": "", "text": "\n".join(text_content)}
dir = "C:/Users/deepa/Downloads/lenntech-data-sheets"

corpus = dict()
# dir = "samples"
all_files = os.listdir(dir)
for file in tqdm.tqdm(all_files,total=len(all_files)):
    if(file.endswith(".pdf")):
        corpus[file] = prepare_data(f"{dir}/{file}")
        with open('preprocess/intermed_data.jsonl','a+') as fp:
            fp.write(json.dumps([file,corpus[file]]))
# queries = {"rahul": "Comparitive membrane?"}
#
#
# hostname = "localhost:9200"
# index_name = "team42"
#
# #### Intialize ####
# # (1) True - Delete existing index and re-index all documents from scratch
# # (2) False - Load existing index
# initialize = True # False
#
# #### Sharding ####
# # (1) For datasets with small corpus (datasets ~ < 5k docs) => limit shards = 1
# # SciFact is a relatively small dataset! (limit shards to 1)
# number_of_shards = 1
# model = BM25(index_name=index_name, hostname=hostname, initialize=initialize, number_of_shards=number_of_shards)
#
# # (2) For datasets with big corpus ==> keep default configuration
# # model = BM25(index_name=index_name, hostname=hostname, initialize=initialize)
# retriever = EvaluateRetrieval(model,[3])
#
# #### Retrieve dense results (format of results is identical to qrels)
# results = retriever.retrieve(corpus, queries)
#
# print(results)