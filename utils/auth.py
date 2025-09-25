from config import MANAGER_ID, DRIVERS


def check_admin(user_id: int):
    """Проверка, является ли пользователь администратором."""

    return user_id == MANAGER_ID


def check_driver(user_id: int):
    """Проверка, является ли пользователь водителем."""

    return user_id in DRIVERS

def get_admin_id():
    """Получение ID администратора."""

    return MANAGER_ID