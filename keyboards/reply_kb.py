from aiogram.utils.keyboard import ReplyKeyboardBuilder, ReplyKeyboardMarkup
from aiogram.types import KeyboardButton


def welcome_button():
    """Кнопка приветствия"""

    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="👋 Привет")]], resize_keyboard=True
        )

def button_get_id():
    """Кнопка для получения id"""

    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="🔍 Получить ID")]], resize_keyboard=True
    )

def contact_with_admin_kb():
    """Кнопка для связи с администратором"""

    builder = ReplyKeyboardBuilder()
    builder.button(text="📞 Связаться с администратором")
    builder.adjust(1)
    return builder.as_markup(resize_keyboard=True)

def driver_menu():
    """Основная клавиатура для водителя"""

    builder = ReplyKeyboardBuilder()
    builder.button(text="Расход ➖")
    builder.button(text="Доход ➕")
    builder.button(text="Отчёт 📊")
    builder.adjust(1, 1, 1)
    return builder.as_markup(resize_keyboard=True)


def admin_menu():
    """Основная клавиатура для администратора"""

    builder = ReplyKeyboardBuilder()
    builder.button(text="Сводный отчёт 📈")
    builder.button(text="Выгрузка ⬇️")
    builder.button(text="Добавить водителя ✅")
    builder.button(text="Удалить водителя ❌")
    builder.button(text="Назад ◀️")
    builder.adjust(1, 1, 2, 1)
    return builder.as_markup(resize_keyboard=True)


def back_button_kb():
    """клавиатура для шага назад"""

    builder = ReplyKeyboardBuilder()
    builder.button(text="Назад ⬅️")
    return builder.as_markup(resize_keyboard=True)


def reply_income_menu():
    """клавиатура для оплаты заказа"""

    builder = ReplyKeyboardBuilder()
    builder.button(text="Оплата за заказ 💰")
    builder.button(text="Доплата по заказу 🫰")
    builder.button(text="⬅️ Назад")
    builder.adjust(2, 1)
    return builder.as_markup(resize_keyboard=True)

def report_menu_driver_kb():
    """Клавиатура для отчёта для водителя"""

    builder = ReplyKeyboardBuilder()
    builder.button(text="Текущий день ☀️")
    builder.button(text="Текущий месяц 📅")
    builder.button(text="⬅️ Назад")
    builder.adjust(1, 1, 1)
    return builder.as_markup(resize_keyboard=True)

def report_menu_admin_kb():
    """Клавиатура для отчёта администратора"""

    builder = ReplyKeyboardBuilder()
    builder.button(text="Сегодня 🕛")
    builder.button(text="Текущий месяц 🈷️")
    builder.button(text="За всё время 🗓️")
    builder.button(text="Назад ◀️")
    builder.adjust(2, 1, 1)
    return builder.as_markup(resize_keyboard=True)