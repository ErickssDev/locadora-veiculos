from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings


# Configurações específicas para SQLite
engine_kwargs = {
    "future": True,
    "echo": False,
}

# SQLite precisa de configuração especial para asyncio
if "sqlite" in settings.database_url:
    engine_kwargs["connect_args"] = {"check_same_thread": False}

engine: AsyncEngine = create_async_engine(
    settings.database_url,
    **engine_kwargs
)

AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)
