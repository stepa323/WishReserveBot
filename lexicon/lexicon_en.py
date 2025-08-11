LEXICON_EN = {
    '/start': '''🌟 <b>Welcome to WishReserveBot!</b> 🌟

🎁 Create perfect wish lists for any occasion! 
🔒 Let friends secretly reserve gifts without spoiling surprises.

Start your gifting journey now! ✨''',

    '/help': '''🆘 <b>Need assistance?</b>

Our support team is available 24/7 to help you.''',

    'start_menu': '🏠 Main Menu',
    'btn_start': '🚀 Begin',
    'btn_support': '💬 Support',
    'btn_go_back': '↩ Back',
    'btn_my_wishlists': '📋 My Wishlists',
    'btn_friends_wishlists': "👯 Friends' Lists",
    'btn_help': '❓ Help Center',
    'btn_create_wishlist': '➕ New Wishlist',

    'my_wishlists_if_none': '''📭 <b>No wishlists yet</b>

Let's create your first wishlist - it takes just a minute!''',

    'my_wishlists': '''📚 <b>Your Wishlists</b>

Tap to manage or share with friends''',

    'friends_wishlists_if_none': '''👀 <b>No lists available</b>

Ask friends to share their wishlists with you''',

    'friends_wishlists': '''🎯 <b>Friends' Wishlists</b>

Reserve gifts secretly and make their day!''',

    'create_wishlist_title': '✏️ Enter wishlist title (4-50 chars):',
    'create_wishlist_description': '📝 Add description (optional, /skip to bypass):',
    'create_wishlist_date': '📅 Event date (DD.MM.YYYY or /skip):',
    'wishlist_created': '''✅ <b>Wishlist created successfully!</b>

🎯 <b>Title:</b> {title}
📝 <b>Description:</b> {description}
📅 <b>Date:</b> {date}''',
    'cancel_wishlist_creation': '❌ Cancel',
    'not_specified': 'Not specified',
    'canceled_wishlist_creation': 'ℹ️ Creation canceled',

    # Item creation flow
    'add_item_name': '🎁 Item name:',
    'add_item_description': '📌 Description (optional):',
    'add_item_photo': '📸 Photo (optional):',
    'add_item_price': '💲 Approximate price:',
    'add_item_link': '🔗 Product link (optional):',
    'add_item_priority': '⭐ Priority level:',

    'priority_options': {
        'high': 'Top priority',
        'medium': 'Nice to have',
        'low': 'If possible'
    },

    # Validation messages
    'invalid_title_length': "⚠ Title must be 4-50 characters",
    'invalid_description_length': "⚠ Description exceeds 300 chars",
    'empty_date_error': "⚠ Please enter date",
    'invalid_date_format': "⚠ Use DD.MM.YYYY format",
    'date_in_past_error': "⚠ Date cannot be past",

    'created_by': "Created by",
    'description': "Description",
    'event_date': "Event date",
    'wishlist_items': "Items in wishlist",
    'no_items_in_wishlist': "No items in this wishlist yet",
    'wishlist_not_found': "Wishlist not found",
    'btn_add_item': "➕ Add item",
    'btn_edit_wishlist': "✏️ Edit",
    'btn_share_wishlist': "🔗 Share",

    'admin_welcome': 'Welcome to Admin Panel!',
    'admin_newsletter_btn': 'Newsletter',
    'admin_statistic_btn': 'Statistics',
    "admin_statistics_text": "📊 Bot Statistics:\n\n👤 Users: {users_count}\n🎁 Wishlists: {wishlists_count}\n🎯 Gifts: {gifts_count}",
    'admin_newsletter_start': 'Send the message for newsletter:',
    'admin_newsletter_confirm': 'Are you sure you want to send this message to all users?',
    'admin_newsletter_started': '⏳ Newsletter started...',
    'admin_newsletter_canceled': '❌ Newsletter canceled',
    'admin_newsletter_stats': '📊 Newsletter statistics:\n\n• Total users: {total}\n• Successfully sent: {success}\n• Failed to send: {failed}',
    'confirm_yes': '✅ Yes, send',
    'confirm_no': '❌ Cancel',
    'error_no_message': 'Error: newsletter message not found',
}
