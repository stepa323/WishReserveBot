import logging
from datetime import datetime
from typing import Optional

from aiogram import Router, F
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from aiogram.utils.keyboard import InlineKeyboardBuilder

from database.requests import get_wishlist, get_or_create_user, create_or_update_wishlist
from handlers.handlers_utils import delete_item_message
from keyboards.keyboard_utils import wishlist_kb
from states.states import FSMNewWishList

router = Router()

logger = logging.getLogger(__name__)


async def render_wishlist_edit_template(
        wishlist_data: dict,
        i18n: dict
) -> str:
    # Данные из состояния
    title = wishlist_data.get('title', i18n['no_data'])
    description = wishlist_data.get('description', i18n['no_data'])
    event_date = wishlist_data.get('event_date', i18n['no_data'])
    is_private = wishlist_data.get('is_private', False)
    is_editing = wishlist_data.get('is_editing', False)

    privacy_value = i18n['privacy_private'] if is_private else i18n['privacy_public']

    state_mode = i18n['editing'] if is_editing else i18n['creating']
    edit_mode = i18n['edit_wishlist_text'].format(state=state_mode)

    return i18n['wishlist_edit_template'].format(
        title=title,
        privacy_value=privacy_value,
        description=description,
        event_date=event_date,
        edit_mode=edit_mode
    )


async def update_wishlist_message(
        last_bot_message: Message | None,
        i18n: dict,
        state: FSMContext,
        new_message_target: Message | CallbackQuery | None = None,
) -> Message:
    data = await state.get_data()

    text = await render_wishlist_edit_template(data, i18n)

    kb = wishlist_kb(
        i18n,
        is_private=data.get('is_private'),
    )

    if last_bot_message:
        try:
            await last_bot_message.edit_text(
                text=text,
                reply_markup=kb
            )
            return last_bot_message
        except TelegramBadRequest:
            pass

    if isinstance(new_message_target, CallbackQuery):
        msg = await new_message_target.message.answer(
            text=text,
            reply_markup=kb
        )
    else:
        msg = await new_message_target.answer(
            text=text,
            reply_markup=kb
        )
    return msg


def validate_date(date_str: str) -> Optional[str]:
    try:
        datetime.strptime(date_str, "%d.%m.%Y")
        return None
    except ValueError:
        return "invalid_date_format"


@router.callback_query((F.data == 'btn_create_wishlist') | (F.data.startswith('edit_wishlist')))
async def start_wishlist_creation(callback: CallbackQuery, i18n: dict, state: FSMContext):
    await callback.answer()
    await delete_item_message(state)

    if callback.data.startswith('edit_wishlist_'):
        try:
            wishlist_id = int(callback.data.split('_')[-1])
            wishlist = await get_wishlist(wishlist_id)
            user = await get_or_create_user(callback.from_user.id)

            if not wishlist or wishlist.owner_id != user.id:
                await callback.answer(i18n['access_denied'], show_alert=True)
                return

            await state.update_data(
                title=wishlist.title,
                is_private=wishlist.is_private,
                description=wishlist.description,
                event_date=wishlist.event_date.strftime("%d.%m.%Y") if wishlist.event_date else None,
                wishlist_id=wishlist.id,
                access_uuid=wishlist.access_uuid,
                is_editing=True
            )
            await state.set_state(FSMNewWishList.wishlist_info)

            text = await render_wishlist_edit_template({
                'title': wishlist.title,
                'is_private': wishlist.is_private,
                'description': wishlist.description,
                'event_date': wishlist.event_date.strftime("%d.%m.%Y") if wishlist.event_date else None,
                'access_uuid': wishlist.access_uuid,
                'is_editing': True
            }, i18n)

            last_msg = await callback.message.edit_text(
                text=text,
                reply_markup=wishlist_kb(
                    i18n,
                    is_private=wishlist.is_private
                ),
                parse_mode="HTML"
            )
            await state.update_data(last_bot_message=last_msg)
            return
        except Exception as e:
            logger.error(f"Error loading wishlist: {e}")
            await callback.answer(i18n['error_occurred'], show_alert=True)
            return

    await state.set_state(FSMNewWishList.wishlist_info)
    text = await render_wishlist_edit_template({
        'title': i18n['no_data'],
        'is_private': False,
        'description': i18n['no_data'],
        'event_date': i18n['no_data'],
        'access_uuid': ''
    }, i18n)

    last_msg = await callback.message.edit_text(
        text=text,
        reply_markup=wishlist_kb(i18n),
        parse_mode="HTML"
    )
    await state.update_data(last_bot_message=last_msg)


@router.callback_query(F.data == 'cancel', StateFilter(FSMNewWishList))
async def cancel_creation(callback: CallbackQuery, i18n: dict, state: FSMContext):
    await callback.answer()
    state_data = await state.get_data()
    wishlist_id = state_data.get('wishlist_id')
    if wishlist_id:
        wishlist = await get_wishlist(wishlist_id)
        keyboard = InlineKeyboardBuilder().button(text=i18n['back_to_wishlist'],
                                                  callback_data=f"view_wishlist_{wishlist.access_uuid}").as_markup()
    else:
        keyboard = InlineKeyboardBuilder().button(text=i18n['btn_my_wishlists'],
                                                  callback_data='btn_my_wishlists').as_markup()
    await state.clear()
    await callback.message.edit_text(i18n['creation_canceled'], reply_markup=keyboard)


@router.callback_query(F.data == 'toggle_privacy', StateFilter(FSMNewWishList.wishlist_info))
async def toggle_privacy(callback: CallbackQuery, i18n: dict, state: FSMContext):
    await callback.answer()
    data = await state.get_data()
    new_privacy = not data.get('is_private', False)
    await state.update_data(is_private=new_privacy)
    await update_wishlist_message(callback.message, i18n, state)


@router.callback_query(F.data.startswith('edit_'), StateFilter(FSMNewWishList.wishlist_info))
async def start_editing_field(callback: CallbackQuery, i18n: dict, state: FSMContext):
    await callback.answer()
    field = callback.data.split('_')[1]

    if field == 'title':
        await state.set_state(FSMNewWishList.editing_title)
        await callback.message.edit_text(i18n['enter_title_prompt'])
    elif field == 'description':
        await state.set_state(FSMNewWishList.editing_description)
        await callback.message.edit_text(i18n['enter_description_prompt'])
    elif field == 'date':
        await state.set_state(FSMNewWishList.editing_date)
        await callback.message.edit_text(i18n['enter_date_prompt'])


@router.message(StateFilter(FSMNewWishList.editing_title))
async def process_title(message: Message, i18n: dict, state: FSMContext):
    if len(message.text) > 50:
        await message.reply(i18n['title_too_long'])
        return

    data = await state.get_data()
    last_bot_message = data.get('last_bot_message')  # get last bot message

    await state.update_data(title=message.text)
    await state.set_state(FSMNewWishList.wishlist_info)

    # delete user message
    try:
        await message.delete()
    except TelegramBadRequest:
        pass

    new_msg = await update_wishlist_message(last_bot_message, i18n, state, message)
    await state.update_data(last_bot_message=new_msg)


@router.message(StateFilter(FSMNewWishList.editing_description))
async def process_description(message: Message, i18n: dict, state: FSMContext):
    if len(message.text) > 300:
        await message.reply(i18n['description_too_long'])
        return

    data = await state.get_data()
    last_bot_message = data.get('last_bot_message')

    await state.update_data(description=message.text)
    await state.set_state(FSMNewWishList.wishlist_info)

    try:
        await message.delete()
    except TelegramBadRequest:
        pass

    new_msg = await update_wishlist_message(last_bot_message, i18n, state)
    await state.update_data(last_bot_message=new_msg)


@router.message(StateFilter(FSMNewWishList.editing_date))
async def process_date(message: Message, i18n: dict, state: FSMContext):
    error = validate_date(message.text)
    if error:
        await message.reply(i18n[error])
        return

    data = await state.get_data()
    last_bot_message = data.get('last_bot_message')

    await state.update_data(event_date=message.text)
    await state.set_state(FSMNewWishList.wishlist_info)

    try:
        await message.delete()
    except TelegramBadRequest:
        pass

    new_msg = await update_wishlist_message(last_bot_message, i18n, state)
    await state.update_data(last_bot_message=new_msg)


@router.callback_query(F.data == 'confirm', StateFilter(FSMNewWishList.wishlist_info))
async def confirm_wishlist(callback: CallbackQuery, i18n: dict, state: FSMContext):
    await callback.answer()
    data = await state.get_data()
    try:
        event_date = datetime.strptime(data['event_date'], "%d.%m.%Y") if data.get('event_date') else None
        wishlist = await create_or_update_wishlist(
            user_id=callback.from_user.id,
            username=callback.from_user.username,
            title=data['title'],
            is_private=data['is_private'],
            description=data.get('description'),
            event_date=event_date,
            wishlist_id=data.get('wishlist_id')
        )
        await callback.message.edit_text(
            text=i18n['wishlist_created'].format(title=wishlist.title),
            reply_markup=InlineKeyboardBuilder()
            .button(text=i18n['view_wishlist'], callback_data=f"view_wishlist_{wishlist.access_uuid}")
            .as_markup()
        )
        await state.clear()
    except Exception as e:
        logger.error(f"Error saving wishlist: {e}")
        await callback.answer(i18n['save_error'], show_alert=True)
