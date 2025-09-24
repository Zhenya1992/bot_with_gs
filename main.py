import asyncio
from aiogram import Bot, Dispatcher
from config import TOKEN
# from handlers import router
import logging
from handlers.driver import h1_expense
from handlers import start

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
dp = Dispatcher()
dp.include_router(start.router)
dp.include_router(h1_expense.router)


async def main():
    """Корутина для запуска бота"""

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
