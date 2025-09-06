LEXICON_RU = {
    'start_message': '''🌟 <b>Добро пожаловать в WishReserveBot!</b> 🌟

🎁 Создавайте списки желаний для любых событий!
🔒 Друзья смогут незаметно бронировать подарки.

Начните прямо сейчас! ✨''',

    'help_message': '''🆘 <b>Нужна помощь?</b>

Наша поддержка работает круглосуточно.''',
    'support_button': '💬 Поддержка',
    'back_button': '↩ Назад',
    'friends_wishlist_buttons': "👯 Списки желаний друзей",
    'help_button': '❓ Помощь',

    'my_wishlists_if_none': '''📭 <b>Списков пока нет</b>

Создайте первый список желаний за минуту!''',

    'my_wishlists': '''📚 <b>Ваши списки желаний</b>

Нажмите для управления или для того чтобы поделиться с друзьями''',

    'friends_wishlists_if_none': '''👀 <b>Нет доступных списков желаний</b>

Попросите друзей поделиться''',

    'friends_wishlists': '''🎯 <b>Списки друзей</b>

Тайно бронируйте подарки!''',

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

    'created_by': "Автор",
    'description': "Описание",
    'event_date': "Дата события",
    'wishlist_items': "Подарки в вишлисте",
    'no_items_in_wishlist': "В вишлисте пока нет подарков",
    'wishlist_not_found': "Вишлист не найден",
    'btn_add_item': "➕ Добавить подарок",
    'btn_edit_wishlist': "✏️ Редактировать",
    'btn_delete_wishlist': "🗑 Удалить",

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

    'invalid_request': '❌ Неверный запрос',
    'wishlist_deleted_success': '✅ Вишлист успешно удален',

    # Элементы интерфейса вишлиста
    "btn_edit_title": "✏️ Название",
    "btn_edit_description": "✏️ Описание",
    "btn_edit_date": "✏️ Дата",
    "btn_make_private": "🔒 Сделать приватным",
    "btn_make_public": "🌐 Сделать публичным",
    "btn_confirm": "✅ Готово",
    "btn_cancel": "❌ Отмена",
    "not_specified": "не указано",
    "private": "приватный",
    "public": "публичный",

    # Подсказки для ввода
    "enter_title_prompt": "Введите название вишлиста (до 50 символов):",
    "enter_description_prompt": "Введите описание (до 300 символов):",
    "enter_date_prompt": "Введите дату в формате ДД.ММ.ГГГГ:",

    # Сообщения об ошибках
    "title_too_long": "❌ Слишком длинное название (максимум 50 символов)",
    "description_too_long": "❌ Слишком длинное описание (максимум 300 символов)",
    "invalid_date_format": "❌ Неверный формат даты. Используйте ДД.ММ.ГГГГ",

    # Основные сообщения
    "wishlist_edit_menu": "📋 Редактирование вишлиста:\n\nВыберите параметр для изменения:",
    "creation_canceled": "❌ Создание вишлиста отменено",
    "wishlist_created": "✅ Вишлист «{title}» успешно создан!",
    "view_wishlist": "👀 Посмотреть вишлист",
    'back_to_wishlist': '👀 Вернуться к вишлисту',
    "save_error": "❌ Ошибка при сохранении вишлиста",

    # Кнопки действий
    "cancel": "❌ Отмена",
    "confirm": "✅ Подтвердить",
    "btn_create_wishlist": "➕ Создать вишлист",
    "btn_my_wishlists": "📋 Мои вишлисты",

    # Сообщения валидации
    "invalid_title_length": "Название должно быть от 4 до 50 символов",
    "invalid_description_length": "Описание не должно превышать 300 символов",
    "access_denied": "⛔ Доступ запрещен",
    "error_occurred": "⚠️ Произошла ошибка",
    "wishlist_shared_with_you": "👤 @{owner_username} поделился с вами вишлистом:\n🎁 \"{wishlist_title}\"",
    "btn_view_shared_wishlist": "👀 Посмотреть вишлист",
    "btn_subscribe": "✅ Подписаться",
    "btn_unsubscribe": "❌ Отписаться",
    "btn_subscription_pending": "⏳ Ожидание",
    "subscribed_success": "✅ Вы успешно подписались на вишлист!",
    "unsubscribed_success": "❌ Вы отписались от вишлиста",
    "subscription_request_sent": "📨 Запрос на подписку отправлен владельцу",
    "already_subscribed": "✅ Вы уже подписаны на этот вишлист",
    "not_subscribed": "❌ Вы не подписаны на этот вишлист",
    "subscription_pending": "⏳ Запрос на подписку ожидает одобрения",
    "you_are_subscribed": "✅ Вы подписаны на этот вишлист",
    "this_is_your_wishlist": "⭐ Это ваш вишлист",
    "reserved_by": "Забронировано",
    "wishlist_own_access": "Это ваш вишлист!",
    "wishlist_private_access": "Это приватный вишлист. Запросите доступ у владельца",
    "privacy_status": "Статус приватности",
    "btn_approve": "✅ Одобрить",
    "btn_reject": "❌ Отклонить",
    "wishlist_new_request": "Пользователь @{username} хочет подписаться на ваш вишлист \"{wishlist_title}\"",
    "share_link": "Поделиться",

    "wishlist_template": "🎁 <b>{title}</b>\n\n👤 Создатель: @{owner_username}\n🔒 Приватность: {privacy_value}\n🔗 Ссылка: <code>{share_url}</code>\n\n📝 Описание: {description}\n📅 Дата события: {event_date}\n📦 Подарков: {items_count}\n👥 Подписчиков: {subscribers_count}\n\n{subscription_status}",
    "privacy_private": "🔒 Приватный",
    "privacy_public": "🌐 Публичный",

    "no_description": "нет данных",
    "no_event_date": "не указана",

    "subscription_owner": "⭐ Это ваш вишлист",
    "subscription_subscribed": "✅ Вы подписаны",
    "subscription_none": "❌ Не подписаны",

    "wishlist_limited_template": "🎁 <b>{title}</b>\n\n👤 Создатель: @{owner_username}\n\n📝 Описание: {description}\n📅 Дата события: {event_date}\n\n{subscription_status}",

    "wishlist_private_info": "🔐 Это приватный вишлист. Нажмите 'Подписаться' чтобы запросить доступ",
    "subscription_pending_info": "⏳ Ваш запрос на доступ ожидает одобрения владельцем",
    "subscription_approved": "✅ Ваш запрос на доступ к вишлисту \"{wishlist_title}\" одобрен!",
    "subscription_rejected": "❌ Ваш запрос на доступ к вишлисту \"{wishlist_title}\" отклонен",

    "subscription_approved_owner": "✅ Вы одобрили запрос от @{username}",
    "subscription_rejected_owner": "❌ Вы отклонили запрос от @{username}",

    "subscription_not_found": "Запрос на подписку не найден",

    "item_preview": "🎁 <b>Добавление подарка:</b>\n\n📝 <b>Название:</b> {name}\n📄 <b>Описание:</b> {description}\n🔗 <b>Ссылка:</b> {link}\n💰 <b>Цена:</b> {price}\n🎯 <b>Приоритет:</b> {priority}\n\nВыберите поле для редактирования:",
    "btn_edit_name": "✏️ Название",
    "btn_edit_link": "✏️ Ссылка",
    "btn_edit_price": "✏️ Цена",
    "btn_edit_priority": "✏️ Приоритет",
    "btn_edit_photo": "📸 Фото",

    "enter_item_name": "📝 Введите название подарка:",
    "enter_item_description": "📄 Введите описание подарка:",
    "enter_item_link": "🔗 Введите ссылку на подарок:",
    "enter_item_price": "💰 Введите цену подарка:",
    "select_item_priority": "🎯 Выберите приоритет подарка:",
    "send_item_photo": "📸 Отправьте фото подарка:",
    "btn_remove_photo": "🗑️ Удалить фото",

    "blank_name_error": "Название не может быть пустым",
    "item_name_too_long": "❌ Название слишком длинное (макс. 50 символов)",
    "item_description_too_long": "❌ Описание слишком длинное (макс. 300 символов)",
    "invalid_price": "❌ Неверный формат цены",

    "item_added_success": "✅ Подарок \"{name}\" успешно добавлен!",
    "item_add_error": "❌ Ошибка при добавлении подарка",

    "priority_low": "📉 Низкий",
    "priority_medium": "📊 Средний",
    "priority_high": "📈 Высокий",

    "no_data": "не указано",

    "price": "Цена",
    "priority": "Приоритет",
    "link": "Ссылка",


    "btn_reserve": "🎁 Забронировать",
    "btn_reserved": "✅ Забронировано",
    "btn_already_reserved": "⛔ Уже забронировано",

    "item_updated": "✅ Подарок \"{name}\" успешно обновлен!",

}
