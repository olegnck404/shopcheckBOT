from aiogram import types, Router, F
from database import get_product_by_sku

router = Router(name=__name__)


def create_products_keyboard():
    pass


@router.message(F.text == "📋 Все товары")
async def show_all_products(message: types.Message):
    keyboard = create_products_keyboard()
    await message.answer("Список товаров:", reply_markup=keyboard)

@router.message(F.text=="🔍 Поиск по артикулу")
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
