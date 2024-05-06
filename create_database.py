import sqlite3

# Connect to the SQLite database (creates a new file if it doesn't exist)
conn = sqlite3.connect('phones.db')
cursor = conn.cursor()

# Create the table
cursor.execute("""
CREATE TABLE IF NOT EXISTS phones (
    ProductID INTEGER PRIMARY KEY,
    ProductName TEXT,
    Brand TEXT,
    Storage TEXT,
    Color TEXT,
    Price REAL,
    QuantityInStock INTEGER,
    Location TEXT
)
""")

# Sample data
data = [
    (1, 'iPhone 13', 'Apple', '128GB', 'Blue', 999, 20, 'Shelf 1'),
    (2, 'Galaxy S21', 'Samsung', '256GB', 'Phantom Black', 899, 15, 'Shelf 2'),
    (3, 'Pixel 6', 'Google', '128GB', 'Stormy Black', 799, 18, 'Shelf 3'),
    (4, 'OnePlus 9', 'OnePlus', '256GB', 'Winter Mist', 729, 25, 'Shelf 1'),
    (5, 'Xperia 1 III', 'Sony', '256GB', 'Frosted Black', 1199, 10, 'Shelf 2'),
    (6, 'Mi 11X', 'Xiaomi', '128GB', 'Cosmic Black', 599, 30, 'Shelf 3'),
    (7, 'Find X3 Pro', 'OPPO', '256GB', 'Gloss Black', 1099, 12, 'Shelf 1'),
    (8, 'ROG Phone 5', 'ASUS', '256GB', 'Phantom Black', 999, 20, 'Shelf 2'),
    (9, 'Vivo X60 Pro', 'Vivo', '256GB', 'Midnight Black', 799, 15, 'Shelf 3'),
    (10, 'Moto G Power 2021', 'Motorola', '64GB', 'Aurora Black', 249, 35, 'Shelf 1')
]

# Insert the data
cursor.executemany("INSERT INTO phones VALUES (?, ?, ?, ?, ?, ?, ?, ?)", data)
conn.commit()

# Close the connection
conn.close()