import logging
from datetime import datetime

from aiogram import Router, F, Bot
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import CallbackQuery, Message
from aiogram.utils.chat_action import ChatActionSender

from handlers.handlers_utils import process_invalid_input, edit_last_msg, validate_date_input
from keyboards.keyboard_utils import create_inline_kb
from states.states import FSMNewWishList

from database.requests import create_or_update_wishlist

router = Router()

logger = logging.getLogger(__name__)


#* Exit from states machine
#@router.callback_query(F.data == 'btn_my_wishlists', ~StateFilter(default_state))
#async def process_cancel_command(callback: CallbackQuery, i18n: dict[str, str], state: FSMContext):
    #await callback.answer(text=i18n.get('canceled_wishlist_creation'), show_alert=True)

  #  await state.clear()


# 0 step of creating wishlist
@router.callback_query(F.data == 'btn_create_wishlist', StateFilter(default_state))
async def process_btn_create_wishlist(callback: CallbackQuery, i18n: dict[str, str], state: FSMContext):
    keyboard = create_inline_kb(1, i18n, btn_my_wishlists='cancel_wishlist_creation')

    await callback.answer()

    await callback.message.edit_text(
        text=i18n.get('create_wishlist_title'),
        reply_markup=keyboard
    )
    await state.set_state(FSMNewWishList.fill_title_list)
    await state.update_data(last_message_id=callback.message.message_id)


# TITLE
# 1 step of creating wishlist and handling input
@router.message(StateFilter(FSMNewWishList.fill_title_list))
async def process_title_sent(message: Message, i18n: dict[str, str], state: FSMContext):
    keyboard = create_inline_kb(1, i18n, btn_my_wishlists='cancel_wishlist_creation')
    title = message.text.strip()

    # validating input
    if not (4 <= len(title) <= 50):
        await process_invalid_input(message, i18n, 'invalid_title_length')
    else:
        state_data = await state.get_data()
        last_message_id = state_data.get('last_message_id')
        await edit_last_msg(last_message_id, state, title, message, i18n, keyboard, 'title',
                            'create_wishlist_description')
        await state.set_state(FSMNewWishList.fill_description_list)


# DESCRIPTION (OPTIONAL)
# 2 step of creating wishlist
@router.message(StateFilter(FSMNewWishList.fill_description_list))
async def process_description_sent(message: Message, i18n: dict[str, str], state: FSMContext):
    keyboard = create_inline_kb(1, i18n, btn_my_wishlists='cancel_wishlist_creation')
    description = message.text.strip()

    # validating input
    if len(description) > 300:
        await process_invalid_input(message, i18n, 'invalid_description_length')
    else:
        if description == '/skip':
            description = ''
        state_data = await state.get_data()
        last_message_id = state_data.get('last_message_id')
        await edit_last_msg(last_message_id, state, description, message, i18n, keyboard, 'description',
                            'create_wishlist_date')
        await state.set_state(FSMNewWishList.fill_date)


# DATE (OPTIONAL)
# 3 step
@router.message(StateFilter(FSMNewWishList.fill_date))
async def process_date_sent(message: Message, i18n: dict[str, str], state: FSMContext):
    keyboard = create_inline_kb(1, i18n, 'start_menu', 'btn_my_wishlists')
    date_str = message.text.strip()

    async with ChatActionSender.typing(bot=message.bot, chat_id=message.from_user.id):

        if not await validate_date_input(date_str, message, i18n):
            return

        try:
            state_data = await state.get_data()
            last_message_id = state_data.get('last_message_id')
            user_id = message.from_user.id

            event_date = None
            if date_str and date_str != '/skip':
                event_date = datetime.strptime(date_str, "%d.%m.%Y")
            else:
                date_str = ''

            wishlist = await create_or_update_wishlist(
                user_id=user_id,
                title=state_data.get('title', ''),
                description=state_data.get('description', ''),
                event_date=event_date
            )

            success_message = i18n['wishlist_created'].format(
                title=wishlist.title or i18n.get('not_specified'),
                description=wishlist.description or i18n.get('not_specified'),
                date=date_str if date_str else i18n.get('not_specified')
            )

            await edit_last_msg(
                last_message_id,
                state,
                date_str,
                message,
                i18n,
                keyboard,
                'date',
                success_message
            )

            await state.clear()

        except ValueError as e:
            await message.answer(i18n['error_occurred'].format(error=str(e)))
        except Exception as e:
            logger.error(f"Error creating wishlist: {e}")
            await message.answer(i18n['database_error'])
