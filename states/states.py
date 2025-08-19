from aiogram.fsm.state import StatesGroup, State


class FSMNewWishList(StatesGroup):
    wishlist_info = State()
    editing_title = State()
    editing_description = State()
    editing_date = State()

class FSMNewGift(StatesGroup):
    fill_title_gift = State()
    fill_photo = State()
    fill_description_gift = State()
    fill_price = State()
    fill_link = State()
    fill_priority = State()

class AdminState(StatesGroup):
    waiting_newsletter_message = State()