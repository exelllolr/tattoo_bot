from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from bot.utils.database import get_db
from bot.services.booking_service import book_appointment, get_available_slots
from bot.services.master_service import get_masters
from datetime import datetime, timedelta
from config.settings import WORKING_HOURS, WORKING_DAYS
from config.constants import LOCALE

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
        await message.answer(LOCALE["ru"]["no_appointments"])
        return
    
    response = "Ваши записи:\n"
    for app in appointments:
        response += f"ID: {app[0]}, Мастер: {app[1]}, Дата: {app[2]}, Время: {app[3]}:00, Статус: {app[4]}\n"
    await message.answer(response)

@router.message(lambda message: message.text == "Записаться")
async def start_booking(message: Message, state: FSMContext):
    masters = await get_masters()
    if not masters:
        await message.answer(LOCALE["ru"]["no_masters"])
        return
    
    response = "Выберите мастера:\n"
    for master in masters:
        response += f"{master['id']}. {master['name']} ({master['experience']} лет)\n"
    await message.answer(response)
    await state.set_state(BookingState.master_id)

@router.message(BookingState.master_id)
async def process_master_id(message: Message, state: FSMContext):
    try:
        master_id = int(message.text)
        masters = await get_masters()
        if not any(master['id'] == master_id for master in masters):
            await message.answer("Неверный ID мастера. Попробуйте снова.")
            return
        await state.update_data(master_id=master_id)
        await message.answer("Выберите дату (ГГГГ-ММ-ДД):")
        await state.set_state(BookingState.date)
    except ValueError:
        await message.answer("Пожалуйста, введите число (ID мастера).")

@router.message(BookingState.date)
async def process_date(message: Message, state: FSMContext):
    date = message.text
    if not is_valid_date(date):
        await message.answer(LOCALE["ru"]["invalid_slot"])
        return
    
    data = await state.get_data()
    master_id = data['master_id']
    slots = await get_available_slots(master_id, date)
    if not slots:
        await message.answer("Нет доступных слотов на эту дату.")
        return
    
    response = "Доступные слоты:\n" + "\n".join(f"{slot}:00" for slot in slots)
    await message.answer(response)
    await state.update_data(date=date)
    await state.set_state(BookingState.time)

@router.message(BookingState.time)
async def process_time(message: Message, state: FSMContext):
    try:
        time = int(message.text)
        data = await state.get_data()
        success, message_text = await book_appointment(
            message.from_user.id, data['master_id'], data['date'], time
        )
        await message.answer(message_text)
        if success:
            await state.clear()
    except ValueError:
        await message.answer("Пожалуйста, введите время (число).")

def is_valid_date(date: str) -> bool:
    try:
        appointment_date = datetime.strptime(date, '%Y-%m-%d')
        if appointment_date.weekday() not in WORKING_DAYS:
            return False
        return True
    except ValueError:
        return False