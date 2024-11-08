import sqlite3
import sys

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

def add_product(photo, name, sku, quantity, price):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute('''
            INSERT INTO products (photo, name, sku, quantity, price)
            VALUES (?, ?, ?, ?, ?)
        ''', (photo, name, sku, quantity, price))
        conn.commit()
        print("Товар добавлен успешно.")
    except sqlite3.IntegrityError:
        print("Ошибка: Товар с таким SKU уже существует.")
    finally:
        conn.close()

def view_products():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()

    if products:
        for product in products:
            print(f"ID: {product[0]}, Photo: {product[1]}, Name: {product[2]}, SKU: {product[3]}, Quantity: {product[4]}, Price: {product[5]}")
    else:
        print("Нет товаров в базе данных.")

    conn.close()

def edit_product(sku, quantity=None, price=None):
    conn = get_db_connection()
    cursor = conn.cursor()

    if quantity is not None:
        cursor.execute("UPDATE products SET quantity = ? WHERE sku = ?", (quantity, sku))

    if price is not None:
        cursor.execute("UPDATE products SET price = ? WHERE sku = ?", (price, sku))

    conn.commit()

    if cursor.rowcount == 0:
        print("Ошибка: Товар с таким SKU не найден.")
    else:
        print("Товар обновлён успешно.")

    conn.close()

def main():
    create_table()  # Убедимся, что таблица создана

    while True:
        print("\nКоманды:")
        print("1. Добавить товар")
        print("2. Просмотреть все товары")
        print("3. Редактировать товар")
        print("4. Выход")

        choice = input("Выберите команду: ")

        if choice == '1':
            photo = input("Введите URL фото товара: ")
            name = input("Введите название товара: ")
            sku = input("Введите артикул товара (SKU): ")
            quantity = int(input("Введите количество товара: "))
            price = float(input("Введите цену товара: "))
            add_product(photo, name, sku, quantity, price)

        elif choice == '2':
            view_products()

        elif choice == '3':
            sku = input("Введите артикул товара (SKU) для редактирования: ")
            quantity = input("Введите новое количество товара (или оставьте пустым для пропуска): ")
            price = input("Введите новую цену товара (или оставьте пустым для пропуска): ")

            quantity = int(quantity) if quantity else None
            price = float(price) if price else None

            edit_product(sku, quantity, price)

        elif choice == '4':
            print("Выход из программы.")
            sys.exit(0)

        else:
            print("Неверный выбор. Пожалуйста, попробуйте снова.")

if __name__ == '__main__':
    main()
