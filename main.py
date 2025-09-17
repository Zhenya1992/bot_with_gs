import asyncio
from aiogram import Bot, Dispatcher
from config import TOKEN
from handlers import router
import logging

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
dp = Dispatcher()


async def main():
    """Корутина для запуска бота"""

    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
