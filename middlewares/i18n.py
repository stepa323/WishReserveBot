from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, User
from typing import Any, Awaitable, Callable

from database.requests import get_user_language
from handlers.handlers_utils import get_i18n


class TranslatorMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any]
    ) -> Any:

        user: User = data.get("event_from_user")
        if user is None:
            return await handler(event, data)

        # язык из базы
        user_lang = await get_user_language(user.id)

        translations = data.get("translations", {})
        data["i18n"] = get_i18n(translations, user_lang)

        return await handler(event, data)
