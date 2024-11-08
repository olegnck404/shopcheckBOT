import sqlite3

def get_db_connection():
    conn = sqlite3.connect('products.db')
    return conn

def create_table():
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

create_table()  # Ensure the table is created on startup.
