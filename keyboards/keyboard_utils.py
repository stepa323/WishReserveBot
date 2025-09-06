from typing import Optional

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from database.models import Item, User


def create_inline_kb(
        width: int,
        i18n: dict[str, str],
        *args: str,
        **kwargs: str
) -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()

    buttons: list[InlineKeyboardButton] = []

    if args:
        for button in args:
            if button in i18n.keys():
                text = i18n.get(button)
            else:
                text = button
            buttons.append(InlineKeyboardButton(
                text=text,
                callback_data=button
            ))
    if kwargs:
        for button, text in kwargs.items():
            if text in i18n.keys():
                text = i18n.get(text)
            buttons.append(InlineKeyboardButton(
                text=text,
                callback_data=button
            ))

    kb_builder.row(*buttons, width=width)

    return kb_builder.as_markup()


def wishlist_kb(i18n: dict, is_private: Optional[bool] = None) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(text=i18n['btn_edit_title'], callback_data="edit_title")

    privacy_text = i18n['btn_make_private'] if not is_private else i18n['btn_make_public']
    builder.button(text=privacy_text, callback_data="toggle_privacy")

    builder.button(text=i18n['btn_edit_description'], callback_data="edit_description")
    builder.button(text=i18n['btn_edit_date'], callback_data="edit_date")

    # Кнопки подтверждения/отмены
    builder.button(text=i18n['btn_cancel'], callback_data="cancel")
    builder.button(text=i18n['btn_confirm'], callback_data="confirm")

    # Распределяем кнопки по рядам
    builder.adjust(1,1,1,1,2)

    return builder.as_markup()

def item_kb(i18n: dict) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(text=i18n['btn_edit_name'], callback_data="edit_name")
    builder.button(text=i18n["btn_edit_description"], callback_data="edit_description")

    builder.button(text=i18n['btn_edit_link'], callback_data="edit_link")
    builder.button(text=i18n['btn_edit_price'], callback_data="edit_price")
    builder.button(text=i18n['btn_edit_priority'], callback_data="edit_priority")
    builder.button(text=i18n['btn_edit_photo'], callback_data="edit_photo")
    builder.button(text=i18n['btn_remove_photo'], callback_data="remove_photo")

    # Кнопки подтверждения/отмены
    builder.button(text=i18n['btn_cancel'], callback_data="cancel")
    builder.button(text=i18n['btn_confirm'], callback_data="confirm_item")

    # Распределяем кнопки по рядам
    builder.adjust(1,1,1,1,1,1,1,2)

    return builder.as_markup()


def create_item_keyboard(item: Item, i18n: dict, curr: int, total: int, is_owner=False) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    if is_owner:
        builder.button(
            text=i18n['btn_edit'],
            callback_data=f"edit_item_{item.id}"
        )
    else:
        if not item.is_reserved:
            builder.button(
                text=i18n['btn_reserve'],
                callback_data=f"reserve_item_{item.id}"
            )
        else:
            builder.button(
                text=i18n['btn_reserved'],
                callback_data="already_reserved"
            )

    # Кнопки навигации
    if curr > 1:
        builder.button(text="<<", callback_data=f"prev_item_{item.wishlist_id}_{curr}")
    if curr < total:
        builder.button(text=">>", callback_data=f"next_item_{item.wishlist_id}_{curr}")

    builder.adjust(1, 3)
    return builder.as_markup()