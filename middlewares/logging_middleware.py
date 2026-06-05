from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery


# -------------------- Logging Middleware --------------------

class LoggingMiddleware(BaseMiddleware):

    async def __call__(self, handler, event, data: dict):

        if isinstance(event, Message):

            user = event.from_user

            text = event.text

            if user:

                print(
                    f"Пользователь {user.id} "
                    f"отправил сообщение: {text}"
                )

        elif isinstance(event, CallbackQuery):

            user = event.from_user

            callback_data = event.data

            if user:

                print(
                    f"Пользователь {user.id} "
                    f"нажал inline-кнопку: {callback_data}"
                )

        return await handler(event, data)