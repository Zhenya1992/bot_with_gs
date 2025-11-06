from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from services.google_sheets import add_record
from keyboards.reply_kb import admin_menu
router = Router()


class RemoveDrivers(StatesGroup):
    """Класс удаления водителей"""

    waiting_for_user_id = State()


@router.message(F.text == "Удалить водителя ❌")
async def start_remove_driver(message: Message, state: FSMContext):
    """Функция удаления водителей"""

    await state.set_state(RemoveDrivers.waiting_for_user_id)
    await message.answer("Введите id водителя для удаления:")


@router.message(RemoveDrivers.waiting_for_user_id)
async def confirm_remove_driver(message: Message, state: FSMContext):
    """Функция подтверждения удаления водителей"""

    try:
        driver_id = int(message.text)
    except ValueError:
        await message.answer("Введите корректный id водителя")
        return

    add_record(
        user_id=driver_id,
        username="удаленный водитель",
        record_type="водитель",
        subcategory="удаление",
        amount=0,
        comment="водитель удален администратором"
    )
    await message.answer(
        f"Водитель с id {driver_id} удален",
        reply_markup=admin_menu()
    )
    await state.clear()