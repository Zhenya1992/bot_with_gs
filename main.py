import asyncio
from aiogram import Bot, Dispatcher
from config import TOKEN
# from handlers import router
import logging
from handlers.driver import h1_expense, h2_income, h3_report
from handlers import start
from handlers.admin import h0_back_to_admin_menu

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
dp = Dispatcher()
dp.include_router(start.router)
dp.include_router(h1_expense.router)
dp.include_router(h2_income.router)
dp.include_router(h3_report.router)
dp.include_router(h0_back_to_admin_menu.router)


async def main():
    """Корутина для запуска бота"""

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
