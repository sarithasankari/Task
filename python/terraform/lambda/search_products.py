import json
import numpy as np
from openai import OpenAI

client = OpenAI(api_key="YOUR_OPENAI_API_KEY")

products_vectors = [
    {"id": 1, "name": "iPhone 15", "vector": [0.1, 0.2, 0.3]},
    {"id": 2, "name": "Samsung Galaxy", "vector": [0.0, 0.1, 0.2]},
    {"id": 3, "name": "MacBook Pro", "vector": [0.5, 0.4, 0.3]},
]

def cosine_similarity(v1, v2):
    v1 = np.array(v1)
    v2 = np.array(v2)
    return np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))

def lambda_handler(event, context):
    query = event.get("query", "")
    if not query:
        return {"statusCode": 400, "body": "Query missing"}

    embedding = client.embeddings.create(
        model="text-embedding-3-small",
        input=query
    ).data[0].embedding

    results = []
    for product in products_vectors:
        sim = cosine_similarity(embedding, product["vector"])
        results.append({"product": product["name"], "similarity": sim})

    top5 = sorted(results, key=lambda x: x["similarity"], reverse=True)[:5]

    return {"statusCode": 200, "body": json.dumps(top5)}
