from aiogram import Router, F
from aiogram.types import Message
from bot.utils.database import get_db

router = Router()

@router.message(lambda message: message.text == "Написать в поддержку")
async def handle_support(message: Message):
    await message.answer("Напишите ваше сообщение, и мы передадим его мастеру или администратору.")

@router.message(F.text)
async def handle_message(message: Message, state: FSMContext):
    async with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO messages (user_id, master_id, text)
            VALUES (?, ?, ?)
        ''', (message.from_user.id, 1, message.text))  # master_id=1 для поддержки
        conn.commit()
    
    await message.answer("Ваше сообщение отправлено!")