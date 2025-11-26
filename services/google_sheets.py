import json
from datetime import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials

import config
from config import GOOGLE_CREDENTIALS_PATH, DRIVERS

from zoneinfo import ZoneInfo

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

    now = datetime.now(ZoneInfo("Europe/Minsk"))
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

    update_drivers_in_config()


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


def get_records_by_month(user_id: int, month: int, year: int):
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

        drivers_ids = list()

        for row in all_data[1:]:
            try:
                if len(row) > 6 and row[6].strip():
                    telegram_id = int(row[6].strip())
                    drivers_ids.append(telegram_id)
            except (ValueError, IndexError):
                continue
        print(f"Найдены ID водителей: {drivers_ids}")
        return sorted(list(drivers_ids))

    except Exception as e:
        print(f"Ошибка при получении списка водителей: {e}")
        return []


def update_drivers_in_config():
    """Функция для обновления списка водителей"""

    try:
        current_drivers = get_drivers_from_sheets()
        if not isinstance(config.DRIVERS, list):
            config.DRIVERS = []

        merged = set(config.DRIVERS) | set(current_drivers)
        config.DRIVERS[:] = sorted(list(merged))

        print(f"✅ Список DRIVERS обновлен: {config.DRIVERS}")
        return config.DRIVERS

    except Exception as e:
        print(f"❌ Ошибка при обновлении DRIVERS: {e}")
        return []


def get_admin_summary(period:str):
    """Функция для получения отчета за все периоды для администратора"""

    records = sheet.get_all_values()
    headers = records[0]
    rows = records[1:]

    today_str = datetime.now().strftime('%d.%m.%Y')
    month_str = datetime.now().strftime('%m.%Y')

    summary = {}
    for row in rows:
        if len(row) < 8:
            continue

        date, _, record_type, _, amount, _, user_id, username = row
        if period == 'day' and date != today_str:
            continue

        if period == 'month' and  not date.endswith(month_str):
            continue

        try:
            amount = float(amount.replecace(',', '.'))
        except ValueError:
            continue

        if username not in summary:
            summary[username] = {"income": 0, "expense": 0}

        if record_type.lower() == 'доход':
            summary[username]["income"] += amount
        elif record_type.lower() == 'расход':
            summary[username]["expense"] += amount

    lines =[]
    total_income = 0
    total_expense = 0

    for user, data in summary.items():
        lines.append(
            f"{user} - Доход: {data['income']:.2f}, Расход: {data['expense']:.2f}"
        )
        total_income += data['income']
        total_expense += data['expense']

    lines.append("Итого : ")
    lines.append(f"Доход : {total_income:.2f}")
    lines.append(f"Расход : {total_expense:.2f}")
    lines.append(f"Баланс : {total_income - total_expense:.2f}")

    return "\n".join(lines) if lines else "Нет данных за выбранный период"


def get_all_data():
    """"Функция для получения всех данных из таблицы"""

    return sheet.get_all_values()