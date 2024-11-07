from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from db import get_all_products

# Клавиатура для основного меню
def create_main_keyboard():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(
        KeyboardButton("🔍 Поиск по артикулу"),
        KeyboardButton("📋 Все товары")
    )
    return keyboard

# Клавиатура для админ-панели
def create_admin_keyboard():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(
        KeyboardButton("📋 Отобразить все товары"),
        KeyboardButton("Выйти из админ-панели")
    )
    return keyboard

# Инлайн-клавиатура для товаров
def create_products_keyboard(is_admin=False):
    keyboard = InlineKeyboardMarkup(row_width=1)
    products = get_all_products()
    
    for sku, name in products:
        keyboard.add(InlineKeyboardButton(name, callback_data=f"view_product_{sku}"))
    
    if is_admin:
        keyboard.add(InlineKeyboardButton("➕ Добавить товар", callback_data="add_product"))
    
    return keyboard

# Клавиатура для управления продуктом
def create_product_management_keyboard():
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(
        InlineKeyboardButton("✏️ Изменить товар", callback_data="edit_product"),
        InlineKeyboardButton("❌ Удалить товар", callback_data="delete_product"),
        InlineKeyboardButton("↩️ Назад", callback_data="back_to_main_menu")
    )
    return keyboard
