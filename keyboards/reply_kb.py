from aiogram.utils.keyboard import ReplyKeyboardBuilder, ReplyKeyboardMarkup
from aiogram.types import KeyboardButton


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

def drive_menu():
    """Основная клавиатура для водителя"""

    builder = ReplyKeyboardBuilder()
    builder.button(text="Расход")
    builder.button(text="Доход")
    builder.button(text="Отчёт")
    builder.adjust(1, 1, 1)
    return builder.as_markup(resize_keyboard=True)


def admin_menu():
    """Основная клавиатура для администратора"""

    builder = ReplyKeyboardBuilder()
    builder.button(text="Отчёт")
    builder.button(text="Выгрузка")
    builder.button(text="Добавить водителя")
    builder.button(text="Удалить водителя")
    builder.button(text="Назад")
    builder.adjust(1, 1, 2, 1)
    return builder.as_markup(resize_keyboard=True)


def back_button_kb():
    """Клавиатура для кнопки назад"""

    builder = ReplyKeyboardBuilder()
    builder.button(text="🔙 Назад")
    return builder.as_markup(resize_keyboard=True)
