from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from services.google_sheets import add_record
from keyboards.reply_kb import admin_menu, driver_menu
from services.request_store import get_request, remove_request

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


@router.callback_query(F.data.startswith("add_driver:"))
async def add_driver_from_callback(callback: CallbackQuery):
    """Функция добавления водителя с помощью инлайн-кнопки"""

    _, token = callback.data.split(":", 1)

    data = get_request(token)
    if not data:
        await callback.answer("Данные не найдены или уже обработаны.", show_alert=True)
        return

    driver_id = data["user_id"]
    driver_name = data["user_name"]

    add_record(
        user_id=driver_id,
        username=driver_name,
        record_type="водитель",
        subcategory="регистрация",
        amount=0,
        comment="новый сотрудник добавлен"
    )

    remove_request(token)

    new_text = callback.message.text + "\n\n✅ Водитель зарегистрирован."

    await callback.message.edit_text(new_text)
    await callback.answer("Готово.")

    try:
        await callback.bot.send_message(
            driver_id,
            "Добро пожаловать! Вы успешно добавлены.",
            reply_markup=driver_menu()
        )
    except:
        pass

@router.message(AddDriver.waiting_id)
async def get_id_drivers(message: Message, state: FSMContext):
    """Получение id водителя"""

    new_driver_id = int(message.text)

    await state.update_data(new_driver_id=new_driver_id)
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


    try:
        await message.bot.send_message(new_driver_id, text='Теперь Вы можете пользоваться ботом',
                                       reply_markup=driver_menu())
    except:
        await message.answer('Не удалось отправить сообщение')

    await state.clear()