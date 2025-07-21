from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from bot.utils.database import get_db

router = Router()

@router.message(Command("add_master"))
async def add_master(message: Message):
    if not is_admin(message.from_user.id):
        await message.answer("У вас нет прав администратора.")
        return
    
    args = message.text.split(maxsplit=4)
    if len(args) != 5:
        await message.answer("Формат: /add_master <имя> <стаж> <описание> <аватар_url> <портфолио_urls>")
        return
    
    _, name, experience, description, avatar_url = args
    portfolio_urls = '[]'  # Временная заглушка
    
    async with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO masters (name, experience, description, avatar_url, portfolio_urls)
            VALUES (?, ?, ?, ?, ?)
        ''', (name, int(experience), description, avatar_url, portfolio_urls))
        conn.commit()
    
    await message.answer(f"Мастер {name} добавлен!")

@router.message(Command("cancel_appointment"))
async def cancel_appointment(message: Message):
    if not is_admin(message.from_user.id):
        await message.answer("У вас нет прав администратора.")
        return
    
    args = message.text.split(maxsplit=1)
    if len(args) != 2:
        await message.answer("Формат: /cancel_appointment <id_записи>")
        return
    
    appointment_id = args[1]
    async with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE appointments
            SET status = 'cancelled'
            WHERE id = ?
        ''', (appointment_id,))
        conn.commit()
    
    await message.answer(f"Запись {appointment_id} отменена!")

def is_admin(user_id: int) -> bool:
    # Простая проверка админа (в продакшене заменить на список админов в БД)
    return user_id == 123456789  # Замените на реальный ID админа