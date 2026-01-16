CREATE DATABASE IF NOT EXISTS product_db;

USE product_db;

DROP TABLE IF EXISTS products_vectors;

CREATE TABLE IF NOT EXISTS products_vectors (
    product_id INT PRIMARY KEY,
    product_name VARCHAR(255) NOT NULL,
    vector JSON NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
