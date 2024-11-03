import weaviate
from weaviate.classes.config import Configure
import os
import pandas as pd
import time

#Before Running this code run the docker-compse file
#Connect to weaviate instance
client = weaviate.connect_to_local(
    headers={
        "X-OpenAI-Api-Key" : os.getenv("OPENAI_API_KEY")
    }
)

#initialize model and parameters
embeddings = client.collections.create(
    name = "LogParser",
    vectorizer_config=[
        Configure.NamedVectors.text2vec_openai(
            name="Logs",
            source_properties=["log"],
            model="text-embedding-3-small",
            dimensions=1536
        )
    ]
)

collection = client.collections.get("LogParser")

#read log file and change each entry into an embedding
f = open("samplelog.txt", "r")

#import data
counter = 0
with collection.batch.dynamic() as batch:
    for entry in f:
        print(entry)
        if entry == "\n":
            print("Line Skipped")
            continue
        if (counter %10 == 0):
            print(f"Import {counter} / total")
        
        weaviate_obj = {
            "log": entry
        }

        batch.add_object(
            properties=weaviate_obj
        )
        counter += 1
        time.sleep(0.1)

f.close()
client.close()