from aiogram.types import Message
from aiogram import F, Router
from keyboards.reply_kb import drive_menu, admin_menu, button_get_id
from utils.auth import check_admin, check_driver

router = Router()


@router.message(F.text == "/start")
async def start(message: Message):
    """Команда /start"""

    await message.answer(text="👋 Привет,\nДля работы с ботом нажмите на кнопку 👇 ", reply_markup=button_get_id())


@router.message(F.text == "🔍 Получить id")
async def get_id(message: Message):
    user_id = message.from_user.id
    if check_admin(user_id):
        await message.answer("👋 Привет, админ!", reply_markup=admin_menu())

    elif check_driver(user_id):
        await message.answer("👋 Привет, водитель!", reply_markup=drive_menu())
    else:
        tg_id = message.from_user.id
        await message.answer(f"{tg_id} ваш id", reply_markup=admin_menu())
