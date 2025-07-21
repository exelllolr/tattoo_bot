from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from bot.utils.database import get_db
from bot.services.master_service import get_masters
from config.constants import LOCALE

router = Router()

class MessageState(StatesGroup):
    master_id = State()
    text = State()

@router.message(lambda message: message.text == "Написать в поддержку")
async def start_support_message(message: Message, state: FSMContext):
    masters = await get_masters()
    response = "Выберите мастера для отправки сообщения (введите ID):\n"
    for master in masters:
        response += f"{master['id']}. {master['name']}\n"
    await message.answer(response)
    await state.set_state(MessageState.master_id)

@router.message(MessageState.master_id)
async def process_master_id(message: Message, state: FSMContext):
    try:
        master_id = int(message.text)
        masters = await get_masters()
        if not any(master['id'] == master_id for master in masters):
            await message.answer("Неверный ID мастера. Попробуйте снова.")
            return
        await state.update_data(master_id=master_id)
        await message.answer(LOCALE["ru"]["support_prompt"])
        await state.set_state(MessageState.text)
    except ValueError:
        await message.answer("Пожалуйста, введите число (ID мастера).")

@router.message(MessageState.text)
async def handle_message(message: Message, state: FSMContext):
    data = await state.get_data()
    async with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO messages (user_id, master_id, text)
            VALUES (?, ?, ?)
        ''', (message.from_user.id, data['master_id'], message.text))
        conn.commit()
    
    await message.answer(LOCALE["ru"]["message_sent"])
    await state.clear()