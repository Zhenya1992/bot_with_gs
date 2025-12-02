from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def add_driver_inline_kb_with_token(token: str, driver_name: str):
    """Функция добавления водителя с помощью инлайн-клавиатуры."""

    callback_data = f"add_driver:{token}"
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=f"➕ Добавить водителя ({driver_name})",
                    callback_data=callback_data
                )
            ]
        ]
    )

def pay_button_kb(amount: float, url: str):
    """Кнопка оплаты"""

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=f"💳 Произвести оплату {amount} byn",
                    url=url
                )
            ]
        ]
    )