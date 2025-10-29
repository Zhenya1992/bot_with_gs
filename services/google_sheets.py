import json
from datetime import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials

from config import GOOGLE_CREDENTIALS_PATH

scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']

with open(GOOGLE_CREDENTIALS_PATH, 'r') as f:
    creds_dict = json.load(f)

credentials = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
client = gspread.authorize(credentials)

SPREADSHEET_NAME = "bot_with_gs"

spreadsheet = client.open(SPREADSHEET_NAME)
sheet = spreadsheet.sheet1


def add_record(record_type: str, subcategory: str, amount: float, comment: str, user_id: int, username: str):
    """Функция для записи в таблицу Google Sheets"""

    now = datetime.now()
    row = [
        now.strftime('%d.%m.%Y'),
        now.strftime('%H:%M:%S'),
        record_type,
        subcategory,
        amount,
        comment,
        user_id,
        username
    ]
    sheet.append_row(row, value_input_option="USER_ENTERED")


def get_records_by_day(user_id: int, date: str):
    """Функция для получения записей за день"""

    rows = sheet.get_all_values()[1:]
    filtered_rows = []
    for row in rows:
        row_date = row[0]
        row_user_id = row[6]
        if row_date == date and str(user_id) == row_user_id:
            filtered_rows.append(row)
    return filtered_rows
