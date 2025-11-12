from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from keyboards.reply_kb import report_menu_admin_kb

router = Router()


@router.message(F.text == "Сводный отчёт 📈")
async def admin_summary_menu(message: Message, state: FSMContext):
    """Меню для выбора отчета за выбранный период"""

    await state.clear()
    await message.answer("Выберите период, :", reply_markup=report_menu_admin_kb())

