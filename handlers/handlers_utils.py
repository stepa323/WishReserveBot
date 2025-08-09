import asyncio
from datetime import datetime

from aiogram.fsm.context import FSMContext
from aiogram.types import Message, InlineKeyboardMarkup


async def process_invalid_input(message: Message, i18n: dict[str, str], key: str) -> None:
    """
        Process invalid user input by showing a temporary warning message.

        Args:
            message: The original message from user
            i18n: Dictionary with localized strings
            key: Key for the warning message in i18n dict
        """
    try:
        await message.delete()
    except Exception:
        pass

    warning_msg = await message.answer(text=i18n.get(key))

    # deleting the warning message after 5 secs
    await asyncio.sleep(5)
    try:
        await warning_msg.delete()
    except Exception:
        pass


async def edit_last_msg(
        last_message_id: int,
        state: FSMContext,
        user_input: str,
        message: Message,
        i18n: dict[str, str],
        keyboard: InlineKeyboardMarkup,
        state_key: str,
        i18n_key: str
) -> None:
    """
    Edit the last bot message or send a new one if editing fails.

    Args:
        last_message_id: ID of the last message to edit
        state: FSM context to update data
        user_input: User's input to store in state
        message: Current message object from user
        i18n: Localization dictionary
        keyboard: Reply keyboard markup
        state_key: Key to store data in state
        i18n_key: Key for localized text
    """
    if i18n_key in i18n:
        text = i18n.get(i18n_key)
    else:
        text = i18n_key

    chat_id = message.chat.id

    # Update state with user input
    await state.update_data({state_key: user_input})

    # Try to edit last message if ID exists
    if last_message_id:
        try:
            await message.bot.edit_message_text(
                chat_id=chat_id,
                message_id=last_message_id,
                text=text,
                reply_markup=keyboard
            )
            return
        except Exception:
            pass

    # Fallback to new message if editing fails or no last_message_id
    sent_msg = await message.answer(
        text=text,
        reply_markup=keyboard
    )
    await state.update_data(last_message_id=sent_msg.message_id)
    await message.delete()


async def validate_date_input(date_str: str, message: Message, i18n: dict) -> bool:
    """Validate date input and show errors if needed"""
    if date_str == '/skip':
        return True
    if not date_str:
        await process_invalid_input(message, i18n, 'empty_date_error')
        return False

    if not is_valid_date_format(date_str):
        await process_invalid_input(message, i18n, 'invalid_date_format')
        return False

    if is_date_in_past(date_str):
        await process_invalid_input(message, i18n, 'date_in_past_error')
        return False

    return True


def is_valid_date_format(date_str: str) -> bool:
    """Check if date matches expected format (e.g., DD.MM.YYYY)"""
    try:
        datetime.strptime(date_str, '%d.%m.%Y')
        return True
    except ValueError:
        return False


def is_date_in_past(date_str: str) -> bool:
    """Check if date is in the past"""
    try:
        input_date = datetime.strptime(date_str, '%d.%m.%Y').date()
        return input_date < datetime.now().date()
    except ValueError:
        return False
