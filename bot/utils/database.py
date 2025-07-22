import psycopg2
import asyncio
from contextlib import asynccontextmanager
import os

async def init_db():
    conn = psycopg2.connect(os.environ.get("DATABASE_URL"))
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS masters (
            id SERIAL PRIMARY KEY,
            name TEXT NOT NULL,
            experience INTEGER NOT NULL,
            description TEXT,
            avatar_url TEXT,
            portfolio_urls TEXT
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS appointments (
            id SERIAL PRIMARY KEY,
            user_id INTEGER NOT NULL,
            master_id INTEGER NOT NULL,
            date TEXT NOT NULL,
            time INTEGER NOT NULL,
            status TEXT NOT NULL,
            FOREIGN KEY (master_id) REFERENCES masters(id)
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id SERIAL PRIMARY KEY,
            user_id INTEGER NOT NULL,
            master_id INTEGER NOT NULL,
            text TEXT NOT NULL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (master_id) REFERENCES masters(id)
        )
    ''')
    
    cursor.execute('''
        INSERT INTO masters (name, experience, description, avatar_url, portfolio_urls)
        VALUES
        ('Алексей "Скорпион"', 7, 'Специализируюсь на реализме и черно-серых татуировках. Хочу попробовать крупные цветные проекты в стиле акварели.', 'https://example.com/avatar1.jpg', '["https://example.com/portfolio1.jpg","https://example.com/portfolio2.jpg","https://example.com/portfolio3.jpg"]'),
        ('Екатерина "Луна"', 5, 'Работаю в стилях графика и олдскул. Экспериментирую с нео-традишнл.', 'https://example.com/avatar2.jpg', '["https://example.com/portfolio4.jpg","https://example.com/portfolio5.jpg"]')
        ON CONFLICT DO NOTHING
    ''')
    
    conn.commit()
    conn.close()

@asynccontextmanager
async def get_db():
    conn = psycopg2.connect(os.environ.get("DATABASE_URL"))
    try:
        yield conn
    finally:
        conn.close()