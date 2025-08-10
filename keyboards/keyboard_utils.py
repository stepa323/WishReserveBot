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
                text=button
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
