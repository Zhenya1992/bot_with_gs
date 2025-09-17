from aiogram.utils.keyboard import ReplyKeyboardBuilder


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
