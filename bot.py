import asyncio  # async-библиотека Python

from aiogram import Bot, Dispatcher  # основные классы aiogram

from config import BOT_TOKEN  # токен бота


# -------------------- Роутеры --------------------

from handlers.common import router as common_router  # /start, /help
from handlers.user import router as user_router  # профиль, баланс
from handlers.shop import router as shop_router  # магазин
from handlers.admin import router as admin_router  # админ-команды


# -------------------- Middlewares --------------------

from middlewares.logging_middleware import LoggingMiddleware  # логирование
from middlewares.antiflood_middleware import AntiFloodMiddleware  # антифлуд
from middlewares.user_middleware import UserMiddleware  # user_id


# -------------------- Создание бота --------------------

bot = Bot(token=BOT_TOKEN)  # создаём бота

dp = Dispatcher()  # создаём диспетчер


# -------------------- Главная async-функция --------------------

async def main():

    # ---------- Middlewares для сообщений ----------

    dp.message.middleware(LoggingMiddleware())  # логирование

    dp.message.middleware(
        AntiFloodMiddleware(limit=1.0)
    )  # антифлуд

    dp.message.middleware(
        UserMiddleware()
    )  # добавление user_id


    # ---------- Middlewares для callback ----------

    dp.callback_query.middleware(
        AntiFloodMiddleware(limit=1.0)
    )

    dp.callback_query.middleware(
        LoggingMiddleware()
    )

    dp.callback_query.middleware(
        UserMiddleware()
    )


    # -------------------- Роутеры --------------------

    dp.include_router(common_router)

    dp.include_router(user_router)

    dp.include_router(shop_router)

    dp.include_router(admin_router)


    # -------------------- Запуск бота --------------------

    await dp.start_polling(bot)


# -------------------- Запуск файла --------------------

if __name__ == "__main__":

    asyncio.run(main())