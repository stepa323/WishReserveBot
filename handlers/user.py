from aiogram import Router, F
from aiogram.filters import CommandStart, Command, StateFilter
from aiogram.fsm.state import default_state
from aiogram.types import Message, CallbackQuery
from keyboards.keyboard_utils import create_inline_kb

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
    
    # Send welcome message with the generated keyboard
    await message.answer(
        text=i18n.get('/start'),  # Get localized start message
        reply_markup=keyboard
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

# Handler for "My Wishlists" button click
@router.callback_query(F.data == 'btn_my_wishlists', StateFilter(default_state))
async def process_btn_my_wishlist_click(callback: CallbackQuery, i18n: dict[str, str]):
    """
    Displays user's wishlists or empty state if none exist.
    
    Args:
        callback: The callback query object 
        i18n: Dictionary containing localized strings
    """
    # TODO: Fetch actual wishlists from database
    wishlists = False  # Placeholder for actual data

    await callback.answer()  # Acknowledge callback
    
    # Create keyboard with "Create Wishlist" and back button
    keyboard = create_inline_kb(1, i18n, 'btn_create_wishlist', start_menu='btn_go_back')
    
    # Show appropriate message based on whether wishlists exist
    if not wishlists:
        await callback.message.edit_text(
            text=i18n.get('my_wishlists_if_none'),  # Empty state message
            reply_markup=keyboard
        )
    else:
        await callback.message.edit_text(
            text=i18n.get('my_wishlists'),  # Message with wishlists
            reply_markup=keyboard
        )

# Handler for "Friends' Wishlists" button click  
@router.callback_query(F.data == 'btn_friends_wishlists', StateFilter(default_state))
async def process_btn_friends_wishlists(callback: CallbackQuery, i18n: dict[str, str]):
    """
    Displays friends' wishlists or empty state if none exist.
    
    Args:
        callback: The callback query object
        i18n: Dictionary containing localized strings
    """
    # TODO: Fetch actual friends' wishlists from database
    wishlists = False  # Placeholder for actual data

    await callback.answer()
    
    # Create keyboard with just back button
    keyboard = create_inline_kb(1, i18n, start_menu='btn_go_back')
    
    # Show appropriate message based on data availability
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
