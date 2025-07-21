from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from bot.utils.keyboard import get_main_menu

router = Router()

@router.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer(
        "Добро пожаловать в тату-салон! Выберите действие:",
        reply_markup=get_main_menu()
    )