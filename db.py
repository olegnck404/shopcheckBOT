import sqlite3

def get_db_connection():
    conn = sqlite3.connect('products.db')
    conn.row_factory = sqlite3.Row  # Для получения результатов как словари
    return conn

def create_products_table():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        photo TEXT,
        name TEXT,
        sku TEXT UNIQUE,
        quantity INTEGER,
        price REAL
    )
    ''')
    conn.commit()
    conn.close()

def get_product_by_sku(sku):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products WHERE sku = ?", (sku,))
    product = cursor.fetchone()
    conn.close()
    return product

def insert_product(name, sku, price, quantity):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO products (name, sku, price, quantity) VALUES (?, ?, ?, ?)",
                   (name, sku, price, quantity))
    conn.commit()
    conn.close()

def delete_product_by_sku(sku):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM products WHERE sku = ?", (sku,))
    conn.commit()
    conn.close()

def get_all_products():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT sku, name FROM products")
    products = cursor.fetchall()
    conn.close()
    return products
