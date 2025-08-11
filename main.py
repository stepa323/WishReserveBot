import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from config.config import Config, load_config
from handlers import user, wishlists_forms
from handlers.admin import admin_router
from lexicon.lexicon_en import LEXICON_EN
from lexicon.lexicon_ru import LEXICON_RU

from middlewares.i18n import TranslatorMiddleware

from database.models import async_main

logger = logging.getLogger(__name__)

translations = {
    'default': 'en',
    'en': LEXICON_EN,
    'ru': LEXICON_RU
}

async def main():
    logging.basicConfig(
        level=logging.INFO,
        format='%(filename)s:%(lineno)d #%(levelname)-8s '
               '[%(asctime)s] - %(name)s - %(message)s'
    )
    logger.info('Starting bot')

    config: Config = load_config()
    
    storage = MemoryStorage()

    bot = Bot(
        token=config.bot.token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    dp = Dispatcher(storage=storage)

    logger.info('Connecting routers')

    dp.include_router(user.router)
    dp.include_router(wishlists_forms.router)
    dp.include_router(admin_router)

    logger.info('Connecting middleware')

    dp.update.middleware(TranslatorMiddleware())

    logger.info('Init database')

    dp.startup.register(startup)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, translations=translations)

async def startup(dispatcher: Dispatcher):
    await async_main()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info('Bot stopped')
