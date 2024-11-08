from aiogram import types, Router
from aiogram.filters import Command  # Import Command filter

router = Router()

async def start_command(message: types.Message):
    await message.answer("Привет! Выберите действие:", reply_markup=create_main_keyboard())

def create_main_keyboard():
    # Create an instance of ReplyKeyboardMarkup
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)

    # Define buttons
    button_search = types.KeyboardButton("🔍 Поиск по артикулу")
    button_all_products = types.KeyboardButton("📋 Все товары")

    # Add buttons to the keyboard
    keyboard.add(button_search, button_all_products)

    return keyboard

def register_start_handler(router: Router):
    # Register the command handler with the Command filter
    router.message.register(start_command, Command(commands=['start']))