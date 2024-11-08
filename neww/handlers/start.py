from aiogram import types, Router
from aiogram.filters import Command  # Импорт фильтра Command

router = Router()

async def start_command(message: types.Message):
    await message.answer("Привет! Выберите действие:", reply_markup=create_main_keyboard())

def create_main_keyboard():
    # Создание кнопок в формате списка списков
    buttons = [
        [types.KeyboardButton(text="🔍 Поиск по артикулу")],
        [types.KeyboardButton(text="📋 Все товары")]
    ]

    # Создание и возврат экземпляра ReplyKeyboardMarkup с заданными кнопками
    return types.ReplyKeyboardMarkup(resize_keyboard=True, keyboard=buttons)

def register_start_handler(router: Router):
    # Регистрация обработчика команды /start с использованием фильтра Command
    router.message.register(start_command, Command(commands=['start']))