from aiogram import types, Dispatcher

def create_main_keyboard():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(types.KeyboardButton("🔍 Поиск по артикулу"), types.KeyboardButton("📋 Все товары"))
    return keyboard

async def start_command(message: types.Message):
    await message.answer("Привет! Выберите действие:", reply_markup=create_main_keyboard())

def register_start_handler(dp: Dispatcher):
    dp.register_message_handler(start_command, commands=['start'])
