from aiogram import BaseMiddleware
import config
from typing import Any, Dict, Callable, Awaitable


class DriverAccessMiddleware(BaseMiddleware):
    """Класс для проверки доступа к боту"""

    async def __call__(
            self,
            handler: Callable[[Any, Dict[str, Any]], Awaitable[Any]],
            event,
            data: Dict[str, Any]
    ) -> Any:

        user_id = None
        if hasattr(event, 'from_user'):
            user_id = event.from_user.id
        elif hasattr(event, 'message') and hasattr(event.message, 'from_user'):
            user_id = event.message.from_user.id

        if not user_id:
            return await handler(event, data)

        is_allowed_command = False

        if hasattr(event, 'text') and event.text:
            text = event.text.strip()

            if text.startswith('/start'):
                is_allowed_command = True
            elif text == "📞 Связаться с администратором":
                is_allowed_command = True
            elif text == "Ожидание связи от администратора 🕒 ...":
                is_allowed_command = True

        if is_allowed_command:
            return await handler(event, data)

        if user_id == config.MANAGER_ID:
            return await handler(event, data)

        if user_id not in config.DRIVERS:
            try:
                if hasattr(event, 'answer'):
                    await event.answer("Вы не являетесь водителем, сдайте на права!")
                elif hasattr(event, 'message') and hasattr(event.message, 'answer'):
                    await event.message.answer("Вы не являетесь водителем, сдайте на права!")
            except:
                pass
            return

        return await handler(event, data)