import logging
from datetime import datetime

from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import CallbackQuery, Message

from handlers.handlers_utils import validate_date_input
from keyboards.keyboard_utils import create_inline_kb
from states.states import FSMNewWishList

from database.requests import create_or_update_wishlist

router = Router()

logger = logging.getLogger(__name__)


@router.callback_query(F.data == 'btn_my_wishlists', ~StateFilter(default_state))
async def process_cancel_command(callback: CallbackQuery, i18n: dict[str, str], state: FSMContext):
    await callback.answer()

    await callback.message.answer(text=i18n.get('canceled_wishlist_creation'))

    await state.clear()


@router.callback_query(F.data == 'btn_create_wishlist', StateFilter(default_state))
async def process_btn_create_wishlist(callback: CallbackQuery, i18n: dict[str, str], state: FSMContext):
    keyboard = create_inline_kb(1, i18n, btn_my_wishlists='cancel_wishlist_creation')

    await callback.answer()

    await callback.message.answer(
        text=i18n.get('create_wishlist_title'),
        reply_markup=keyboard
    )
    await state.set_state(FSMNewWishList.fill_title_list)


@router.message(StateFilter(FSMNewWishList.fill_title_list))
async def process_title_sent(message: Message, i18n: dict[str, str], state: FSMContext):
    title = message.text.strip()

    # validating input
    if not (4 <= len(title) <= 50):
        await message.answer(text=i18n.get('invalid_title_length'))
    else:
        keyboard = create_inline_kb(2, i18n, 'private', 'public', btn_my_wishlists='cancel_wishlist_creation')
        await message.answer(text=i18n.get('choose_privacy'), reply_markup=keyboard)
        await state.update_data(title=title)
        await state.set_state(FSMNewWishList.choose_privacy)


@router.callback_query(StateFilter(FSMNewWishList.choose_privacy), F.data.in_(['private', 'public']))
async def process_privacy_chosen(callback: CallbackQuery, i18n: dict[str, str], state: FSMContext):
    keyboard = create_inline_kb(1, i18n, btn_my_wishlists='cancel_wishlist_creation')
    is_private = callback.data == 'private'
    await callback.answer()
    await callback.message.answer(text=i18n.get('create_wishlist_description'), reply_markup=keyboard)
    await state.update_data(is_private=is_private)
    await state.set_state(FSMNewWishList.fill_description_list)


@router.message(StateFilter(FSMNewWishList.fill_description_list))
async def process_description_sent(message: Message, i18n: dict[str, str], state: FSMContext):
    keyboard = create_inline_kb(1, i18n, btn_my_wishlists='cancel_wishlist_creation')
    description = message.text.strip()

    # validating input
    if len(description) > 300:
        await message.answer(text=i18n.get('invalid_description_length'))
    else:
        if description == '/skip':
            description = ''
        await message.answer(text=i18n.get('create_wishlist_date'), reply_markup=keyboard)
        await state.update_data(description=description)
        await state.set_state(FSMNewWishList.fill_date)


@router.message(StateFilter(FSMNewWishList.fill_date))
async def process_date_sent(message: Message, i18n: dict[str, str], state: FSMContext):
    date_str = message.text.strip()

    is_not_valid = await validate_date_input(date_str)
    if is_not_valid:
        await message.answer(text=i18n.get(is_not_valid))
    try:
        user_id = message.from_user.id

        event_date = None
        if date_str and date_str != '/skip':
            event_date = datetime.strptime(date_str, "%d.%m.%Y")
        else:
            date_str = ''
        state_data = await state.get_data()

        wishlist = await create_or_update_wishlist(
            user_id=user_id,
            title=state_data.get('title', ''),
            is_private=state_data.get('is_private'),
            description=state_data.get('description', ''),
            event_date=event_date
        )

        success_message = i18n.get('wishlist_created').format(
            title=wishlist.title,
            description=wishlist.description or i18n.get('not_specified'),
            date=date_str if date_str else i18n.get('not_specified'),
            visibility=i18n.get('visibility_private') if wishlist.is_private else i18n.get('visibility_public'))

        keyboard = create_inline_kb(1, i18n, **{f'view_wishlist_{wishlist.access_uuid}': f'🎁 {wishlist.title}'},
                                    start_menu='start_menu')
        await message.answer(text=success_message, reply_markup=keyboard)

        await state.clear()
    except Exception as e:
        logger.error(f"Error creating wishlist: {e}")
