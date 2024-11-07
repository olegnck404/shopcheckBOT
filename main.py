import logging
from aiogram import Bot, Dispatcher
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.utils import executor
from config import API_TOKEN
from handlers import start_command, show_all_products, search_product, admin_login, add_product_name, add_product, search_by_sku
from db import create_products_table

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Инициализация бота и диспетчера
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())

# Создание таблицы в базе данных
create_products_table()

# Регистрация обработчиков
dp.register_message_handler(start_command, commands=['start'])
dp.register_message_handler(show_all_products, lambda message: message.text == "📋 Все товары")
dp.register_message_handler(search_product, lambda message: message.text == "🔍 Поиск по артикулу")
dp.register_message_handler(search_by_sku, lambda message: message.text.isdigit())
dp.register_message_handler(admin_login, lambda message: message.text.startswith("admin://"))
dp.register_callback_query_handler(add_product, lambda c: c.data == "add_product")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
