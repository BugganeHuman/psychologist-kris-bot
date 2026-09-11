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
PATH_TO_CREDS = os.path.join(BASE_DIR, "creds.json")

creds = ServiceAccountCredentials.from_json_keyfile_name(PATH_TO_CREDS, scope)
client = gspread.authorize(creds)

sheet_final = client.open_by_key(os.getenv("SHEET_ID_FINAL")).sheet1