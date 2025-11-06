from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from services.google_sheets import add_record, get_drivers_from_sheets
from keyboards.reply_kb import admin_menu
router = Router()


class AddDriver(StatesGroup):
    """Класс добавления водителей"""

    waiting_id = State()
    waiting_name = State()


@router.message(F.text == "Добавить водителя ✅")
async def ask_for_driver_id(message: Message, state: FSMContext):
    """Реакция на кнопку добавить водителя"""

    await state.set_state(AddDriver.waiting_id)
    await message.answer("Введите новый телеграмм ID водителя")


@router.message(AddDriver.waiting_id)
async def get_id_drivers(message: Message, state: FSMContext):
    """Получение id водителя"""

    new_driver_id = int(message.text)

    await state.update_data(new_driver_id=new_driver_id)
    existing_drivers_ids = get_drivers_from_sheets()
    if not existing_drivers_ids:
        await message.answer("Ошибка получения данных из Google Sheets")
        return
    if new_driver_id in existing_drivers_ids:
        await message.answer(
            f"Водитель с таким ID уже существует:\n{new_driver_id}",
            reply_markup=admin_menu())
        await state.clear()
        return

    await state.set_state(AddDriver.waiting_name)
    await message.answer(f"Введите имя водителя")


@router.message(AddDriver.waiting_name)
async def get_name_drivers(message: Message, state: FSMContext):
    """Получение имени водителя"""

    user_data = await state.get_data()
    new_driver_id = user_data["new_driver_id"]
    new_driver_name = message.text

    add_record(
        user_id=new_driver_id,
        username=new_driver_name,
        record_type="водитель",
        subcategory="регистрация",
        amount=0,
        comment="новый сотрудник добавлен",
    )

    await message.answer(
        f"Добавлен новый водитель:\n{new_driver_id}\n",
        reply_markup=admin_menu())
    await state.clear()