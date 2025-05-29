
import os
import gspread
from dotenv import load_dotenv
from oauth2client.service_account import ServiceAccountCredentials

load_dotenv()
GOOGLE_CREDS_FILE = os.getenv("GOOGLE_CREDS_FILE")
TELEGRAM_BOT_NAME = os.getenv("TELEGRAM_BOT_NAME")

# this part is to set up the google sheet

scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name(GOOGLE_CREDS_FILE, scope)
client = gspread.authorize(creds)
sheet = client.open(TELEGRAM_BOT_NAME).sheet1