from aiogram import Bot
from aiogram.types import WebAppInfo
from config.settings import WEBAPP_URL

async def send_webapp_response(bot: Bot, chat_id: int, message: str):
    await bot.send_message(
        chat_id=chat_id,
        text=message,
        reply_markup=WebAppInfo(url=WEBAPP_URL)
    )