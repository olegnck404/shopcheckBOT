from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


def create_main_keyboard() -> ReplyKeyboardMarkup:
    buttons = [
        [
            KeyboardButton(text="🔍 Поиск по артикулу"),
            KeyboardButton(text="📋 Все товары")
        ]
    ]
    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)


def create_products_keyboard():
    pass
