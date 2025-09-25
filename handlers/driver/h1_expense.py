from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from keyboards.reply_kb import back_button_kb, drive_menu
from services.google_sheets import add_record

router = Router()


class ExpenseStates(StatesGroup):
    """Класс состояний для расходов"""

    waiting_for_amount_and_comment = State()


@router.message(F.text == "Расход")
async def start_expense(message: Message, state: FSMContext):
    """Начало добавления расхода"""

    await message.answer(
        "Укажите расход:\nПример:\n`20.30 заправка`",
        parse_mode="Markdown",
        reply_markup=back_button_kb()
    )
    await state.set_state(ExpenseStates.waiting_for_amount_and_comment)


@router.message(ExpenseStates.waiting_for_amount_and_comment, F.text == "🔙 Назад")
async def back_from_expense(message: Message, state: FSMContext):
    """Возврат в водительский меню"""

    await state.clear()
    await message.answer("Возврат в главное меню", reply_markup=drive_menu())


@router.message(ExpenseStates.waiting_for_amount_and_comment)
async def process_expense(message: Message, state: FSMContext):
    """Обработка ввода суммы и комментария"""

    try:
        parts = message.text.split(maxsplit=1)
        amount = float(parts[0].replace(",", "."))
        comment = parts[1] if len(parts) > 1 else "-"
    except (ValueError, IndexError):
        await message.answer(" Введите корректно, например: 20 заправка")
        return

    add_record(
        user_id=message.from_user.id,
        username=message.from_user.full_name,
        record_type="расход",
        subcategory="расход",
        amount=amount,
        comment=comment
    )

    await message.answer(
        f"Расход зарегистрирован:\n"
        f"Сумма: {amount:.2f} byn.\n"
        f"Комментарий: {comment}",
        reply_markup=drive_menu()
    )
    await state.clear()
