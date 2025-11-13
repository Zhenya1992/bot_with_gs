from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from keyboards.reply_kb import report_menu_admin_kb
from services.google_sheets import get_admin_summary
router = Router()


@router.message(F.text == "Сводный отчёт 📈")
async def admin_summary_menu(message: Message, state: FSMContext):
    """Меню для выбора отчета за выбранный период"""

    await state.clear()
    await message.answer("Выберите период, :", reply_markup=report_menu_admin_kb())


@router.message(F.text == "Сегодня 🕛")
async def admin_summary_today(message: Message):
    """Отчет за сегодня"""

    report = get_admin_summary("day")
    await message.answer(f"Отчет за сегодня:\n{report}")


@router.message(F.text == "Текущий месяц 🈷️")
async def admin_summary_month(message: Message):
    """Отчет за месяц"""

    report = get_admin_summary("month")
    await message.answer(f"Отчет за месяц:\n{report}")


@router.message(F.text == "За всё время 🗓️")
async def admin_summary_all(message: Message):
    """Отчет за весь период"""

    report = get_admin_summary("all")
    await message.answer(f"Отчет за весь период:\n{report}")