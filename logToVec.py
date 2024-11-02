import weaviate
import weaviate.classes as wvc
import os
import pandas as pd
import time

#Before Running this code run the docker-compse file
#Connect to weaviate instance
client = weaviate.connect_to_local(
    host = "localhost",
    headers={
        "X-OpenAI-Api-Key" : os.getenv("OPENAI_API_KEY")
    }
)

# Define the Schema object to use
product_schema = {
    "class": "Logs",
    "description": "Log entries for recent log file",
    "vectorizer": "text2vec-openai",
    "moduleConfig": {
        "text2vec-openai": {
          "model": "ada",
          "modelVersion": "002",
          "type": "text"
        }
    },
    "properties": [{
        "name": "entry",
        "description": "log entry",
        "dataType": ["text"]
    }]
}

# add the Article schema
client.schema.create_class(product_schema)

# get the schema to make sure it worked
client.schema.get()

#configure weaviate batch
client.batch.configure(
    batch_size = 10, #starting batch size
    dynamic = True, #dynamically increase/decrease based on performance
    timeout_retries = 3 #  timeout retries if anything goes wrong
)

#read log file and change each entry into an embedding
f = open("samplelog.ext", "r")

counter = 0
for entry in f:
    if (counter %10 == 0):
        print(f"Import {counter} / {len(f)} ")
    
    properties = {"entry" : entry}

    client.batch.add_data_object(properties, "Logs")
    counter += 1
    time.sleep(1)

# Test that all data has loaded – get object count
result = (
    client.query.aggregate("Logs")
    .with_fields("meta { count }")
    .do()
)
print("Object count: ", result["data"]["Aggregate"]["Logs"], "\n")