from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from keyboards.reply_kb import admin_menu

router = Router()


@router.message(F.text == "Назад ◀️")
async def back_to_admin_menu(message: Message, state: FSMContext):
    """Функция для возврата в меню админа"""

    await state.clear()
    await message.answer(text="Меню администратора", reply_markup=admin_menu())
