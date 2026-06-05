from aiogram.filters import BaseFilter
from aiogram.types import Message

from config import ADMIN_ID


# -------------------- Фильтр администратора --------------------

class AdminFilter(BaseFilter):

    async def __call__(self, message: Message):

        user = message.from_user

        if user is None:
            return False

        return user.id == ADMIN_ID