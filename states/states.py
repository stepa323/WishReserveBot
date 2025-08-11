from aiogram.fsm.state import StatesGroup, State


class FSMNewWishList(StatesGroup):
    fill_title_list = State()
    fill_description_list = State()
    fill_date = State()

class FSMNewGift(StatesGroup):
    fill_title_gift = State()
    fill_photo = State()
    fill_description_gift = State()
    fill_price = State()
    fill_link = State()
    fill_priority = State()

class AdminState(StatesGroup):
    waiting_newsletter_message = State()