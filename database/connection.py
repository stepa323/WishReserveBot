import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base

class DatabaseConnection:
    """SQLite connection handler with async support"""
    
    def __init__(self, db_path: str = "sqlite+aiosqlite:///app.db"):
        self.db_url = db_path
        self.engine = None
        self.SessionLocal = None

    def connect(self):
        """Initialize SQLite connection"""
        self.engine = create_async_engine(
            self.db_url,
            connect_args={"check_same_thread": False},  # SQLite-specific
            echo=True  # Set to False in production
        )
        self.SessionLocal = sessionmaker(
            self.engine,
            class_=AsyncSession,
            expire_on_commit=False
        )

    async def create_tables(self):
        """Create all tables"""
        from .models import Base
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    async def get_session(self):
        """Database session generator"""
        session = self.SessionLocal()
        try:
            yield session
        finally:
            await session.close()
