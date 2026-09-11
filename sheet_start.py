import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]

# Укажи точный путь к твоему json-файлу с ключами
PATH_TO_CREDS = os.path.join(BASE_DIR, "creds.json")

creds = ServiceAccountCredentials.from_json_keyfile_name(PATH_TO_CREDS, scope)
client = gspread.authorize(creds)

# Открываем таблицу по ID из .env
sheet = client.open_by_key(os.getenv("SHEET_ID")).sheet1