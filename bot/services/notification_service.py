import asyncio
from datetime import datetime, timedelta
from aiogram import Bot
from bot.utils.database import get_db
from config.settings import NOTIFICATION_INTERVAL

async def schedule_notifications(bot: Bot):
    while True:
        async with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT a.id, a.user_id, m.name, a.date, a.time
                FROM appointments a
                JOIN masters m ON a.master_id = m.id
                WHERE a.status = 'confirmed'
            ''')
            appointments = cursor.fetchall()
        
        now = datetime.now()
        for appointment in appointments:
            app_id, user_id, master_name, date, time = appointment
            appointment_time = datetime.strptime(f"{date} {time}:00", '%Y-%m-%d %H:%M')
            if now <= appointment_time <= now + timedelta(hours=24):
                await bot.send_message(
                    user_id,
                    f"Напоминание: Ваша запись к мастеру {master_name} завтра в {time}:00!"
                )
        
        await asyncio.sleep(NOTIFICATION_INTERVAL)