from aiogram import Dispatcher
from aiogram import Router
from .start import register_start_handler
from .products import register_product_handlers
from .admin import register_admin_handlers

# Create a router instance
router = Router()

def register_handlers(dp: Dispatcher):
    # Register handlers with the router
    register_start_handler(router)
    register_product_handlers(router)
    register_admin_handlers(router)

    # Include the router in the dispatcher
    dp.include_router(router)