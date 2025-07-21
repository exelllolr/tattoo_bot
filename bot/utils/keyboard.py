from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, WebAppInfo
from config.settings import WEBAPP_URL

def get_main_menu():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Выбрать мастера", web_app=WebAppInfo(url=WEBAPP_URL + "/masters"))],
            [KeyboardButton(text="Мои записи", web_app=WebAppInfo(url=WEBAPP_URL + "/appointments"))],
            [KeyboardButton(text="Написать в поддержку")]
        ],
        resize_keyboard=True
    )
    return keyboard