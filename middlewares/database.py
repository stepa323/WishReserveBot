from typing import Callable, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from database.connection import DatabaseConnection
from database.db import Database
from sqlalchemy.ext.asyncio import AsyncSession

class DatabaseMiddleware(BaseMiddleware):
    """Middleware that injects database session into handlers"""
    def __init__(self, db_conn: DatabaseConnection):
        super().__init__()
        self.db_conn = db_conn

    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any]
    ) -> Any:
        async with self.db_conn.get_session() as session:
            data['db'] = Database(session)
            return await handler(event, data)
