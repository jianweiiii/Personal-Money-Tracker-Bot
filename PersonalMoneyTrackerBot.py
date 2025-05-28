import os
from dotenv import load_dotenv

load_dotenv()
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
GOOGLE_CREDS_FILE = os.getenv("GOOGLE_CREDS_FILE")

from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# 🔐 Setup Google Sheet
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name(GOOGLE_CREDS_FILE, scope)
client = gspread.authorize(creds)
sheet = client.open("Personal Money Tracker Bot").sheet1  # Change to your sheet name

# 🤖 Telegram Bot Handlers
async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user.username or str(update.message.from_user.id)
    sheet.append_row([user, "Hello"])
    await update.message.reply_text("👋 Sent 'Hello' to Google Sheet!")

if __name__ == '__main__':
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    app.add_handler(CommandHandler("hello", hello))

    app.run_polling()
