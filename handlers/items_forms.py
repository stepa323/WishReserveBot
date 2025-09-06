import logging

from aiogram import F, Router
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

from database.models import PriorityLevel
from database.requests import get_wishlist, get_or_create_user, create_or_update_item, get_item
from handlers.handlers_utils import send_item_info, delete_item_message
from keyboards.keyboard_utils import create_inline_kb, item_kb
from states.states import FSMAddItem

router = Router()
logger = logging.getLogger(__name__)


async def update_item_preview_message(
        last_bot_message: Message | None,
        i18n: dict,
        state: FSMContext,
        new_message_target: Message | CallbackQuery | None = None,
) -> Message:
    data = await state.get_data()

    # Формируем текст предпросмотра
    preview_text = i18n['item_preview'].format(
        name=data.get('name', i18n['no_data']),
        description=data.get('description', i18n['no_data']),
        link=data.get('link', i18n['no_data']),
        price=data.get('price', i18n['no_data']),
        priority=data.get('priority', i18n['no_data'])
    )

    # Создаем клавиатуру
    kb = item_kb(i18n)

    # Определяем какое фото использовать
    photo_id = data.get('photo_id')
    default_photo_id = 'AgACAgIAAxkBAAIEn2i4ZrM8bV59St8pqdofxRprZaKFAAJA-jEbYUnISfxgYrJ1VxanAQADAgADbQADNgQ'
    use_photo = photo_id or default_photo_id  # Если своего фото нет - используем дефолтное

    # Определяем куда отправлять сообщение
    if isinstance(new_message_target, CallbackQuery):
        target = new_message_target.message
    elif isinstance(new_message_target, Message):
        target = new_message_target
    else:
        target = last_bot_message

    # Всегда отправляем как фото сообщение
    if last_bot_message:
        try:
            # Удаляем старое сообщение
            await last_bot_message.delete()
        except TelegramBadRequest:
            pass

    if target:
        msg = await target.answer_photo(
            photo=use_photo,
            caption=preview_text,
            reply_markup=kb,
            parse_mode="HTML"
        )
    else:
        msg = await last_bot_message.answer_photo(
            photo=use_photo,
            caption=preview_text,
            reply_markup=kb,
            parse_mode="HTML"
        )
    return msg


@router.callback_query(F.data.startswith('add_item_'))
async def start_add_item(callback: CallbackQuery, i18n: dict, state: FSMContext):
    """Начинает процесс добавления подарка"""
    await callback.answer()

    await delete_item_message(state)

    wishlist_id = int(callback.data.split('_')[2])

    wishlist = await get_wishlist(wishlist_id)
    user = await get_or_create_user(callback.from_user.id)

    if not wishlist or wishlist.owner_id != user.id:
        await callback.answer(i18n['access_denied'], show_alert=True)
        return

    await state.update_data(
        wishlist_id=wishlist_id,
        item_id=None,
        name=i18n['no_data'],
        description=i18n['no_data'],
        link=i18n['no_data'],
        price=i18n['no_data'],
        priority=i18n['no_data'],
        photo_id=None  # Фото пока нет
    )

    await state.set_state(FSMAddItem.item_info)

    preview_text = i18n['item_preview'].format(
        name=i18n['no_data'],
        description=i18n['no_data'],
        link=i18n['no_data'],
        price=i18n['no_data'],
        priority=i18n['no_data']
    )

    # Используем дефолтное фото (своего еще нет)
    default_photo_id = 'AgACAgIAAxkBAAIEn2i4ZrM8bV59St8pqdofxRprZaKFAAJA-jEbYUnISfxgYrJ1VxanAQADAgADbQADNgQ'

    last_msg = await callback.message.answer_photo(
        photo=default_photo_id,
        caption=preview_text,
        reply_markup=item_kb(i18n),
        parse_mode="HTML"
    )
    await state.update_data(last_bot_message=last_msg)


@router.callback_query(F.data.startswith('edit_item_'))
async def start_edit_item(callback: CallbackQuery, i18n: dict, state: FSMContext):
    """Начинает процесс редактирования подарка"""
    await callback.answer()

    await delete_item_message(state)

    item_id = int(callback.data.split('_')[2])

    item = await get_item(item_id, with_wishlist=True)

    if not item or not item.wishlist:
        await callback.answer(i18n['item_not_found'], show_alert=True)
        return

    user = await get_or_create_user(callback.from_user.id)

    if item.wishlist.owner_id != user.id:
        await callback.answer(i18n['access_denied'], show_alert=True)
        return

    initial_data = {
        'wishlist_id': item.wishlist_id,
        'item_id': item_id,
        'name': item.name or i18n['no_data'],
        'description': item.description or i18n['no_data'],
        'link': item.link or i18n['no_data'],
        'price': str(item.price) if item.price else i18n['no_data'],
        'priority': i18n[f'priority_{item.priority_level.value}'],
        'photo_id': item.photo_id  # Сохраняем оригинальное фото (может быть None)
    }

    await state.update_data(**initial_data)
    await state.set_state(FSMAddItem.item_info)

    # Рендерим предпросмотр
    preview_text = i18n['item_preview'].format(**initial_data)

    # Определяем какое фото использовать
    photo_id = item.photo_id
    default_photo_id = 'AgACAgIAAxkBAAIEn2i4ZrM8bV59St8pqdofxRprZaKFAAJA-jEbYUnISfxgYrJ1VxanAQADAgADbQADNgQ'
    use_photo = photo_id or default_photo_id  # Если своего фото нет - используем дефолтное

    last_msg = await callback.message.answer_photo(
        photo=use_photo,
        caption=preview_text,
        reply_markup=item_kb(i18n),
        parse_mode="HTML"
    )

    await state.update_data(last_bot_message=last_msg)

    # Удаляем оригинальное сообщение
    try:
        await callback.message.delete()
    except TelegramBadRequest:
        pass



@router.callback_query(F.data.startswith('edit_'), StateFilter(FSMAddItem.item_info))
async def start_editing_item_field(callback: CallbackQuery, i18n: dict, state: FSMContext):
    """Начинает редактирование поля подарка"""
    await callback.answer()

    field = callback.data.split('_')[1]

    if field == 'name':
        await state.set_state(FSMAddItem.editing_name)
        # Удаляем старое сообщение и отправляем новое
        await callback.message.delete()
        await callback.message.answer(i18n['enter_item_name'])
    elif field == 'description':
        await state.set_state(FSMAddItem.editing_description)
        await callback.message.delete()
        await callback.message.answer(i18n['enter_item_description'])
    elif field == 'link':
        await state.set_state(FSMAddItem.editing_link)
        await callback.message.delete()
        await callback.message.answer(i18n['enter_item_link'])
    elif field == 'price':
        await state.set_state(FSMAddItem.editing_price)
        await callback.message.delete()
        await callback.message.answer(i18n['enter_item_price'])
    elif field == 'priority':
        await state.set_state(FSMAddItem.editing_priority)
        # Показываем клавиатуру с приоритетами
        keyboard = create_inline_kb(
            3,
            i18n,
            **{
                f"set_priority_{PriorityLevel.LOW.value}": 'priority_low',
                f"set_priority_{PriorityLevel.MEDIUM.value}": 'priority_medium',
                f"set_priority_{PriorityLevel.HIGH.value}": 'priority_high'
            },
            cancel='btn_cancel'
        )
        await callback.message.delete()
        await callback.message.answer(i18n['select_item_priority'], reply_markup=keyboard)
    elif field == 'photo':
        await state.set_state(FSMAddItem.editing_photo)
        await callback.message.delete()
        await callback.message.answer(i18n['send_item_photo'])


@router.callback_query(F.data.startswith('set_priority_'), StateFilter(FSMAddItem.editing_priority))
async def set_item_priority(callback: CallbackQuery, i18n: dict, state: FSMContext):
    """Устанавливает приоритет подарка"""
    await callback.answer()

    priority_value = callback.data.split('_')[2]
    priority = PriorityLevel(priority_value)

    await state.update_data(priority=i18n.get(f'priority_{priority.value}'))
    await state.set_state(FSMAddItem.item_info)

    data = await state.get_data()
    last_bot_message = data.get('last_bot_message')

    new_msg = await update_item_preview_message(last_bot_message, i18n, state)
    await state.update_data(last_bot_message=new_msg)


@router.message(StateFilter(FSMAddItem.editing_name))
async def process_item_name(message: Message, i18n: dict, state: FSMContext):
    """Обрабатывает название подарка"""
    if len(message.text) > 50:
        await message.reply(i18n['item_name_too_long'])
        return

    data = await state.get_data()
    last_bot_message = data.get('last_bot_message')

    await state.update_data(name=message.text)
    await state.set_state(FSMAddItem.item_info)

    try:
        await message.delete()
    except TelegramBadRequest:
        pass

    new_msg = await update_item_preview_message(last_bot_message, i18n, state, message)
    await state.update_data(last_bot_message=new_msg)


@router.message(StateFilter(FSMAddItem.editing_description))
async def process_item_description(message: Message, i18n: dict, state: FSMContext):
    """Обрабатывает описание подарка"""
    if len(message.text) > 300:
        await message.reply(i18n['item_description_too_long'])
        return

    data = await state.get_data()
    last_bot_message = data.get('last_bot_message')

    await state.update_data(description=message.text)
    await state.set_state(FSMAddItem.item_info)

    try:
        await message.delete()
    except TelegramBadRequest:
        pass

    new_msg = await update_item_preview_message(last_bot_message, i18n, state)
    await state.update_data(last_bot_message=new_msg)


@router.message(StateFilter(FSMAddItem.editing_link))
async def process_item_link(message: Message, i18n: dict, state: FSMContext):
    """Обрабатывает ссылку подарка"""
    data = await state.get_data()
    last_bot_message = data.get('last_bot_message')

    await state.update_data(link=message.text)
    await state.set_state(FSMAddItem.item_info)

    try:
        await message.delete()
    except TelegramBadRequest:
        pass

    new_msg = await update_item_preview_message(last_bot_message, i18n, state)
    await state.update_data(last_bot_message=new_msg)


@router.message(StateFilter(FSMAddItem.editing_price))
async def process_item_price(message: Message, i18n: dict, state: FSMContext):
    """Обрабатывает цену подарка"""
    try:
        price = float(message.text)
    except ValueError:
        await message.reply(i18n['invalid_price'])
        return

    data = await state.get_data()
    last_bot_message = data.get('last_bot_message')

    await state.update_data(price=price)
    await state.set_state(FSMAddItem.item_info)

    try:
        await message.delete()
    except TelegramBadRequest:
        pass

    new_msg = await update_item_preview_message(last_bot_message, i18n, state)
    await state.update_data(last_bot_message=new_msg)


@router.message(StateFilter(FSMAddItem.editing_photo), F.photo)
async def process_item_photo(message: Message, i18n: dict, state: FSMContext):
    """Обрабатывает фото подарка"""
    photo_id = message.photo[-1].file_id

    data = await state.get_data()
    last_bot_message = data.get('last_bot_message')

    await state.update_data(photo_id=photo_id)
    await state.set_state(FSMAddItem.item_info)

    try:
        await message.delete()
    except TelegramBadRequest:
        pass

    # Передаем message как new_message_target
    new_msg = await update_item_preview_message(last_bot_message, i18n, state, message)
    await state.update_data(last_bot_message=new_msg)


@router.callback_query(F.data == 'confirm_item', StateFilter(FSMAddItem.item_info))
async def confirm_item(callback: CallbackQuery, i18n: dict, state: FSMContext):
    """Подтверждает добавление/редактирование подарка и показывает обновленные подарки"""
    data = await state.get_data()

    if not data.get('name') or data.get('name') == i18n['no_data']:
        await callback.answer(text=i18n["blank_name_error"], show_alert=True)
        return

    try:
        price = float(data['price']) if data['price'] and data['price'] != i18n['no_data'] else None

        priority = PriorityLevel.MEDIUM
        for level in PriorityLevel:
            if i18n[f'priority_{level.value}'] == data.get('priority'):
                priority = level
                break

        item = await create_or_update_item(
            item_id=data.get('item_id'),
            wishlist_id=data['wishlist_id'],
            name=data['name'],
            description=data['description'] if data['description'] != i18n['no_data'] else None,
            link=data['link'] if data['link'] != i18n['no_data'] else None,
            price=price,
            priority=priority,
            photo_id=data['photo_id']
        )

        # Показываем alert с подтверждением
        action_text = i18n['item_updated'] if data.get('item_id') else i18n['item_added_success']
        await callback.answer(action_text.format(name=item.name), show_alert=True)

        # Получаем обновленный вишлист с подарками
        wishlist = await get_wishlist(data['wishlist_id'], with_items=True, with_owner=True)

        # Получаем пользователя
        user = await get_or_create_user(callback.from_user.id)
        is_owner = wishlist.owner_id == user.id

        # Удаляем сообщение с редактированием подарка
        try:
            await callback.message.delete()
        except TelegramBadRequest:
            pass

        current_item = 1
        for i, item1 in enumerate(wishlist.items, start=1):
            if item1.id == item.id:
                current_item = i
                continue

        await send_item_info(callback.message, current_item, wishlist, i18n, is_owner, True)

        await state.clear()

    except Exception as e:
        logger.error(f"Error saving item: {e}")
        await callback.answer(i18n['item_add_error'], show_alert=True)


@router.callback_query(F.data == 'cancel', StateFilter(FSMAddItem))
async def cancel_item_creation(callback: CallbackQuery, i18n: dict, state: FSMContext):
    """Отменяет создание/редактирование"""
    data = await state.get_data()

    # Показываем alert с отменой
    await callback.answer(i18n['creation_canceled'], show_alert=True)

    wishlist_id = data.get('wishlist_id')

    if wishlist_id:
        # Возвращаемся к вишлисту
        wishlist = await get_wishlist(wishlist_id)

        # Удаляем сообщение с предпросмотром
        try:
            await callback.message.delete()
        except TelegramBadRequest:
            pass

        # Создаем новый callback для возврата
        from aiogram.types import CallbackQuery

        class FakeCallback:
            def __init__(self, message, from_user, access_uuid):
                self.message = message
                self.from_user = from_user
                self.data = f"view_wishlist_{access_uuid}"

            async def answer(self):
                pass

        from handlers.user import view_wishlist

        fake_callback = FakeCallback(callback.message, callback.from_user, wishlist.access_uuid)
        await view_wishlist(fake_callback, i18n)

    await state.clear()

@router.callback_query(F.data == 'remove_photo', StateFilter(FSMAddItem.item_info))
async def remove_item_photo(callback: CallbackQuery, i18n: dict, state: FSMContext):
    """Удаляет фото подарка"""
    await callback.answer()

    await state.update_data(photo_id=None)
    data = await state.get_data()
    last_bot_message = data.get('last_bot_message')

    new_msg = await update_item_preview_message(last_bot_message, i18n, state)
    await state.update_data(last_bot_message=new_msg)
