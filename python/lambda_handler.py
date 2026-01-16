import json
import mysql.connector
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

DB_CONFIG = {
    "host": "localhost", 
    "user": "root",
    "password": "12345",
    "database": "product_db"
}

print("Loading model...")
model = SentenceTransformer('all-MiniLM-L6-v2')

def get_product_vectors():
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()
    cursor.execute("SELECT product_name, vector FROM products_vectors")
    rows = cursor.fetchall()
    
    product_names = []
    vectors = []
    
    for name, vector_json in rows:
        product_names.append(name)
        vectors.append(json.loads(vector_json))
        
    cursor.close()
    conn.close()
    
    return product_names, np.array(vectors)

def lambda_handler(event, context):
    try:
    
        query = event.get("query") or event.get("queryStringParameters", {}).get("query")
        
        if not query:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "Query parameter is required"})
            }

        product_names, product_vectors = get_product_vectors()
        
        if not product_names:
             return {
                "statusCode": 404,
                "body": json.dumps({"error": "No products found in database"})
            }

        query_vector = model.encode([query])[0]
        

        similarities = cosine_similarity([query_vector], product_vectors)[0]
        

        top_k = 5
        top_indices = similarities.argsort()[-top_k:][::-1]
        
        results = []
        for idx in top_indices:
            results.append({
                "product_name": product_names[idx],
                "score": float(similarities[idx])
            })
            
        return {
            "statusCode": 200,
            "body": json.dumps(results)
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }

if __name__ == "__main__":
    # Local Test
    test_event = {"query": "running shoes"}
    print(lambda_handler(test_event, None))
