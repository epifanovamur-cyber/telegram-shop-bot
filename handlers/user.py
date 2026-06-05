from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from services.user_service import (
    get_profile_text,
    get_balance_text
)

from services.shop_service import get_available_products

from keyboards import get_shop_keyboard


# -------------------- Роутер пользователя --------------------

router = Router()


# -------------------- Профиль --------------------

async def show_profile(message: Message, user_id: int):
    text = get_profile_text(user_id)
    await message.answer(text)


@router.message(Command("profile"))
async def profile_command(message: Message, user_id: int):
    await show_profile(message, user_id)


@router.message(lambda message: message.text == "👤 Профиль")
async def profile_button(message: Message, user_id: int):
    await show_profile(message, user_id)


# -------------------- Баланс --------------------

@router.message(Command("balance"))
async def balance_command(message: Message, user_id: int):
    text = get_balance_text(user_id)
    await message.answer(text)


@router.message(lambda message: message.text == "💰 Баланс")
async def balance_button(message: Message, user_id: int):
    text = get_balance_text(user_id)
    await message.answer(text)


# -------------------- Магазин --------------------

async def show_shop(message: Message):

    products = get_available_products()

    if not products:
        await message.answer("🛒 В магазине пока нет доступных товаров")
        return

    await message.answer(
        "🛒 Добро пожаловать в магазин!",
        reply_markup=get_shop_keyboard(products)
    )


@router.message(Command("shop"))
async def shop_command(message: Message):
    await show_shop(message)


@router.message(lambda message: message.text == "🛒 Магазин")
async def shop_button(message: Message):
    await show_shop(message)


