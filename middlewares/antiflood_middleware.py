import time

from aiogram import BaseMiddleware
from aiogram.types import Message


# -------------------- AntiFlood Middleware --------------------

class AntiFloodMiddleware(BaseMiddleware):

    def __init__(self, limit: float = 1.0):

        self.limit = limit

        self.users = {}


    async def __call__(self, handler, event: Message, data: dict):

        user = event.from_user

        if user is None:
            return await handler(event, data)

        now = time.time()

        last_time = self.users.get(user.id, 0)

        if now - last_time < self.limit:

            await event.answer("⏳ Не так быстро")

            return None

        self.users[user.id] = now

        return await handler(event, data)