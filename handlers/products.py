from aiogram import types, Router, F
from database import get_product_by_sku, get_db_connection
from keyboards.keyboards import create_products_keyboard

router = Router(name=__name__)

@router.message(F.text == "📋 Все товары")
async def show_all_products(message: types.Message):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()
    conn.close()

    if products:
        product_list = ""
        for product in products:
            _, photo, name, sku, quantity, price = product
            product_list += f"ID: {product[0]}, Name: {name}, SKU: {sku}, Quantity: {quantity}, Price: {price}\n"

        await message.answer(f"Список товаров:\n{product_list}")
    else:
        await message.answer("Нет товаров в базе данных.")

@router.message(F.text == "🔍 Поиск по артикулу")
async def search_product(message: types.Message):
    await message.answer("Введите артикул товара:")

@router.message()
async def search_by_sku(message: types.Message):
    sku = message.text.strip()
    product = get_product_by_sku(sku)

    if product:
        _, photo, name, sku, quantity, price = product
        caption = f"{name}\nSKU: {sku}\nЦена: {price}\nКоличество: {quantity}"
        if photo:
            await message.answer_photo(photo=photo, caption=caption)
        else:
            await message.answer(caption)
    else:
        await message.answer("❌ Товар с таким артикулом не найден.")
