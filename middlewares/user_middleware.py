from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery


# -------------------- User Middleware --------------------

class UserMiddleware(BaseMiddleware):

    async def __call__(self, handler, event, data: dict):

        if isinstance(event, Message):

            user = event.from_user

        elif isinstance(event, CallbackQuery):

            user = event.from_user

        else:

            return await handler(event, data)

        if user:

            data["user_id"] = user.id

            data["username"] = user.username

        return await handler(event, data)