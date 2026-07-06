from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes

TOKEN = 8990619568:AAG0CrLckhXVzsay0xWvdioKgqLIuyYjDCc
ADMIN_ID = 123456789  # 638020518

user_data = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton("🚗 Пройти верифікацію", callback_data="start_form")]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "🏁 Вітаємо у Project0372-CAR-COMMUNITY!\n\nНатисніть кнопку нижче.",
        reply_markup=reply_markup
    )

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id
    user_data[user_id] = {}

    await query.message.reply_text("👤 Вкажіть ПІБ (Прізвище Ім'я По батькові):")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    text = update.message.text

    if user_id not in user_data:
        return

    data = user_data[user_id]

    if "name" not in data:
        data["name"] = text
        await update.message.reply_text("📱 Вкажіть ваш Telegram (@username):")

    elif "telegram" not in data:
        data["telegram"] = text
        await update.message.reply_text("🚗 Вкажіть марку вашого авто:")

    elif "car" not in data:
        data["car"] = text

        keyboard = [
            [
                InlineKeyboardButton("✅ Одобрити", callback_data=f"approve_{user_id}"),
                InlineKeyboardButton("❌ Відхилити", callback_data=f"reject_{user_id}")
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        msg = f"""📥 Нова заявка

👤 {data['name']}
📱 {data['telegram']}
🚗 {data['car']}"""

        await context.bot.send_message(chat_id=ADMIN_ID, text=msg, reply_markup=reply_markup)

        await update.message.reply_text("✅ Дякуємо! Заявку відправлено.")

async def admin_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    data = query.data

    if data.startswith("approve_"):
        user_id = int(data.split("_")[1])
        await context.bot.send_message(user_id, "🎉 Ваша заявка схвалена! Ласкаво просимо 🚗")

    elif data.startswith("reject_"):
        user_id = int(data.split("_")[1])
        await context.bot.send_message(user_id, "❌ Ваша заявка відхилена.")

def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button, pattern="start_form"))
    app.add_handler(CallbackQueryHandler(admin_buttons))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    app.run_polling()

if __name__ == "__main__":
    main()
