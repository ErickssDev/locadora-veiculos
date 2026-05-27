
import asyncio
import os
import sys
from pathlib import Path

from sqlalchemy.ext.asyncio import create_async_engine

# ensure backend folder is on sys.path so `app` package can be imported
HERE = Path(__file__).resolve().parent
BACKEND_ROOT = str(HERE.parent)
if BACKEND_ROOT not in sys.path:
    sys.path.insert(0, BACKEND_ROOT)

from app.db.base import Base

# ensure models are imported so they're registered on Base.metadata
from app import models  # noqa: F401

DB_URL = os.getenv('DATABASE_URL', 'sqlite+aiosqlite:///./test.db')

async def main():
    print('Using DB URL:', DB_URL)
    engine = create_async_engine(DB_URL, echo=False, connect_args={"check_same_thread": False})

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    await engine.dispose()
    print('Tables created')

if __name__ == '__main__':
    asyncio.run(main())
