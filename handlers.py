from aiogram import types
from aiogram.types import CallbackQuery
from aiogram.dispatcher import FSMContext
from db import get_product_by_sku, insert_product, delete_product_by_sku
from keyboards import create_main_keyboard, create_products_keyboard, create_admin_keyboard, create_product_management_keyboard
from states import AdminStates
from config import ADMIN_PASSWORD

# Обработчик команды /start
async def start_command(message: types.Message):
    await message.answer("Привет! Выберите действие:", reply_markup=create_main_keyboard())

# Обработчик нажатия на кнопку "Все товары"
async def show_all_products(message: types.Message):
    keyboard = create_products_keyboard()
    await message.answer("Список товаров:", reply_markup=keyboard)

# Обработчик нажатия на кнопку "Поиск по артикулу"
async def search_product(message: types.Message):
    await message.answer("Введите артикул товара:")

# Обработчик ввода артикула
async def search_by_sku(message: types.Message):
    sku = message.text.strip()
    product = get_product_by_sku(sku)
    
    if product:
        _, photo, name, sku, quantity, price = product
        if photo:
            await message.answer_photo(photo, caption=f"{name}\nSKU: {sku}\nЦена: {price}\nКоличество: {quantity}")
        else:
            await message.answer(f"{name}\nSKU: {sku}\nЦена: {price}\nКоличество: {quantity}")
    else:
        await message.answer("❌ Товар с таким артикулом не найден.")

# Вход в админ-панель
async def admin_login(message: types.Message):
    password = message.text.split("://")[1]
    if password == ADMIN_PASSWORD:
        await message.answer("Добро пожаловать, администратор! Выберите действие:", reply_markup=create_admin_keyboard())
        await AdminStates.CHOOSE_ACTION.set()
    else:
        await message.answer("❌ Неверный пароль!")

# Обработчики для админ-панели (добавление, удаление, редактирование)
async def add_product(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.message.answer("Введите название товара:")
    await AdminStates.ADD_PRODUCT.set()
    await callback_query.answer()

async def add_product_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Введите артикул товара:")
    await AdminStates.ADD_PRODUCT.set()

# Функции для добавления товара, удаления и т.д.
