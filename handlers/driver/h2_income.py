from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from keyboards.reply_kb import reply_income_menu, back_button_kb, driver_menu
from services.google_sheets import add_record

router = Router()


class IncomeStates(StatesGroup):
    choosing_type = State()
    waiting_for_amount = State()
    waiting_for_comment = State()


@router.message(F.text == "Доход ➕")
async def show_income_menu(message: Message, state: FSMContext):
    """Показ меню для регистрации дохода"""

    await message.answer("Выберите тип дохода:", reply_markup=reply_income_menu())
    await state.set_state(IncomeStates.choosing_type)


@router.message(IncomeStates.choosing_type, F.text.in_(["Оплата за заказ 💰", "Доплата по заказу 🫰"]))
async def ask_income_amount(message: Message, state: FSMContext):
    """Запрос суммы дохода"""

    await state.update_data(income_type=message.text)
    await message.answer("Введите сумму числом,🧾 например :\n `4.50`",
                         parse_mode="Markdown",
                         reply_markup=back_button_kb())
    await state.set_state(IncomeStates.waiting_for_amount)


@router.message(IncomeStates.waiting_for_amount)
async def ask_income_comment(message: Message, state: FSMContext):
    """Запрос комментария"""

    if message.text == "Назад ⬅️":
        await state.set_state(IncomeStates.choosing_type)
        await message.answer("Выберите тип дохода:", reply_markup=reply_income_menu())
        return

    try:
        amount = float(message.text.replace(",", "."))
    except ValueError:
        await message.answer("❌ Введите корректную сумму или нажмите 'Назад ⬅️'.")
        return

    await state.update_data(amount=amount)
    await message.answer("Добавьте комментарий, например\n(адрес заказа, через пробел):\n`Гоголя 17`",
                         parse_mode="Markdown",
                         reply_markup=back_button_kb())
    await state.set_state(IncomeStates.waiting_for_comment)


@router.message(IncomeStates.waiting_for_comment)
async def confirm_income(message: Message, state: FSMContext):
    """Подтверждение дохода"""

    user_data = await state.get_data()

    income_type = user_data['income_type']
    amount = user_data['amount']
    comment = message.text

    subcategory = "оплата" if income_type == "Оплата за заказ" else "доплата"

    add_record(
        user_id=message.from_user.id,
        username=message.from_user.full_name,
        record_type='доход',
        subcategory=subcategory,
        amount=amount,
        comment=comment
    )

    await message.answer(
        f"✅ Доход зарегистрирован:\n"
        f"Тип: {income_type}\n"
        f"Сумма: {amount:.2f} byn.\n"
        f"Комментарий: {comment}",
        reply_markup=driver_menu()
    )
    await state.clear()


@router.message(F.text == "⬅️ Назад")
async def go_back(message: Message, state: FSMContext):
    """Возврат в главное меню дохода"""

    await state.clear()
    await message.answer("Возврат в меню ", reply_markup=driver_menu())
