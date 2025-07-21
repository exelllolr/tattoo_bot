from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from bot.utils.database import get_db
from bot.services.booking_service import book_appointment, get_available_slots
from datetime import datetime, timedelta
from config.settings import WORKING_HOURS, WORKING_DAYS

router = Router()

class BookingState(StatesGroup):
    master_id = State()
    date = State()
    time = State()

@router.message(lambda message: message.text == "Мои записи")
async def show_appointments(message: Message):
    async with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT a.id, m.name, a.date, a.time, a.status
            FROM appointments a
            JOIN masters m ON a.master_id = m.id
            WHERE a.user_id = ?
        ''', (message.from_user.id,))
        appointments = cursor.fetchall()
    
    if not appointments:
        await message.answer("У вас нет активных записей.")
        return
    
    response = "Ваши записи:\n"
    for app in appointments:
        response += f"ID: {app[0]}, Мастер: {app[1]}, Дата: {app[2]}, Время: {app[3]}:00, Статус: {app[4]}\n"
    await message.answer(response)