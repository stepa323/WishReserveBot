LEXICON_RU = {
    '/start': '''🌟 <b>Добро пожаловать в WishReserveBot!</b> 🌟

🎁 Создавайте списки желаний для любых событий!
🔒 Друзья смогут незаметно бронировать подарки.

Начните прямо сейчас! ✨''',

    '/help': '''🆘 <b>Нужна помощь?</b>

Наша поддержка работает круглосуточно.''',

    'start_menu': '🏠 Главное меню',
    'btn_start': '🚀 Начать',
    'btn_support': '💬 Поддержка',
    'btn_go_back': '↩ Назад',
    'btn_my_wishlists': '📋 Мои списки желаний',
    'btn_friends_wishlists': "👯 Списки желаний друзей",
    'btn_help': '❓ Помощь',
    'btn_create_wishlist': '➕ Новый список',

    'my_wishlists_if_none': '''📭 <b>Списков пока нет</b>

Создайте первый список желаний за минуту!''',

    'my_wishlists': '''📚 <b>Ваши списки желаний</b>

Нажмите для управления или для того чтобы поделиться с друзьями''',

    'friends_wishlists_if_none': '''👀 <b>Нет доступных списков желаний</b>

Попросите друзей поделиться''',

    'friends_wishlists': '''🎯 <b>Списки друзей</b>

Тайно бронируйте подарки!''',

    'create_wishlist_title': '✏️ Название списка (4-50 знаков):',
    'create_wishlist_description': '📝 Описание (необязательно, /skip чтобы пропустить):',
    'create_wishlist_date': '📅 Дата события (ДД.ММ.ГГГГ или /skip):',
    'wishlist_created': '''✅ <b>Список успешно создан!</b>

🎯 <b>Название:</b> {title}
📝 <b>Описание:</b> {description}
📅 <b>Дата:</b> {date}''',
    'not_specified': 'Не указано',
    'cancel_wishlist_creation': '❌ Отмена',
    'canceled_wishlist_creation': 'ℹ️ Создание отменено',

    # Добавление подарка
    'add_item_name': '🎁 Название:',
    'add_item_description': '📌 Описание (необязательно):',
    'add_item_photo': '📸 Фото (необязательно):',
    'add_item_price': '💲 Примерная цена:',
    'add_item_link': '🔗 Ссылка на товар:',
    'add_item_priority': '⭐ Приоритет:',

    'priority_options': {
        'high': 'Очень хочу',
        'medium': 'Было бы хорошо',
        'low': 'Если получится'
    },

    # Сообщения валидации
    'invalid_title_length': "⚠ От 4 до 50 символов",
    'invalid_description_length': "⚠ Не более 300 знаков",
    'empty_date_error': "⚠ Укажите дату",
    'invalid_date_format': "⚠ Формат ДД.ММ.ГГГГ",
    'date_in_past_error': "⚠ Дата в прошлом",

    'created_by': "Автор",
    'description': "Описание",
    'event_date': "Дата события",
    'wishlist_items': "Подарки в вишлисте",
    'no_items_in_wishlist': "В вишлисте пока нет подарков",
    'wishlist_not_found': "Вишлист не найден",
    'btn_add_item': "➕ Добавить подарок",
    'btn_edit_wishlist': "✏️ Редактировать",
    'btn_share_wishlist': "🔗 Поделиться",

    'admin_welcome': 'Добро пожаловать в Админ-панель!',
    'admin_newsletter_btn': 'Рассылка',
    'admin_statistic_btn': 'Статистика',
    "admin_statistics_text": "📊 Статистика бота:\n\n👤 Пользователей: {users_count}\n🎁 Вишлистов: {wishlists_count}\n🎯 Подарков: {gifts_count}",
    'admin_newsletter_start': 'Отправьте сообщение для рассылки:',
    'admin_newsletter_confirm': 'Вы уверены, что хотите разослать это сообщение всем пользователям?',
    'admin_newsletter_started': '⏳ Начата рассылка...',
    'admin_newsletter_canceled': '❌ Рассылка отменена',
    'admin_newsletter_stats': '📊 Статистика рассылки:\n\n• Всего пользователей: {total}\n• Успешно отправлено: {success}\n• Не удалось отправить: {failed}',
    'confirm_yes': '✅ Да, отправить',
    'confirm_no': '❌ Отменить',
    'error_no_message': 'Ошибка: сообщение для рассылки не найдено',
}
