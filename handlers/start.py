from aiogram import types, Router
from aiogram.filters import CommandStart

from keyboards.keyboards import create_main_keyboard

router = Router(name=__name__)

@router.message(CommandStart())
async def start_command(message: types.Message):
    await message.answer("Привет! Выберите действие:",
                         reply_markup=create_main_keyboard())


