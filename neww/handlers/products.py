from aiogram import types, Dispatcher
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from database import get_product_by_sku

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

def register_product_handlers(dp: Dispatcher):
    dp.register_message_handler(show_all_products, lambda message: message.text == "📋 Все товары")
    dp.register_message_handler(search_product, lambda message: message.text == "🔍 Поиск по артикулу")
    dp.register_message_handler(search_by_sku)
