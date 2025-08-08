from aiogram import Router, F
from aiogram.filters import CommandStart, Command, StateFilter
from aiogram.fsm.state import default_state
from aiogram.types import Message, CallbackQuery

from keyboards.keyboard_utils import create_inline_kb

router = Router()


@router.message(CommandStart(), StateFilter(default_state))
async def process_start_message(message: Message, i18n: dict[str, str]):
    keyboard = create_inline_kb(2, i18n, 'btn_my_wishlists', 'btn_friends_wishlists', 'btn_help')
    await message.answer(
        text=i18n.get('/start'),
        reply_markup=keyboard
    )


@router.callback_query(F.data == 'start_menu', StateFilter(default_state))
async def process_start_message(callback: CallbackQuery, i18n: dict[str, str]):
    keyboard = create_inline_kb(2, i18n, 'btn_my_wishlists', 'btn_friends_wishlists', 'btn_help')
    await callback.message.edit_text(
        text=i18n.get('/start'),
        reply_markup=keyboard
    )


@router.callback_query(F.data == 'btn_my_wishlists', StateFilter(default_state))
async def process_btn_my_wishlist_click(callback: CallbackQuery, i18n: dict[str, str]):
    # Получаем списки желаний из базы данных
    wishlists = False

    keyboard = create_inline_kb(1, i18n, 'btn_create_wishlist', start_menu='btn_go_back')
    if not wishlists:
        await callback.message.edit_text(
            text=i18n.get('my_wishlists_if_none'),
            reply_markup=keyboard
        )
    else:
        await callback.message.edit_text(
            text=i18n.get('my_wishlists'),
            reply_markup=keyboard
        )


@router.callback_query(F.data == 'btn_friends_wishlists', StateFilter(default_state))
async def process_btn_friends_wishlists(callback: CallbackQuery, i18n: dict[str, str]):
    # Получаем списки желаний друзей из базы данных
    wishlists = False

    keyboard = create_inline_kb(1, i18n, 'btn_create_wishlist', start_menu='btn_go_back')
    if not wishlists:
        await callback.message.edit_text(
            text=i18n.get('friends_wishlists_if_none'),
            reply_markup=keyboard
        )
    else:
        await callback.message.edit_text(
            text=i18n.get('friends_wishlists'),
            reply_markup=keyboard
        )


@router.callback_query(F.data == 'btn_help', StateFilter(default_state))
async def process_btn_help(callback: CallbackQuery, i18n: dict[str, str]):
    keyboard = create_inline_kb(1, i18n, 'btn_support', start_menu='btn_go_back')
    await callback.message.edit_text(
        text=i18n.get('/help'),
        reply_markup=keyboard
    )


@router.message(Command(commands='/help'), StateFilter(default_state))
async def process_btn_help(message: Message, i18n: dict[str, str]):
    keyboard = create_inline_kb(1, i18n, 'btn_support')
    await message.answer(
        text=i18n.get('/help'),
        reply_markup=keyboard
    )
