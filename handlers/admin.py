from aiogram import types, Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import Text  # Import Text filter for text matching

class AdminStates(StatesGroup):
    ENTER_PASSWORD = State()  
    CHOOSE_ACTION = State()  
    ADD_PRODUCT = State()  
    EDIT_PRODUCT = State()  
    VIEW_PRODUCT = State()  

ADMIN_PASSWORD = "158x12llo"

async def admin_login(message: types.Message):
    if message.text.startswith("admin://"):
        password = message.text.split("://")[1]
        if password == ADMIN_PASSWORD:
            await message.answer("Добро пожаловать в админ-панель! Выберите действие:")
            await AdminStates.CHOOSE_ACTION.set()
        else:
            await message.answer("Неверный пароль.")
    else:
        await message.answer("Используйте формат: admin://ваш_пароль")

def register_admin_handlers(router: Router):
    # Register the admin login handler with the router
    router.message.register(admin_login, Text(startswith="admin://"))