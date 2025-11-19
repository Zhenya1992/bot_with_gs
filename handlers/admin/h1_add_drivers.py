from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.state import StatesGroup, State
from services.google_sheets import add_record
from keyboards.reply_kb import driver_menu
from services.request_store import get_request, remove_request

router = Router()


# class AddDriver(StatesGroup):
#     """Класс добавления водителей"""
#
#     waiting_id = State()
#     waiting_name = State()
#

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