from aiogram import Router, F
from aiogram.filters import CommandStart, Command, StateFilter
from aiogram.fsm.state import default_state
from aiogram.types import Message, CallbackQuery
from aiogram.utils.chat_action import ChatActionSender

from keyboards.keyboard_utils import create_inline_kb

from database.requests import get_or_create_user, get_wishlists, get_friends_wishlists, get_wishlist

# Initialize router for handling messages and callbacks
router = Router()


# Handler for /start command (only in default state)
@router.message(CommandStart(), StateFilter(default_state))
async def process_start_message(message: Message, i18n: dict[str, str]):
    """
    Handles the /start command by sending a welcome message with interactive buttons.
    """
    # Create inline keyboard with 1 buttons per row using localization keys
    keyboard = create_inline_kb(1, i18n, 'btn_my_wishlists', 'btn_friends_wishlists', 'btn_help')

    # Get or create user
    await get_or_create_user(
        telegram_id=message.from_user.id,
        username=message.from_user.username
    )

    # Send welcome message with the generated keyboard
    await message.answer(
        text=i18n.get('/start'),
        reply_markup=keyboard,
        message_effect_id="5046509860389126442"
    )


# Handler for returning to start menu via callback
@router.callback_query(F.data == 'start_menu', StateFilter(default_state))
async def process_start_message(callback: CallbackQuery, i18n: dict[str, str]):
    """
    Handles the 'start_menu' callback to return to main menu.
    """
    # Recreate the main menu keyboard
    keyboard = create_inline_kb(1, i18n, 'btn_my_wishlists', 'btn_friends_wishlists', 'btn_help')

    # Acknowledge the callback (removes loading animation)
    await callback.answer()

    # Edit the existing message to show main menu
    await callback.message.edit_text(
        text=i18n.get('/start'),
        reply_markup=keyboard
    )


@router.callback_query(F.data == 'btn_my_wishlists', StateFilter(default_state))
async def process_btn_my_wishlist_click(callback: CallbackQuery, i18n: dict[str, str]):
    """
    Displays user's wishlists with interactive buttons or empty state if none exist.
    """
    user_id = callback.from_user.id
    wishlists = await get_wishlists(user_id)

    await callback.answer()  # Acknowledge callback

    async with ChatActionSender.typing(bot=callback.bot, chat_id=callback.from_user.id):
        if not wishlists:
            keyboard = create_inline_kb(1, i18n, 'btn_create_wishlist', start_menu='btn_go_back')
            await callback.message.edit_text(
                text=i18n.get('my_wishlists_if_none'),
                reply_markup=keyboard
            )
        else:
            wishlists_buttons = {}
            for wishlist in wishlists:
                wishlists_buttons[f'view_wishlist_{wishlist.id}'] = f'🎁 {wishlist.title}'

            keyboard = create_inline_kb(1, i18n, **wishlists_buttons, btn_create_wishlist='btn_create_wishlist',
                                        start_menu='btn_go_back')

            await callback.message.edit_text(
                text=i18n.get('my_wishlists'),
                reply_markup=keyboard
            )


@router.callback_query(F.data == 'btn_friends_wishlists', StateFilter(default_state))
async def process_btn_friends_wishlists(callback: CallbackQuery, i18n: dict[str, str]):
    """
    Displays friends' wishlists with sharing status or empty state.
    """
    user_id = callback.from_user.id
    friends_wishlists = await get_friends_wishlists(user_id)

    await callback.answer()

    if not friends_wishlists:
        keyboard = create_inline_kb(1, i18n, start_menu='btn_go_back')
        await callback.message.edit_text(
            text=i18n.get('friends_wishlists_if_none'),
            reply_markup=keyboard
        )
    else:
        wishlists_buttons = {}
        for wishlist in friends_wishlists:
            wishlists_buttons[f'view_wishlist_{wishlist.id}'] = f'🎁 {wishlist.title}'

        keyboard = create_inline_kb(1, i18n, **wishlists_buttons,
                                    start_menu='btn_go_back')

        await callback.message.edit_text(
            text=i18n.get('friends_wishlists'),
            reply_markup=keyboard
        )


@router.callback_query(F.data.startswith('view_wishlist'))
async def view_wishlist(callback: CallbackQuery, i18n: dict[str, str]):
    """
    Displays wishlist title, description, event date and gifts with interactive buttons
    """
    await callback.answer()
    async with ChatActionSender.typing(bot=callback.bot, chat_id=callback.from_user.id):
        wishlist_id = int(callback.data.split('view_wishlist_')[1])

        wishlist = await get_wishlist(wishlist_id=wishlist_id, with_items=True, with_owner=True)

        if not wishlist:
            await callback.message.edit_text(
                text=i18n.get('wishlist_not_found'),
                reply_markup=create_inline_kb(1, i18n, start_menu='btn_go_back')
            )
            return

        # Format wishlist details
        text_parts = [
            f"=============================="
            f"📌 <b>{wishlist.title}</b>",
            f"👤 {i18n.get('created_by')}: @{wishlist.owner.username}"
        ]

        if wishlist.description:
            text_parts.append(f"\n📝 {i18n.get('description')}:\n{wishlist.description}")

        if wishlist.event_date:
            formatted_date = wishlist.event_date.strftime("%d.%m.%Y")
            text_parts.append(f"\n📅 {i18n.get('event_date')}: {formatted_date}")

        if wishlist.owner.telegram_id == callback.from_user.id:
            keyboard = create_inline_kb(
                2,
                i18n,
                **{f"add_item_{wishlist.id}": 'btn_add_item',
                   f"edit_wishlist_{wishlist.id}": 'btn_edit_wishlist',
                   f"share_wishlist_{wishlist.id}": 'btn_share_wishlist'},
                btn_my_wishlists='btn_go_back'
            )
        else:
            keyboard = create_inline_kb(3, i18n, btn_friends_wishlists='btn_go_back')

        await callback.message.edit_text(
            text='\n'.join(text_parts),
            reply_markup=keyboard
        )


# Handler for "Help" button click
@router.callback_query(F.data == 'btn_help', StateFilter(default_state))
async def process_btn_help(callback: CallbackQuery, i18n: dict[str, str]):
    """
    Displays help information with support options.
    """
    # Create help menu keyboard with support option
    keyboard = create_inline_kb(1, i18n, 'btn_support', start_menu='btn_go_back')

    await callback.answer()

    # Show help message
    await callback.message.edit_text(
        text=i18n.get('/help'),
        reply_markup=keyboard
    )


# Handler for /help command
@router.message(Command(commands='/help'), StateFilter(default_state))
async def process_help_command(message: Message, i18n: dict[str, str]):
    """
    Handles the /help command via message (alternative to button click).
    """
    # Create help keyboard
    keyboard = create_inline_kb(1, i18n, 'btn_support')

    # Send help message
    await message.answer(
        text=i18n.get('/help'),
        reply_markup=keyboard
    )

