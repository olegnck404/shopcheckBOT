from aiogram import types, Router
from aiogram.filters import Text  # Import Text filter for text matching
from database import get_product_by_sku

router = Router()

async def show_all_products(message: types.Message):
    keyboard = create_products_keyboard()
    await message.answer("Список товаров:", reply_markup=keyboard)

async def search_product(message: types.Message):
    await message.answer("Введите артикул товара:")

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

def create_products_keyboard():
    # Create your keyboard here
    pass

def register_product_handlers(router: Router):
    # Register handlers with the router using Text filter correctly
    router.message.register(show_all_products, Text(text="📋 Все товары"))  # Use text argument for exact match
    router.message.register(search_product, Text(text="🔍 Поиск по артикулу"))
    router.message.register(search_by_sku)  # This will match any text input