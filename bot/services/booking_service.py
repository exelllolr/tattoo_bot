from datetime import datetime, timedelta
import sqlite3
from bot.utils.database import get_db
from config.settings import WORKING_HOURS, WORKING_DAYS

async def book_appointment(user_id: int, master_id: int, date: str, time: int):
    if not is_valid_slot(date, time):
        return False, "Выбранное время недоступно."
    
    async with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT id FROM appointments
            WHERE master_id = ? AND date = ? AND time = ? AND status = 'confirmed'
        ''', (master_id, date, time))
        if cursor.fetchone():
            return False, "Это время уже занято."
        
        cursor.execute('''
            INSERT INTO appointments (user_id, master_id, date, time, status)
            VALUES (?, ?, ?, ?, 'confirmed')
        ''', (user_id, master_id, date, time))
        conn.commit()
        return True, "Запись успешно создана!"

async def get_available_slots(master_id: int, date: str):
    slots = []
    async with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT time FROM appointments
            WHERE master_id = ? AND date = ? AND status = 'confirmed'
        ''', (master_id, date))
        booked_slots = [row[0] for row in cursor.fetchall()]
    
    for hour in WORKING_HOURS:
        if hour not in booked_slots:
            slots.append(hour)
    return slots

def is_valid_slot(date: str, time: int) -> bool:
    try:
        appointment_date = datetime.strptime(date, '%Y-%m-%d')
        if appointment_date.weekday() not in WORKING_DAYS:
            return False
        if time not in WORKING_HOURS:
            return False
        return True
    except ValueError:
        return False