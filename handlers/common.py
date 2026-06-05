from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

from services.user_service import register_user, get_user_help_text

from keyboards import main_keyboard


# -------------------- Роутер общих команд --------------------

router = Router()


# -------------------- Telegram ID --------------------

@router.message(Command("myid"))
async def my_id_command(message: Message):

    user = message.from_user

    if user is None:
        await message.answer("Не удалось определить пользователя")
        return

    await message.answer(
        f"Ваш Telegram ID: {user.id}"
    )


# -------------------- Команда /start --------------------

@router.message(CommandStart())
async def start(message: Message):

    user = message.from_user

    if user is None:
        await message.answer("Не удалось определить пользователя")
        return

    result = register_user(user.id)

    await message.answer(
        result["message"],
        reply_markup=main_keyboard
    )


# -------------------- Команда /help --------------------

@router.message(Command("help"))
async def help_command(message: Message):

    text = get_user_help_text()

    await message.answer(text)