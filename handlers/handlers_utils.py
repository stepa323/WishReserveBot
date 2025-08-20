from datetime import datetime

from aiogram.types import Message

from database.models import SubscriptionStatus, Wishlist, User
from database.requests import get_subscription, get_subscribers_count


async def validate_date_input(date_str: str) -> str | bool:
    """Validate date input and show errors if needed"""
    if date_str == '/skip':
        return False
    if not date_str:
        return 'empty_date_error'

    if not is_valid_date_format(date_str):
        return 'invalid_date_format'

    if is_date_in_past(date_str):
        return 'date_in_past_error'

    return False


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


async def render_wishlist_template(
        message: Message,
        wishlist: Wishlist,
        user: User,
        i18n: dict
) -> str:
    """Рендерит шаблон вишлиста с количеством подписчиков"""

    bot_username = (await message.bot.get_me()).username
    share_url = f"https://t.me/{bot_username}?start={wishlist.access_uuid}"

    # Описание
    description = wishlist.description if wishlist.description else i18n['no_description']

    # Дата события
    if wishlist.event_date:
        event_date = wishlist.event_date.strftime("%d.%m.%Y")
    else:
        event_date = i18n['no_event_date']

    # Статус приватности
    privacy_value = i18n['privacy_private'] if wishlist.is_private else i18n['privacy_public']

    # Количество подарков
    items_count = len(wishlist.items) if wishlist.items else 0

    # Количество подписчиков
    subscribers_count = await get_subscribers_count(wishlist.id)

    # Статус подписки
    subscription = await get_subscription(user.id, wishlist.id)
    is_owner = wishlist.owner_id == user.id

    if is_owner:
        subscription_status = i18n['subscription_owner']
    elif subscription and subscription.status == SubscriptionStatus.APPROVED:
        subscription_status = i18n['subscription_subscribed']
    elif subscription and subscription.status == SubscriptionStatus.PENDING:
        subscription_status = i18n['subscription_pending']
    else:
        subscription_status = i18n['subscription_none']

    # Рендерим шаблон с подписчиками
    return i18n['wishlist_template'].format(
        title=wishlist.title,
        owner_username=wishlist.owner.username,
        privacy_value=privacy_value,
        share_url=share_url,
        description=description,
        event_date=event_date,
        items_count=items_count,
        subscribers_count=subscribers_count,
        subscription_status=subscription_status
    )


async def render_limited_wishlist_template(
        wishlist: Wishlist,
        i18n: dict,
        is_pending: bool = False
) -> str:
    description = wishlist.description if wishlist.description else i18n['no_description']

    if wishlist.event_date:
        event_date = wishlist.event_date.strftime("%d.%m.%Y")
    else:
        event_date = i18n['no_event_date']

    if is_pending:
        subscription_status = i18n['subscription_pending_info']
    else:
        subscription_status = i18n['wishlist_private_info']

    return i18n['wishlist_limited_template'].format(
        title=wishlist.title,
        owner_username=wishlist.owner.username,
        description=description,
        event_date=event_date,
        subscription_status=subscription_status
    )


def get_i18n(translations: dict, lang: str):
    default_lang = translations.get("default", "en")

    if lang == "default":
        lang = default_lang

    return translations.get(lang) or translations.get(default_lang) or {}
