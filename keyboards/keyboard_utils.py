from typing import Optional

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


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


def wishlist_kb(i18n: dict,
                title: Optional[str] = None,
                is_private: Optional[bool] = None,
                description: Optional[str] = None,
                event_date: Optional[str] = None) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    title_text = i18n['title_button'].format(title=title if title else i18n['not_specified'])
    privacy_text = i18n['privacy_button'].format(
        status=i18n['private'] if is_private else i18n['public'] if is_private is not None else i18n['not_specified']
    )
    desc_text = i18n['description_button'].format(
        desc=description if description else i18n['not_specified']
    )
    date_text = i18n['date_button'].format(
        date=event_date if event_date else i18n['not_specified']
    )

    builder.button(text=title_text, callback_data="edit_title")
    builder.button(text=privacy_text, callback_data="toggle_privacy")
    builder.button(text=desc_text, callback_data="edit_description")
    builder.button(text=date_text, callback_data="edit_date")


    builder.button(text=i18n['cancel'], callback_data="cancel")
    if title and is_private is not None:
        builder.button(
            text=i18n['confirm'],
            callback_data="confirm"
        )

    builder.adjust(1, 1, 1, 1, 2)
    return builder.as_markup()