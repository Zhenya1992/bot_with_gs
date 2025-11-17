from aiogram.types import Message
from aiogram import F, Router
from keyboards.reply_kb import driver_menu, admin_menu, button_get_id, contact_with_admin_kb, welcome_button
from utils.auth import check_admin, check_driver, get_admin_id, check_user_id
from zoneinfo import ZoneInfo

router = Router()


@router.message(F.text == "/start")
async def start(message: Message):
    """Команда /start"""

    await message.answer(text="👋 Здравствуйте,\nПройдите верификацию, для работы с ботом.",
                         reply_markup=welcome_button())


@router.message(F.text == "👋 Привет")
async def greetings(message: Message):
    """Функция приветствия"""

    user_id = message.from_user.id
    if check_user_id(user_id):
        await message.answer("👋 Привет, пользователь!", reply_markup=driver_menu())
    else:
        await message.answer("Вас не существует в базе данных!", reply_markup=contact_with_admin_kb())


@router.message(F.text == "🔍 Получить ID")
async def get_id(message: Message):
    user_id = message.from_user.id
    if check_admin(user_id):
        await message.answer("👋 Привет, админ!", reply_markup=admin_menu())

    elif check_driver(user_id):
        await message.answer("👋 Привет, водитель!", reply_markup=driver_menu())
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
        await message.answer("✅ Ваше сообщение отправлено администратору!\nОжидайте подключения.",
                             reply_markup=button_get_id())

    except Exception as e:
        return print(f"Error{e}")