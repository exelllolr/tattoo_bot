import sqlite3
import asyncio
from contextlib import asynccontextmanager
from datetime import datetime

async def init_db():
    conn = sqlite3.connect('tattoo_booking.db')
    cursor = conn.cursor()
    
    # Create masters table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS masters (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            experience INTEGER NOT NULL,
            description TEXT,
            avatar_url TEXT,
            portfolio_urls TEXT
        )
    ''')
    
    # Create appointments table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS appointments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            master_id INTEGER NOT NULL,
            date TEXT NOT NULL,
            time INTEGER NOT NULL,
            status TEXT NOT NULL,
            FOREIGN KEY (master_id) REFERENCES masters(id)
        )
    ''')
    
    # Create messages table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            master_id INTEGER NOT NULL,
            text TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (master_id) REFERENCES masters(id)
        )
    ''')
    
    # Insert test data
    cursor.execute('''
        INSERT OR IGNORE INTO masters (name, experience, description, avatar_url, portfolio_urls) VALUES
        ('Алексей "Скорпион"', 7, 'Специализируюсь на реализме и черно-серых татуировках. Хочу попробовать крупные цветные проекты в стиле акварели.', 'https://example.com/avatar1.jpg', '["https://example.com/portfolio1.jpg","https://example.com/portfolio2.jpg","https://example.com/portfolio3.jpg"]'),
        ('Екатерина "Луна"', 5, 'Работаю в стилях графика и олдскул. Экспериментирую с нео-традишнл.', 'https://example.com/avatar2.jpg', '["https://example.com/portfolio4.jpg","https://example.com/portfolio5.jpg"]')
    ''')
    
    conn.commit()
    conn.close()

@asynccontextmanager
async def get_db():
    conn = sqlite3.connect('tattoo_booking.db')
    try:
        yield conn
    finally:
        conn.close()