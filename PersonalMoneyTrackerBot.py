# This is to import all the secrets/api keys from .env file
import os
import datetime
from dotenv import load_dotenv
load_dotenv()
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
GOOGLE_CREDS_FILE = os.getenv("GOOGLE_CREDS_FILE")
TELEGRAM_BOT_NAME = os.getenv("TELEGRAM_BOT_NAME")

from google_sheets import sheet
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder, CommandHandler, CallbackQueryHandler,
    MessageHandler, ContextTypes, filters
)
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from state import user_state, save_state



# this is where i handle all the bot functions

# This is /add command where the bot will as for the category
async def add(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🥗 Food", callback_data='category_Food')],
        [InlineKeyboardButton("🚌 Transport", callback_data='category_Transport')],
        [InlineKeyboardButton("☕ Others", callback_data='category_Others')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Select a category:", reply_markup=reply_markup)


# this is to handle the button click and then save the selected category to user state for future use
async def handle_category(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    category = query.data.split("_")[1]
    user_id = str(query.from_user.id)
    user_state[user_id] = {"category": category}
    save_state(user_state)
    await query.message.reply_text(f"How much did you spend on {category.lower()}?")


# This is to handle the user input and saving it into google sheets for references
async def handle_amount(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.message.from_user.id)
    username = update.message.from_user.username or user_id

    if user_id in user_state:
        try:
            amount = float(update.message.text)
            category = user_state[user_id]["category"]
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"Appending to sheet: {username}, {category}, {amount}, {timestamp}")
            sheet.append_row([username, category, amount, timestamp])
            del user_state[user_id]
            save_state(user_state)
            await update.message.reply_text(f"✅ Recorded: ${amount:.2f} for {category}.")
        except ValueError:
            await update.message.reply_text("⚠️ Please enter a valid number.")
    else:
        await update.message.reply_text("Please type /add to start recording an expense.")


if __name__ == '__main__':
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    app.add_handler(CommandHandler("add", add))
    app.add_handler(CallbackQueryHandler(handle_category))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_amount))

    print("🤖 Bot is running...")
    app.run_polling()