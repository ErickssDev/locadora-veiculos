import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text
import os

DB_URL = os.getenv('DATABASE_URL', 'sqlite+aiosqlite:///./test.db')

async def main():
    print('Using DB URL:', DB_URL)
    engine = create_async_engine(DB_URL, echo=False)
    async with engine.connect() as conn:
        result = await conn.execute(text("SELECT name FROM sqlite_master WHERE type='table';"))
        rows = result.fetchall()
        print('Tables:', rows)

if __name__ == '__main__':
    asyncio.run(main())
