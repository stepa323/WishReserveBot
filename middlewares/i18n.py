from typing import Callable, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, User


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

        user_lang = user.language_code
        translations = data.get("translations")

        i18n = translations.get(user_lang)
        data["i18n"] = i18n if i18n else translations[translations['default']]

        return await handler(event, data)
