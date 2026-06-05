from aiogram import Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command

from services.shop_service import (
    get_purchases_text,
    get_history_text,
    buy_database_product_logic,
    get_top_products_text,
    get_product_card_logic,
    get_available_products
)

from services.user_service import get_balance_value

from keyboards import get_product_card_keyboard, get_shop_keyboard

# -------------------- Роутер магазина --------------------

router = Router()


# -------------------- Карточка товара --------------------

@router.callback_query(lambda callback: callback.data and callback.data.startswith("product_card_"))
async def product_card(callback: CallbackQuery):

    message = callback.message
    data = callback.data

    if message is None:
        await callback.answer()
        return

    if data is None:
        await callback.answer()
        return

    product_id_text = data.replace("product_card_", "")

    if not product_id_text.isdigit():
        await message.answer("❌ Некорректный товар")
        await callback.answer()
        return

    product_id = int(product_id_text)

    result = get_product_card_logic(product_id)

    if not result["success"]:
        await message.answer(result["message"])
        await callback.answer()
        return

    keyboard = get_product_card_keyboard(product_id)

    if result["photo_id"]:
        await message.answer_photo(
            photo=result["photo_id"],
            caption=result["message"],
            reply_markup=keyboard
        )
    else:
        await message.answer(
            result["message"],
            reply_markup=keyboard
        )

    await callback.answer()


# -------------------- Назад в магазин --------------------

@router.callback_query(lambda callback: callback.data == "back_to_shop")
async def back_to_shop(callback: CallbackQuery):

    message = callback.message

    if message is None:
        await callback.answer()
        return

    products = get_available_products()

    if not products:
        await message.answer("🛒 В магазине пока нет доступных товаров")
        await callback.answer()
        return

    await message.answer(
        "🛒 Добро пожаловать в магазин!",
        reply_markup=get_shop_keyboard(products)
    )

    await callback.answer()

# -------------------- Покупка товара --------------------

@router.callback_query(lambda callback: callback.data and callback.data.startswith("buy_product_"))
async def buy_database_product(callback: CallbackQuery, user_id: int):

    message = callback.message
    data = callback.data

    if message is None:
        await callback.answer()
        return

    if data is None:
        await callback.answer()
        return

    product_id_text = data.replace("buy_product_", "")

    if not product_id_text.isdigit():
        await message.answer("❌ Некорректный товар")
        await callback.answer()
        return

    product_id = int(product_id_text)

    result = buy_database_product_logic(
        user_id=user_id,
        product_id=product_id
    )

    if not result["success"]:
        await message.answer(result["message"])
        await callback.answer()
        return

    await message.answer(result["message"])

    await callback.answer()

# -------------------- Проверка баланса из inline-кнопки --------------------

@router.callback_query(lambda callback: callback.data == "check_balance")
async def check_balance(callback: CallbackQuery, user_id: int):

    message = callback.message

    if message is None:
        await callback.answer()
        return

    user_balance = get_balance_value(user_id)

    await callback.message.answer(
        f"💰 Ваш баланс: {user_balance} ₽"
    )

    await callback.answer()


# -------------------- История покупок --------------------

@router.message(lambda message: message.text == "📦 Мои покупки")
async def my_purchases(message: Message, user_id: int):

    text = get_purchases_text(user_id)

    await message.answer(text)


# -------------------- История операций --------------------

@router.message(Command("history"))
async def show_history(message: Message, user_id: int):

    text = get_history_text(user_id)

    await message.answer(text)


# -------------------- Топ товаров --------------------

@router.message(Command("top_products"))
async def top_products_command(message: Message):
    text = get_top_products_text()
    await message.answer(text)


@router.message(lambda message: message.text == "🏆 Топ товаров")
async def top_products_button(message: Message):

    text = get_top_products_text()

    await message.answer(text)



