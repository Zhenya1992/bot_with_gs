from aiogram.types import Message
from aiogram import F, Router
from keyboards.reply_kb import drive_menu, admin_menu
from utils.auth import check_admin, check_driver


router = Router()


@router.message(F.text == "/start")
async def start(message: Message):
    """Команда /start"""

    user_id = message.from_user.id
    if check_admin(user_id):
        await message.answer("👋 Привет, админ!", reply_markup=admin_menu())

    elif check_driver(user_id):
        await message.answer("👋 Привет, водитель!", reply_markup=drive_menu())
    else:
        await message.answer("Обратитесь к администратору")
