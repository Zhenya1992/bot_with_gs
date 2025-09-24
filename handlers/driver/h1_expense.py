from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram import F, Router
from aiogram.fsm.state import State, StatesGroup
from keyboards.reply_kb import back_button_kb, drive_menu
from services.google_sheets import add_record

router = Router()


class ExpenseState(StatesGroup):
    """"Класс для хранения состояний расходов"""

    waiting_for_amount_and_comment = State()


@router.message(F.text == 'Расход')
async def expense(message: Message, state: FSMContext):
    """Обработчик команды 'Расход'"""

    await message.answer(
        'Введите сумму и комментарий к расходу:\nПример:\n`20.70 Заправка`',
        reply_markup=back_button_kb(),
        parse_mode='Markdown',
    )

    await state.set_state(ExpenseState.waiting_for_amount_and_comment)


@router.message(F.text == '🔙 Назад', ExpenseState.waiting_for_amount_and_comment)
async def back_to_main_menu(message: Message, state: FSMContext):
    """Возврат в главное меню"""

    await state.clear()
    await message.answer(text='Возвращаемся в главное меню...', reply_markup=drive_menu())


@router.message(ExpenseState.waiting_for_amount_and_comment)
async def get_expense_info(message: Message, state: FSMContext):
    """Получение информации о расходе в виде суммы и комментария"""

    text = message.text.strip()
    parts = text.split(' ', 1)

    try:
        amount = float(parts[0].replace(',', '.'))
        comment = parts[1] if len(parts) > 1 else ''

        add_record(
            user_id=message.from_user.id,
            username=message.from_user.full_name,
            record_type='расход',
            subcategory='-',
            amount=amount,
            comment=comment
        )

        await message.answer(text=f'Расход успешно добавлен:\n{amount}\n{comment}')
        await state.clear()
    except ValueError:
        await message.answer(
            text='Неверный формат ввода данных\nПожалуйста, введите сумму по примеру:\n`20.70 Заправка`',
            parse_mode='Markdown')

