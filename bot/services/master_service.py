import json
import sqlite3
from bot.utils.database import get_db

async def get_masters():
    async with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT id, name, experience, description, avatar_url, portfolio_urls FROM masters')
        rows = cursor.fetchall()
        return [
            {
                'id': row[0],
                'name': row[1],
                'experience': row[2],
                'description': row[3],
                'avatar_url': row[4],
                'portfolio_urls': json.loads(row[5])
            } for row in rows
        ]