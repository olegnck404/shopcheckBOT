from aiogram import Dispatcher
from .start import register_start_handler
from .products import register_product_handlers
from .admin import register_admin_handlers

def register_handlers(dp: Dispatcher):
    register_start_handler(dp)
    register_product_handlers(dp)
    register_admin_handlers(dp)
