import json
from aiogram import Router
from aiogram.types import Message
from bot.utils.database import get_db
from bot.services.master_service import get_masters
from bot.utils.keyboard import get_main_menu
from config.constants import LOCALE

router = Router()

@router.message(lambda message: message.text == "Выбрать мастера")
async def show_masters(message: Message):
    masters = await get_masters()
    if not masters:
        await message.answer(LOCALE["ru"]["no_masters"])
        return
    
    response = "Наши мастера:\n"
    for master in masters:
        response += (
            f"Имя: {master['name']}\n"
            f"Стаж: {master['experience']} лет\n"
            f"Описание: {master['description']}\n"
            f"Портфолио: {', '.join(master['portfolio_urls'])}\n\n"
        )
    await message.answer(response, reply_markup=get_main_menu())