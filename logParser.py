import re
import numpy as np
from langchain_openai import ChatOpenAI
from weaviate.classes.query import MetadataQuery
import weaviate
import os
import sys

def similaritySearch(prompt):
    #Connect to weaviate instance
    client = weaviate.connect_to_local(
        headers={
            "X-OpenAI-Api-Key" : os.getenv("OPENAI_API_KEY")
        }
    )
    collection = client.collections.get("LogParser")

    # Test
    result = collection.query.near_text(
        query=prompt,
        distance=0.7,
        return_metadata=MetadataQuery(distance=True)
        )
    for o in result.objects:
        print(o.properties["log"], o.metadata.distance)

    client.close()

if __name__ == '__main__':
    if len(sys.argv) == 1:
        print("Please add a prompt")
    
    else:
        similaritySearch(" ".join(sys.argv[1:]))