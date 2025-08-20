import asyncio
import logging

from aiogram import BaseMiddleware
from aiogram.dispatcher.event.bases import UNHANDLED

logger = logging.getLogger("update_logger")


class LoggerMiddleware(BaseMiddleware):
    async def __call__(self, handler, update, data):
        loop = asyncio.get_running_loop()
        start_time = loop.time()
        handled = False
        try:
            result = await handler(update, data)
            handled = result is not UNHANDLED
            return result
        finally:
            duration = (loop.time() - start_time) * 1000

            username = None
            user_id = None
            chat_id = None
            extra_info = ""

            # Сообщение
            if update.message:
                msg = update.message
                user_id = msg.from_user.id if msg.from_user else None
                username = msg.from_user.username if msg.from_user else None
                chat_id = msg.chat.id if msg.chat else None

                if msg.text:
                    extra_info = f"message_text={msg.text!r}"
                elif msg.caption:
                    extra_info = f"message_caption={msg.caption!r}"
                else:
                    extra_info = f"message_content_type={msg.content_type}"
            elif update.callback_query:
                cb = update.callback_query
                user_id = cb.from_user.id if cb.from_user else None
                username = cb.from_user.username if cb.from_user else None
                chat_id = cb.message.chat.id if cb.message and cb.message.chat else None
                extra_info = f"callback_data={cb.data!r}"

            logger.info(
                "Update id=%s is %s. Duration %.2f ms by bot id=%s, user_id=%s, username=%s, chat_id=%s, %s",
                update.update_id,
                "handled" if handled else "not handled",
                duration,
                data["bot"].id,
                user_id,
                username,
                chat_id,
                extra_info,
            )
