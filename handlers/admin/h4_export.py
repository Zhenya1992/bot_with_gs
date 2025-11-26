from aiogram.types import Message, FSInputFile
from aiogram import Router, F
from datetime import datetime
import pandas as pd
from keyboards.reply_kb import export_period_kb
from services.google_sheets import get_all_data


router = Router()


@router.message(F.text == "Выгрузка ⬇️")
async def export_requests(message: Message):
    """"Функция меню для выгрузки для выбранного периода"""

    await message.answer(text="Выберите период для выгрузки данных:", reply_markup=export_period_kb())


@router.message(F.text.in_(["За день 🌞", "За месяц 🌙", "За всё время 📅" ]))
async def export_period(message: Message):
    """Функция для выгрузки данных за выбранный период"""

    all_data = get_all_data()

    columns = [column.strip().lower() for column in all_data[0]]
    df = pd.DataFrame(all_data[1:], columns=columns)

    now = datetime.now()
    period_text = message.text

    if period_text == "За день 🌞":
        df = df[df['дата'] == now.strftime("%d.%m.%Y")]
        file_name = f"export_day_{now.strftime('%Y-%m-%d')}.xlsx"

    elif period_text == "За месяц 🌙":
        months_year = now.strftime("%m.%Y")
        df = df[df['дата'].str.endswith(months_year)]
        file_name = f"export_months_{now.strftime('%Y-%m')}.xlsx"

    else:
        file_name = f"export_all_{now.strftime('%Y-%m-%d')}.xlsx"

    if df.empty:
        await message.answer(text="Нет данных за выбранный период")
        return

    with pd.ExcelWriter(file_name, engine="xlsxwriter") as writer:
        df.to_excel(writer, sheet_name="Все записи", index=False)

        for user, user_df in df.groupby("имя"):
            user_df.to_excel(writer, sheet_name=str(user)[:31], index=False)

        summary = (
            df.groupby("имя")["сумма"]
            .apply(lambda x: pd.to_numeric(x, errors="coerce").sum())
            .reset_index()
        )
        summary.rename(columns={"сумма": "Общая сумма"}, inplace=True)
        summary.to_excel(writer, sheet_name="Сводная таблица", index=False)

    await message.answer_document(FSInputFile(file_name), caption=f"Выгрузка за {period_text}")