from aiogram.fsm.state import StatesGroup, State


class FSMNewWishList(StatesGroup):
    wishlist_info = State()
    editing_title = State()
    editing_description = State()
    editing_date = State()

class FSMAddItem(StatesGroup):
    item_info = State()
    editing_name = State()
    editing_description = State()
    editing_link = State()
    editing_price = State()
    editing_priority = State()
    editing_photo = State()

class AdminState(StatesGroup):
    waiting_newsletter_message = State()