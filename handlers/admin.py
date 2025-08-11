import logging

from aiogram import Router, F, Bot
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from database.requests import get_stats, get_all_users_id
from filters.is_admin import IsAdmin
from keyboards.keyboard_utils import create_inline_kb
from states.states import AdminState

admin_router = Router()

logger = logging.getLogger(__name__)


@admin_router.message(IsAdmin, Command('admin'))
async def admin_panel(message: Message, i18n: dict[str, str]):
    keyboard = create_inline_kb(1, i18n,
                                admin_newsletter='admin_newsletter_btn',
                                admin_statistic='admin_statistic_btn')

    await message.answer(i18n.get('admin_welcome'),
                         reply_markup=keyboard)


@admin_router.callback_query(IsAdmin, F.data == 'admin')
async def admin_panel(callback: CallbackQuery, i18n: dict[str, str], state: FSMContext):
    await state.clear()
    await callback.answer()
    keyboard = create_inline_kb(1, i18n,
                                admin_newsletter='admin_newsletter_btn',
                                admin_statistic='admin_statistic_btn')

    await callback.message.edit_text(i18n.get('admin_welcome'),
                                     reply_markup=keyboard)


@admin_router.callback_query(IsAdmin, F.data == 'admin_statistic')
async def admin_statistic(callback: CallbackQuery, i18n: dict[str, str]):
    keyboard = create_inline_kb(1, i18n, admin='btn_go_back')
    await callback.answer()

    users_count, wishlists_count, gifts_count = await get_stats()

    stats_text = i18n.get('admin_statistics_text').format(
        users_count=users_count,
        wishlists_count=wishlists_count,
        gifts_count=gifts_count
    )

    await callback.message.edit_text(
        text=stats_text,
        reply_markup=keyboard
    )


@admin_router.callback_query(IsAdmin, F.data == 'admin_newsletter')
async def admin_newsletter(callback: CallbackQuery, i18n: dict[str, str], state: FSMContext):
    keyboard = create_inline_kb(1, i18n, admin='btn_go_back')

    await callback.answer()

    await callback.message.edit_text(
        text=i18n.get('admin_newsletter_start'),
        reply_markup=keyboard
    )
    await state.set_state(AdminState.waiting_newsletter_message)


@admin_router.message(AdminState.waiting_newsletter_message)
async def confirm_newsletter(message: Message, state: FSMContext, i18n: dict[str, str]):
    await state.update_data(newsletter_message=message)
    keyboard = create_inline_kb(2, i18n, confirm_newsletter='confirm_yes', cancel_newsletter='confirm_no')

    await message.answer(
        text=i18n.get('admin_newsletter_confirm'),
        reply_markup=keyboard
    )


@admin_router.callback_query(IsAdmin, F.data == 'confirm_newsletter')
async def process_confirm_newsletter(callback: CallbackQuery, state: FSMContext, bot: Bot, i18n: dict[str, str]):
    await callback.answer()

    logger.info('Newsletter confirmed')
    data = await state.get_data()
    newsletter_message = data.get('newsletter_message')

    if not newsletter_message:
        await callback.answer(i18n.get('error_no_message'))
        return

    await callback.message.edit_text(i18n.get('admin_newsletter_started'))

    all_ids = await get_all_users_id()
    total_users = len(all_ids)
    success = 0
    failed = 0

    logger.info('Newsletter started')

    for user_id in all_ids:
        try:
            await newsletter_message.send_copy(chat_id=user_id)
            success += 1
        except Exception as e:
            logger.error(f"Failed to send to {user_id}: {e}")
            failed += 1

    stats_text = i18n['admin_newsletter_stats'].format(
        total=total_users,
        success=success,
        failed=failed
    )

    await callback.message.edit_text(stats_text, reply_markup=create_inline_kb(1, i18n, admin='btn_go_back'))
    await state.clear()


@admin_router.callback_query(IsAdmin, F.data == 'cancel_newsletter')
async def process_cancel_newsletter(callback: CallbackQuery, state: FSMContext, i18n: dict[str, str]):
    await callback.message.edit_text(i18n['admin_newsletter_canceled'])
    await state.clear()
