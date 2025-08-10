from aiogram import Router, F
from aiogram.filters import CommandStart, Command, StateFilter
from aiogram.fsm.state import default_state
from aiogram.types import Message, CallbackQuery
from keyboards.keyboard_utils import create_inline_kb

from database.requests import get_or_create_user, get_wishlists, create_or_update_wishlist

# Initialize router for handling messages and callbacks
router = Router()

# Handler for /start command (only in default state)
@router.message(CommandStart(), StateFilter(default_state))
async def process_start_message(message: Message, i18n: dict[str, str]):
    """
    Handles the /start command by sending a welcome message with interactive buttons.
    
    Args:
        message: The incoming message object
        i18n: Dictionary containing localized strings
    """
    # Create inline keyboard with 2 buttons per row using localization keys
    keyboard = create_inline_kb(2, i18n, 'btn_my_wishlists', 'btn_friends_wishlists', 'btn_help')

    # Get or create user
    user = await get_or_create_user(
        telegram_id=message.from_user.id,
        username=message.from_user.username
    )
    
    # Send welcome message with the generated keyboard
    await message.answer(
        text=i18n.get('/start'),  # Get localized start message
        reply_markup=keyboard
    )
    await message.answer(
        text=f"id:{user.id},tg_id:{user.telegram_id}, username: @{user.username}"
    )

# Handler for returning to start menu via callback
@router.callback_query(F.data == 'start_menu', StateFilter(default_state))
async def process_start_message(callback: CallbackQuery, i18n: dict[str, str]):
    """
    Handles the 'start_menu' callback to return to main menu.
    
    Args:
        callback: The callback query object
        i18n: Dictionary containing localized strings
    """
    # Recreate the main menu keyboard
    keyboard = create_inline_kb(2, i18n, 'btn_my_wishlists', 'btn_friends_wishlists', 'btn_help')

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
    
    keyboard = InlineKeyboardBuilder()
    
    if not wishlists:
        # Empty state
        keyboard.button(
            text=i18n['btn_create_wishlist'],
            callback_data='create_wishlist'
        )
        keyboard.button(
            text=i18n['btn_go_back'],
            callback_data='start_menu'
        )
        await callback.message.edit_text(
            text=i18n['my_wishlists_if_none'],
            reply_markup=keyboard.as_markup()
        )
    else:
        # Display wishlists with pagination
        for wishlist in wishlists:
            keyboard.row(
                InlineKeyboardButton(
                    text=f"🎁 {wishlist.title}",
                    callback_data=f"view_wishlist_{wishlist.id}"
                )
            )
        
        # Add action buttons at the bottom
        keyboard.row(
            InlineKeyboardButton(
                text=i18n['btn_create_wishlist'],
                callback_data='create_wishlist'
            ),
            InlineKeyboardButton(
                text=i18n['btn_go_back'],
                callback_data='start_menu'
            )
        )
        
        wishlists_count = len(wishlists)
        await callback.message.edit_text(
            text=i18n['my_wishlists'].format(count=wishlists_count),
            reply_markup=keyboard.as_markup()
        )


@router.callback_query(F.data == 'btn_friends_wishlists', StateFilter(default_state))
async def process_btn_friends_wishlists(callback: CallbackQuery, i18n: dict[str, str]):
    """
    Displays friends' wishlists with sharing status or empty state.
    """
    user_id = callback.from_user.id
    friends_wishlists = await get_friends_wishlists(user_id)  # Нужно реализовать эту функцию
    
    await callback.answer()
    
    keyboard = InlineKeyboardBuilder()
    
    if not friends_wishlists:
        keyboard.button(
            text=i18n['btn_go_back'],
            callback_data='start_menu'
        )
        await callback.message.edit_text(
            text=i18n['friends_wishlists_if_none'],
            reply_markup=keyboard.as_markup()
        )
    else:
        for wishlist in friends_wishlists:
            friend_name = wishlist.owner.username or f"Friend #{wishlist.owner.id}"
            keyboard.row(
                InlineKeyboardButton(
                    text=f"👤 {friend_name}: {wishlist.title}",
                    callback_data=f"view_friend_wishlist_{wishlist.id}"
                )
            )
        
        keyboard.row(
            InlineKeyboardButton(
                text=i18n['btn_go_back'],
                callback_data='start_menu'
            )
        )
        
        await callback.message.edit_text(
            text=i18n['friends_wishlists'].format(count=len(friends_wishlists)),
            reply_markup=keyboard.as_markup()
        )


# Handler for "Help" button click
@router.callback_query(F.data == 'btn_help', StateFilter(default_state))
async def process_btn_help(callback: CallbackQuery, i18n: dict[str, str]):
    """
    Displays help information with support options.
    
    Args:
        callback: The callback query object
        i18n: Dictionary containing localized strings
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
    
    Args:
        message: The incoming message object
        i18n: Dictionary containing localized strings
    """
    # Create help keyboard (without back button in this case)
    keyboard = create_inline_kb(1, i18n, 'btn_support')

    # Send help message 
    await message.answer(
        text=i18n.get('/help'),
        reply_markup=keyboard
    )
