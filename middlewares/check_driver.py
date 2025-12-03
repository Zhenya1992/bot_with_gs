from aiogram import BaseMiddleware
import config
from typing import Any, Dict, Union, Callable, Awaitable


class DriverAccessMiddleware(BaseMiddleware):
    """Класс для проверки доступа к боту"""

    async def __call__(
        self,
        handler: Callable[[Any, Dict[str, Any]], Awaitable[Any]],
        event,
        data: Dict[str, Any]
    ) -> Any:

        user_id = event.from_user.id if hasattr(event, 'from_user') else None
        if user_id and user_id not in config.DRIVERS:
            await event.answer("Вы не являетесь водителем, сдайте на права!")
            return

        return await handler(event, data)