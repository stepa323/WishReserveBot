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
    'btn_friends_wishlists': "👯 Friends' Lists",
    'btn_help': '❓ Help Center',

    'my_wishlists_if_none': '''📭 <b>No wishlists yet</b>

Let's create your first wishlist - it takes just a minute!''',

    'my_wishlists': '''📚 <b>Your Wishlists</b>

Tap to manage or share with friends''',

    'friends_wishlists_if_none': '''👀 <b>No lists available</b>

Ask friends to share their wishlists with you''',

    'friends_wishlists': '''🎯 <b>Friends' Wishlists</b>

Reserve gifts secretly and make their day!''',

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

    'created_by': "Created by",
    'description': "Description",
    'event_date': "Event date",
    'wishlist_items': "Items in wishlist",
    'no_items_in_wishlist': "No items in this wishlist yet",
    'wishlist_not_found': "Wishlist not found",
    'btn_add_item': "➕ Add item",
    'btn_edit_wishlist': "✏️ Edit",
    'btn_delete_wishlist': "🗑 Delete",

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

    'invalid_request': '❌ Invalid request',
    'wishlist_deleted_success': '✅ Wishlist successfully deleted',

    # Wishlist interface elements
    "title_button": "✏️ Title: {title}",
    "privacy_button": "🔒 Privacy: {status}",
    "description_button": "📝 Description: {desc}",
    "date_button": "📅 Date: {date}",
    "not_specified": "not specified",
    "private": "private",
    "public": "public",

    # Input prompts
    "enter_title_prompt": "Enter wishlist title (up to 50 characters):",
    "enter_description_prompt": "Enter description (up to 300 characters):",
    "enter_date_prompt": "Enter date in DD.MM.YYYY format:",

    # Error messages
    "title_too_long": "❌ Title is too long (max 50 characters)",
    "description_too_long": "❌ Description is too long (max 300 characters)",
    "invalid_date_format": "❌ Invalid date format. Use DD.MM.YYYY",

    # Main messages
    "wishlist_edit_menu": "📋 Wishlist editing:\n\nSelect parameter to edit:",
    "creation_canceled": "❌ Wishlist creation canceled",
    "wishlist_created": "✅ Wishlist «{title}» created successfully!",
    "view_wishlist": "👀 View wishlist",
    "back_to_wishlist": "👀 Back to wishlist",
    "save_error": "❌ Error saving wishlist",

    # Action buttons
    "cancel": "❌ Cancel",
    "confirm": "✅ Confirm",
    "btn_create_wishlist": "➕ Create wishlist",
    "btn_my_wishlists": "📋 My wishlists",

    # Validation messages
    "invalid_title_length": "Title must be between 4 and 50 characters",
    "invalid_description_length": "Description must not exceed 300 characters",
    "access_denied": "⛔ Access denied",
    "error_occurred": "⚠️ An error occurred",

    "wishlist_shared_with_you": "👤 @{owner_username} shared a wishlist with you:\n🎁 \"{wishlist_title}\"",
    "btn_subscribe": "✅ Subscribe",
    "btn_unsubscribe": "❌ Unsubscribe",
    "btn_subscription_pending": "⏳ Pending",
    "subscribed_success": "✅ Successfully subscribed to the wishlist!",
    "unsubscribed_success": "❌ Unsubscribed from the wishlist",
    "subscription_request_sent": "📨 Subscription request sent to the owner",
    "already_subscribed": "✅ You are already subscribed to this wishlist",
    "not_subscribed": "❌ You are not subscribed to this wishlist",
    "subscription_pending": "⏳ Subscription request is pending approval",
    "you_are_subscribed": "✅ You are subscribed to this wishlist",
    "this_is_your_wishlist": "⭐ This is your wishlist",
    "reserved_by": "Reserved by",
    "wishlist_own_access": "This is your wishlist!",
    "wishlist_private_access": "This is a private wishlist. Request access from the owner",
    "privacy_status": "Privacy status",
    "btn_approve": "✅ Approve",
    "btn_reject": "❌ Reject",
    "wishlist_new_request": "User @{username} wants to subscribe to your wishlist \"{wishlist_title}\"",
    "share_link": "Share link",

    "wishlist_template": "🎁 <b>{title}</b>\n\n👤 Created by: @{owner_username}\n🔒 Privacy: {privacy_value}\n🔗 Share link: <code>{share_url}</code>\n\n📝 Description: {description}\n📅 Event date: {event_date}\n📦 Items: {items_count}\n👥 Subscribers: {subscribers_count}\n\n{subscription_status}",    "privacy_private": "🔒 Private",
    "privacy_public": "🌐 Public",

    "no_description": "no data",
    "no_event_date": "not specified",

    "subscription_owner": "⭐ This is your wishlist",
    "subscription_subscribed": "✅ You are subscribed",
    "subscription_none": "❌ Not subscribed",

    "wishlist_limited_template": "🎁 <b>{title}</b>\n\n👤 Created by: @{owner_username}\n🔒 This is a private wishlist\n\n📝 Description: {description}\n📅 Event date: {event_date}\n\n{subscription_status}",

    "wishlist_private_info": "🔐 This is a private wishlist. Click 'Subscribe' to request access",
    "subscription_pending_info": "⏳ Your access request is pending owner approval",

    "subscription_approved": "✅ Your access request to wishlist \"{wishlist_title}\" has been approved!",
    "subscription_rejected": "❌ Your access request to wishlist \"{wishlist_title}\" has been rejected",

    "subscription_approved_owner": "✅ You approved request from @{username}",
    "subscription_rejected_owner": "❌ You rejected request from @{username}",

    "subscription_not_found": "Subscription request not found",
}
