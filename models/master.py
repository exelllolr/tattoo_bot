import json
from aiogram import Router
from aiogram.types import Message
from bot.utils.database import get_db
from bot.services.master_service import get_masters

router = Router()

@router.message(lambda message: message.text == "Выбрать мастера")
async def show_masters(message: Message):
    masters = await get_masters()
    if not masters:
        await message.answer("Мастера пока не добавлены.")
        return
    
    # Ответ будет обрабатываться через Mini App
    await message.answer("Открывайте список мастеров в Mini App!", reply_markup=get_main_menu())