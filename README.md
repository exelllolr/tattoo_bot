Tattoo Booking Bot
Telegram-бот для записи на тату-сессии в салоне.
Установка

Установите зависимости:

pip install -r requirements.txt


Настройте переменные окружения в config/settings.py:


BOT_TOKEN: Токен вашего Telegram-бота
WEBAPP_URL: URL вашего Mini App
DB_NAME: Имя файла базы данных SQLite


Инициализируйте базу данных:

python -m bot.utils.database


Запустите бота и API:

uvicorn bot.api:app --host 0.0.0.0 --port 8000
python -m bot.main

Структура проекта

bot/: Логика бота
handlers/: Обработчики команд и сообщений
models/: Модели данных
services/: Бизнес-логика
utils/: Утилиты


webapp/: Frontend для Telegram Mini App
config/: Конфигурация
migrations/: Миграции БД

Требования

Python 3.8+
aiogram
fastapi
uvicorn
pytest
SQLite

Деплой

Разверните на Heroku/AWS/VPS
Настройте веб-сервер для Mini App (например, nginx)
Обеспечьте доступ к Telegram CDN для изображений
Настройте FastAPI для обработки запросов Mini App

Тестирование
Запустите тесты:
pytest

Пример данных
База данных инициализируется с двумя мастерами:

Алексей "Скорпион" (7 лет опыта, реализм)
Екатерина "Луна" (5 лет опыта, графика и олдскул)
