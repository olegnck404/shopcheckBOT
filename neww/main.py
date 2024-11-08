import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram import Router
from aiogram.utils import start_polling  # Corrected import for polling
from config import API_TOKEN
from handlers import register_handlers

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Инициализация бота и диспетчера
bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

# Регистрация обработчиков
register_handlers(dp)

async def on_startup(dp: Dispatcher):
    logging.info("Bot is starting...")

if __name__ == '__main__':
    start_polling(dp, on_startup=on_startup)  # Use start_polling directly
