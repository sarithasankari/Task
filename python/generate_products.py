import csv
import random


electronics = [
    "Apple iPhone 14",
    "Apple iPhone 14 Pro",
    "Apple iPhone 13",
    "Samzung Galaxy S21",      
    "Samsung Galaxy S21",
    "Samsung Galaxy S22 Ultra",
    "OnePlus 11",
    "Redmi Note 12",
    "Sony WH-1000XM5 Headphones",
    "Boat Rockerz 450"
]

fashion = [
    "Nike Running Shoes",
    "Nike Running Shoe",      
    "Adidas Sports T-Shirt",
    "Adibas Sports T-Shirt", 
    "Levi's Slim Fit Jeans",
    "Puma Casual Sneakers",
    "Zara Women's Jacket",
    "H&M Cotton Shirt",
    "Ray-Ban Aviator Sunglasses"
]

groceries = [
    "Organic Basmati Rice 5kg",
    "Basmati Rice 5 kg",     
    "Fortune Sunflower Oil 1L",
    "Fortune Sunflower Oill 1L", 
    "Tata Salt 1kg",
    "Aashirvaad Atta 10kg",
    "Nescafe Classic Coffee 200g",
    "Bru Instant Coffee 200g",
    "Amul Butter 500g"
]


base_products = electronics + fashion + groceries

def generate_products(total=500):
    products = []

    for i in range(1, total + 1):
        name = random.choice(base_products)

        
        if random.random() < 0.2:
            name = name + " (New Edition)"
        elif random.random() < 0.1:
            name = name.replace(" ", "  ") 

        products.append({
            "product_id": i,
            "product_name": name
        })

    return products

def write_to_csv(products, filename="products.csv"):
    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=["product_id", "product_name"]
        )
        writer.writeheader()
        writer.writerows(products)

if __name__ == "__main__":
    products = generate_products(500)
    write_to_csv(products)
    print("products.csv generated successfully!")
