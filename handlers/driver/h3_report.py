from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from datetime import datetime

from keyboards.reply_kb import report_menu_driver_kb
from services.google_sheets import get_records_by_day

router = Router()

MONTHS = {
    1: 'Январь',
    2: 'Февраль',
    3: 'Март',
    4: 'Апрель',
    5: 'Май',
    6: 'Июнь',
    7: 'Июль',
    8: 'Август',
    9: 'Сентябрь',
    10: 'Октябрь',
    11: 'Ноябрь',
    12: 'Декабрь'
}


@router.message(F.text == 'Отчёт 📊')
async def report_menu(message: Message, state: FSMContext):
    """Функция для отображения меню отчёта."""

    await state.clear()
    await message.answer("Выберите период отчёта:", reply_markup=report_menu_driver_kb())


@router.message(F.text == "Текущий день ☀️")
async def report_current_day(message: Message):
    """Функция для отображения отчёта за текущий день."""

    telegram_id = message.from_user.id
    today = datetime.now().strftime("%d.%m.%Y")

    records = get_records_by_day(telegram_id, today)
    if not records:
        await message.answer("Нет данных за сегодня.")
        return

    text_lines = [f"Отчёт за {today}:\n"]

    total_income = total_expense = 0
    for record in records:
        time, record_type, category, amount, comment = record[1], record[2], record[3], record[4], record[5]
        line = f"{time}    {record_type.upper()}   {amount}руб. "
        if comment:
            line += f"{comment}"
        text_lines.append(line)

        try:
            amt = float(amount.replace(',', '.'))
            if record_type == "Доход":
                total_income += amt
            elif record_type == "Расход":
                total_expense += amt
        except ValueError:
            pass

    text_lines.append(f"\nВсего доходов: {total_income:.2f}")
    text_lines.append(f"\nВсего расходов: {total_expense:.2f}")
    text_lines.append(f"\nПрибыль: {total_income - total_expense:.2f}")

    await message.answer("\n".join(text_lines))