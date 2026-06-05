from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)


# -------------------- Клавиатура магазина --------------------

def get_shop_keyboard(products):

    buttons = []

    for product_id, name, price, stock in products:

        buttons.append([
            InlineKeyboardButton(
                text=f"{name} - {price} ₽",
                callback_data=f"product_card_{product_id}"
            )
        ])

    buttons.append([
        InlineKeyboardButton(
            text="💰 Проверить баланс",
            callback_data="check_balance"
        )
    ])

    return InlineKeyboardMarkup(inline_keyboard=buttons)

# -------------------- Клавиатура отмены --------------------

cancel_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="❌ Отмена")
        ]
    ],
    resize_keyboard=True
)


# -------------------- Главное меню --------------------

main_keyboard = ReplyKeyboardMarkup(
    keyboard=[

        [
            KeyboardButton(text="💰 Баланс"),
            KeyboardButton(text="🛒 Магазин")
        ],

        [
            KeyboardButton(text="📦 Мои покупки"),
            KeyboardButton(text="👤 Профиль")
        ],

        [
            KeyboardButton(text="🏆 Топ товаров")
        ]

    ],
    resize_keyboard=True
)


# -------------------- Клавиатура карточки товара --------------------

def get_product_card_keyboard(product_id):

    buttons = [
        [
            InlineKeyboardButton(
                text="🛒 Купить",
                callback_data=f"buy_product_{product_id}"
            )
        ],
        [
            InlineKeyboardButton(
                text="⬅️ Назад в магазин",
                callback_data="back_to_shop"
            )
        ]
    ]

    return InlineKeyboardMarkup(inline_keyboard=buttons)