import asyncio
import logging
from aiogram import Bot, Dispatcher
from config import BOT_TOKEN

from handlers.admin_handlers.admin_main_handlers import admin_main_router
from handlers.admin_handlers.categories_handlers import admin_categories_router
from handlers.admin_handlers.car_brands_handlers import admin_car_brands_router
"""from handlers.admin_edit import router as admin_edit_router"""
from handlers.client import router as client_router
from handlers.common import router as common_router
from handlers.start import router as start_router

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s | %(levelname)s | %(message)s")

# создаём объекты глобально (удобно для декораторов)
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# регистрируем роутеры
"""dp.include_router(admin_edit_router)"""
dp.include_router(start_router)           # /start
dp.include_router(admin_main_router)      # главное меню админа
dp.include_router(admin_categories_router)# категории
dp.include_router(admin_car_brands_router)       # бренды машин


dp.include_router(client_router)          # клиент
dp.include_router(common_router)          # общие команды

async def main():
    try:
        logging.info("Запуск polling...")
        await dp.start_polling(bot)  # блокирующая функция
    except Exception as e:
        logging.exception("Ошибка при polling:")
    finally:
        # обязательно корректно закрываем сессию, чтобы не оставлять соединения висеть
        await bot.session.close()
        logging.info("Сессия бота закрыта. Выход.")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("Stop by user (KeyboardInterrupt)")
