import csv
import json
import mysql.connector
from sentence_transformers import SentenceTransformer

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "12345", 
    "database": "product_db"
}

def load_products(filename="products.csv"):
    products = []
    with open(filename, mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            products.append(row)
    return products

def generate_embeddings_and_store(products):
    print("Loading SentenceTransformer model...")
    model = SentenceTransformer('all-MiniLM-L6-v2') 
    
    print("Connecting to database...")
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
     
        
        print(f"Processing {len(products)} products...")
        
        batch_size = 100
        for i in range(0, len(products), batch_size):
            batch = products[i:i+batch_size]
            names = [p["product_name"] for p in batch]
            
            embeddings = model.encode(names)
            
            insert_data = []
            for product, embedding in zip(batch, embeddings):
                insert_data.append((
                    int(product["product_id"]),
                    product["product_name"],
                    json.dumps(embedding.tolist()) 
                ))
        
            sql = """INSERT INTO products_vectors (product_id, product_name, vector) 
                     VALUES (%s, %s, %s) 
                     ON DUPLICATE KEY UPDATE product_name=VALUES(product_name), vector=VALUES(vector)"""
            cursor.executemany(sql, insert_data)
            conn.commit()
            print(f"Processed batch {i // batch_size + 1}")

        print("All products embedded and stored successfully!")

    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

if __name__ == "__main__":
    products = load_products()
    generate_embeddings_and_store(products)
