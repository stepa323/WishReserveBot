from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import CallbackQuery

from keyboards.keyboard_utils import create_inline_kb
from states.states import FSMNewWishList

router = Router()


@router.callback_query(F.data == 'cancel_wishlist_creation', ~StateFilter(default_state))
async def process_cancel_command(callback: CallbackQuery, i18n: dict[str, str], state: FSMContext):
    keyboard = create_inline_kb(1, i18n, )
    await callback.message.edit_text(
        text=i18n.get('confirm_cancel'),
        reply_markup=keyboard
    )
    await state.clear()


@router.callback_query(F.data == 'btn_create_wishlist', StateFilter(default_state))
async def process_btn_create_wishlist(callback: CallbackQuery, i18n: dict[str, str], state: FSMContext):
    keyboard = create_inline_kb(1, i18n, cancel_wishlist_creation='cancel_wishlist_creation')
    await callback.message.edit_text(
        text=i18n.get('create_wishlist_title'),
        reply_markup=keyboard
    )
    await state.set_state(FSMNewWishList.fill_title_list)


@router.callback_query(StateFilter(FSMNewWishList.fill_title_list))
async def process_title_sent(callback: CallbackQuery, i18n: dict[str, str], state: FSMContext):
    keyboard = create_inline_kb(1, i18n, cancel_wishlist_creation='cancel_wishlist_creation')
    await callback.message.edit_text(
        text=i18n.get('create_wishlist_description'),
        reply_markup=keyboard
    )
    await state.set_state(FSMNewWishList.fill_description_list)


@router.callback_query(StateFilter(FSMNewWishList.fill_title_list))
async def process_title_sent(callback: CallbackQuery, i18n: dict[str, str], state: FSMContext):
    keyboard = create_inline_kb(1, i18n, cancel_wishlist_creation='cancel_wishlist_creation')
    await callback.message.edit_text(
        text=i18n.get('create_wishlist_description'),
        reply_markup=keyboard
    )
    await state.set_state(FSMNewWishList.fill_description_list)


@router.callback_query(StateFilter(FSMNewWishList.fill_title_list))
async def process_title_sent(callback: CallbackQuery, i18n: dict[str, str], state: FSMContext):
    keyboard = create_inline_kb(1, i18n, cancel_wishlist_creation='cancel_wishlist_creation')
    await callback.message.edit_text(
        text=i18n.get('create_wishlist_date'),
        reply_markup=keyboard
    )
    await state.set_state(FSMNewWishList.fill_date)
