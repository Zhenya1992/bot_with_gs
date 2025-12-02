from aiogram.types import Message
from aiogram.filters import Command
from aiogram import Router
from utils.payments import create_payment
from keyboards.inline_kb import pay_button_kb

router = Router()


@router.message(Command("pay"))
async def pay_command(message: Message):
    """Обработчик оплаты"""

    user_id = message.from_user.id
    username = message.from_user.username or message.from_user.full_name or "Unknown"
    amount = 100.0
    description = f"Оплата подписки от @{username}, ID: {user_id}"

    try:
        confirmation_url, payment_id = await create_payment(amount, description, user_id, username)
    except Exception as e:
        print(f"Ошибка при создании платежа: {e}")
        return

    kb = pay_button_kb(amount, confirmation_url)
    await message.answer(
        f"Платеж на {amount} руб. создан. Подтвердите оплату:",
        reply_markup=kb,
        parse_mode="Markdown"
    )