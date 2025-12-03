from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from services.google_sheets import remove_user_from_sheet
from keyboards.reply_kb import admin_menu, contact_with_admin_kb
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

    result = remove_user_from_sheet(driver_id)
    if not result:
        await message.answer(f"Водитель с таким {driver_id} не найден")
        await state.clear()

        return

    await message.answer(
        f"Водитель с id {driver_id} удален",
        reply_markup=admin_menu()
    )
    await message.bot.send_message(driver_id, "Ваш аккаунт был удален администратором",
                                   reply_markup=contact_with_admin_kb())
    await state.clear()