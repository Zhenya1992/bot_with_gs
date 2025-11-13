from aiogram.types import Message
from aiogram import F, Router
from keyboards.reply_kb import drive_menu, admin_menu, button_get_id, contact_with_admin_kb
from utils.auth import check_admin, check_driver, get_admin_id
from zoneinfo import ZoneInfo

router = Router()


@router.message(F.text == "/start")
async def start(message: Message):
    """Команда /start"""

    await message.answer(text="👋 Привет,\nПолучите ваш ID", reply_markup=button_get_id())


@router.message(F.text == "🔍 Получить ID")
async def get_id(message: Message):
    user_id = message.from_user.id
    if check_admin(user_id):
        await message.answer("👋 Привет, админ!", reply_markup=admin_menu())

    elif check_driver(user_id):
        await message.answer("👋 Привет, водитель!", reply_markup=drive_menu())
    else:
        tg_id = message.from_user.id
        await message.answer(
            f"Ваш ID: `{tg_id}`\nДля работы с ботом нажмите на кнопку ниже",
            reply_markup=contact_with_admin_kb(),
            parse_mode="Markdown",)


@router.message(F.text == "📞 Связаться с администратором")
async def contact_with_administrator(message: Message):
    """Обработчик кнопки связаться с администратором"""

    user_id = message.from_user.id
    user_name = message.from_user.full_name
    username = f"@{message.from_user.username}" if message.from_user.username else "Не указан"

    local_time = message.date.astimezone(ZoneInfo("Europe/Minsk"))
    admin_message = (
        f"📞 Новый запрос на связь от пользователя:\n"
        f"👤 Имя: {user_name}\n"
        f"🆔 ID: {user_id}\n"
        f"📱 Username: {username}\n"
        f"⏰ Время: {local_time.strftime('%d.%m.%Y %H:%M')}"
    )

    admin_id = get_admin_id()
    try:
        await message.bot.send_message(admin_id, admin_message)
        await message.answer("✅ Ваше сообщение отправлено администратору!\nОжидайте подключения.")

    except Exception as e:
        return print(f"Error{e}")