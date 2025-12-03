import asyncio
from aiogram import Bot, Dispatcher
from config import TOKEN
import logging
from handlers.driver import h1_expense, h2_income, h3_report
from handlers import start, h_payment
from handlers.admin import h0_back_to_admin_menu, h1_add_drivers, h2_remove_drivers, h3_summary, h4_export
from services.google_sheets import update_drivers_in_config
from middlewares.check_driver import DriverAccessMiddleware


logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
dp = Dispatcher()

dp.message.middleware(DriverAccessMiddleware())
dp.callback_query.middleware(DriverAccessMiddleware())

dp.include_router(start.router)
dp.include_router(h1_expense.router)
dp.include_router(h2_income.router)
dp.include_router(h3_report.router)
dp.include_router(h0_back_to_admin_menu.router)
dp.include_router(h1_add_drivers.router)
dp.include_router(h2_remove_drivers.router)
dp.include_router(h3_summary.router)
dp.include_router(h4_export.router)
dp.include_router(h_payment.router)

async def main():
    """Корутина для запуска бота"""

    drivers = update_drivers_in_config()
    print(f"🚗 Загружено {len(drivers)} водителей при запуске: {drivers}")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())