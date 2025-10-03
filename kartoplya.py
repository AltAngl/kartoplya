from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes, MessageHandler, filters

# Актуальные цены (обновляйте здесь)
PRICES = """
🥬 *АКТУАЛЬНЫЕ ЦЕНЫ:*

🍅 Помидоры - 150₽/кг
🥒 Огурцы - 120₽/кг
🥔 Картофель - 40₽/кг
🥕 Морковь - 50₽/кг
🥬 Капуста - 35₽/кг
🧅 Лук - 45₽/кг
🌶 Перец - 200₽/кг
🍆 Баклажан - 180₽/кг
"""

# Условия доставки (обновляйте здесь)
DELIVERY = """
🚚 *УСЛОВИЯ ДОСТАВКИ:*

• Минимальный заказ: 500₽
• Доставка по городу: 100₽
• При заказе от 2000₽ - доставка БЕСПЛАТНО
• Время доставки: 9:00 - 21:00
• Доставка в день заказа
• Оплата при получении

📞 Контакты: +7 (XXX) XXX-XX-XX
"""

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("💰 Цены", callback_data='prices')],
        [InlineKeyboardButton("🚚 Доставка", callback_data='delivery')],
        [InlineKeyboardButton("📝 Сделать заказ", callback_data='order')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        f"Привет, {update.effective_user.first_name}! 🥬\n\n"
        "Добро пожаловать в магазин свежих овощей!",
        reply_markup=reply_markup
    )

async def show_prices(query):
    keyboard = [[InlineKeyboardButton("⬅️ Назад", callback_data='back')]]
    await query.edit_message_text(
        PRICES,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode='Markdown'
    )

async def show_delivery(query):
    keyboard = [[InlineKeyboardButton("⬅️ Назад", callback_data='back')]]
    await query.edit_message_text(
        DELIVERY,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode='Markdown'
    )

async def start_order(query, context):
    await query.edit_message_text(
        "📝 *Оформление заказа*\n\n"
        "Напишите ваш заказ в формате:\n\n"
        "*Телефон: +375 (00) 0000000*\n"
        "Ваш заказ текстом\n\n"
        "Пример:\n"
        "+375 (29) 1234567\n"
        "Помидоры 2кг, огурцы 3кг, картофель 5кг",
        parse_mode='Markdown'
    )
    context.user_data['ordering'] = True

async def handle_order(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.user_data.get('ordering'):
        return
    
    order_text = update.message.text
    user = update.effective_user
    
    keyboard = [[InlineKeyboardButton("🏠 Главное меню", callback_data='back')]]
    
    await update.message.reply_text(
        f"✅ *Заказ принят!*\n\n"
        f"*От:* {user.first_name} (@{user.username or 'без username'})\n\n"
        f"*Ваш заказ:*\n{order_text}\n\n"
        f"Мы свяжемся с вами в ближайшее время! 📞",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode='Markdown'
    )
    
    context.user_data['ordering'] = False

async def back_to_menu(query):
    keyboard = [
        [InlineKeyboardButton("💰 Цены", callback_data='prices')],
        [InlineKeyboardButton("🚚 Доставка", callback_data='delivery')],
        [InlineKeyboardButton("📝 Сделать заказ", callback_data='order')]
    ]
    await query.edit_message_text(
        "🥬 *Главное меню*\n\nВыберите действие:",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode='Markdown'
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if query.data == 'prices':
        await show_prices(query)
    elif query.data == 'delivery':
        await show_delivery(query)
    elif query.data == 'order':
        await start_order(query, context)
    elif query.data == 'back':
        await back_to_menu(query)

def main():
    TOKEN = "8226837521:AAEN9X67WQQ-zgBPpWZSF-oDNQlZJa5OeAw"
    
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_order))
    
    print("Бот запущен!")
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()

