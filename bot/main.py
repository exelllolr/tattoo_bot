import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from config.settings import BOT_TOKEN
from bot.handlers import start, masters, appointments, messages, admin
from bot.utils.database import init_db
from bot.services.notification_service import schedule_notifications

# Configure logging
logging.basicConfig(level=logging.INFO)
logging.basicConfig(level=logging.DEBUG)

async def main():
    # Initialize bot and dispatcher
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher(storage=MemoryStorage())
    
    # Register handlers
    dp.include_routers(
        start.router,
        masters.router,
        appointments.router,
        messages.router,
        admin.router
    )
    
    # Initialize database
    await init_db()
    
    # Start notification scheduler
    asyncio.create_task(schedule_notifications(bot))
    
    # Start polling
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())