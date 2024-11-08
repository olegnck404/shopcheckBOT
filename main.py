import logging
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
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

async def main():
    # Start polling using the Dispatcher instance
    await dp.start_polling(bot, on_startup=on_startup)

if __name__ == '__main__':
    asyncio.run(main())