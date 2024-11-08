import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from config import Settings
from handlers import products, admin, start

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger("bot")

async def handle_startup(bot: Bot):
    await bot.delete_webhook(drop_pending_updates=True)
    logger.info("Bot started.")

async def handle_shutdown(bot: Bot):
    logger.info("Bot stopped.")

async def main():
    settings = Settings()
    logger.debug(settings)

    bot = Bot(token=settings.api_token.get_secret_value())
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)
    dp['settings'] = settings
    dp.startup.register(handle_startup)
    dp.shutdown.register(handle_shutdown)
    dp.include_routers(admin.router, start.router, products.router)

    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())