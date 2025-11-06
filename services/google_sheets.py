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


def get_records_by_month(user_id: int, month: str, year: str):
    """Функция для получения записей за месяц"""

    rows = sheet.get_all_values()[1:]
    filtered_rows = []
    for row in rows:
        try:
            row_date = datetime.strptime(row[0], '%d.%m.%Y')
            row_user_id = row[6]
            if row_date.month == month and row_date.year == year and str(user_id) == row_user_id:
                filtered_rows.append(row)
        except (ValueError, IndexError):
            continue
    return filtered_rows


def get_drivers_from_sheets():
    """Функция для получения всех уникальных водителей из столбца Telegram ID"""

    try:
        all_data = sheet.get_all_values()

        if len(all_data) <= 1:
            return []

        drivers_ids = set()

        for row in all_data[1:]:
            try:
                if len(row) > 6 and row[6].strip():
                    telegram_id = int(row[6].strip())
                    drivers_ids.add(telegram_id)
            except (ValueError, IndexError):
                continue
        print(f"Найдены ID водителей: {drivers_ids}")
        return sorted(list(drivers_ids))

    except Exception as e:
        print(f"Ошибка при получении списка водителей: {e}")
        return []