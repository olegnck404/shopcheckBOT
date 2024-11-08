from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from config import Settings


class AdminStates(StatesGroup):
    ENTER_PASSWORD = State()
    CHOOSE_ACTION = State()
    ADD_PRODUCT = State()
    EDIT_PRODUCT = State()
    VIEW_PRODUCT = State()


router = Router(name=__name__)


@router.message(F.text.startswith("admin://"))
async def admin_login(message: types.Message, settings: Settings):
    if message.text.startswith("admin://"):
        password = message.text.split("://")[1]
        if password == settings.admin_password.get_secret_value():
            await message.answer(
                "Добро пожаловать в админ-панель! Выберите действие:")
            await AdminStates.CHOOSE_ACTION.set()
        else:
            await message.answer("Неверный пароль.")
    else:
        await message.answer("Используйте формат: admin://ваш_пароль")
