from aiogram import types, Dispatcher
from aiogram.fsm.context import FSMContext  # Updated import for FSMContext in Aiogram 3.x
from aiogram.dispatcher.filters.state import State, StatesGroup

class AdminStates(StatesGroup):
    ENTER_PASSWORD = State()  
    CHOOSE_ACTION = State()  
    ADD_PRODUCT = State()  
    EDIT_PRODUCT = State()  
    VIEW_PRODUCT = State()  

ADMIN_PASSWORD = "158x12llo"

async def admin_login(message: types.Message):
    password = message.text.split("://")[1]
    
    if password == ADMIN_PASSWORD:
        await message.answer("Добро пожаловать в админ-панель! Выберите действие:")
        await AdminStates.CHOOSE_ACTION.set()
        
def register_admin_handlers(dp: Dispatcher):
    dp.register_message_handler(admin_login, lambda message: message.text.startswith("admin://"))
