from typing import Callable, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from database.connection import DatabaseConnection
from database.db import Database
from sqlalchemy.ext.asyncio import AsyncSession

class DatabaseMiddleware(BaseMiddleware):
    async def __call__(self, handler, event, data):
        async with self.db_conn.SessionLocal() as session:
            data['db_session'] = session
            return await handler(event, data)
