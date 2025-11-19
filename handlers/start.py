from aiogram.types import Message
from aiogram import F, Router
from keyboards.reply_kb import driver_menu, admin_menu, contact_with_admin_kb, wait_button
from utils.auth import check_admin, get_admin_id, check_user_id
from zoneinfo import ZoneInfo
from keyboards.inline_kb import add_driver_inline_kb_with_token
from services.request_store import save_request
import uuid


router = Router()


@router.message(F.text == "/start")
async def start(message: Message):
    """Команда /start"""

    user_id = message.from_user.id

    if check_admin(user_id):
        await message.answer("👋 Привет, админ!", reply_markup=admin_menu())

    elif check_user_id(user_id):
        await message.answer("👋 Привет, пользователь!", reply_markup=driver_menu())
    else:
        await message.answer("Вас не существует в базе данных!", reply_markup=contact_with_admin_kb())


@router.message(F.text == "📞 Связаться с администратором")
async def contact_with_administrator(message: Message):
    """"Функция для связи с администратором и добавление в Google Sheets"""

    user_id = message.from_user.id
    user_name = message.from_user.full_name or "Без имени"
    username = f"@{message.from_user.username}" if message.from_user.username else "Не указан"

    local_time = message.date.astimezone(ZoneInfo("Europe/Minsk"))
    admin_message = (
        f"📞 Новый запрос на связь от пользователя:\n"
        f"👤 Имя: {user_name}\n"
        f"🆔 ID: {user_id}\n"
        f"📱 Username: {username}\n"
        f"⏰ Время: {local_time.strftime('%d.%m.%Y %H:%M')}"
    )

    token = uuid.uuid4().hex
    save_request(
        token,
        {"user_id": user_id, "user_name": user_name, "username": username}
    )

    admin_id = get_admin_id()

    await message.bot.send_message(
        admin_id,
        admin_message,
        reply_markup=add_driver_inline_kb_with_token(token, user_name)
    )

    await message.answer(
        "✅ Ваше сообщение отправлено администратору!\nОжидайте подключения.",
        reply_markup=wait_button()
    )
