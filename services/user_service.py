from database import (
    add_user,
    get_balance,
    get_total_spent,
    get_user_purchases_count
)


# -------------------- Профиль пользователя --------------------

def get_profile_text(user_id):

    balance = get_balance(user_id)

    purchases_count = get_user_purchases_count(user_id)

    total_spent = get_total_spent(user_id)

    return (
        f"👤 Профиль покупателя\n\n"
        f"🆔 Telegram ID: {user_id}\n"
        f"💰 Баланс: {balance} ₽\n"
        f"📦 Покупок: {purchases_count}\n"
        f"🛒 Всего потрачено: {total_spent} ₽"
    )


# -------------------- Баланс --------------------

def get_balance_text(user_id):

    balance = get_balance(user_id)

    return f"💰 Ваш баланс: {balance} ₽"


def get_balance_value(user_id):

    return get_balance(user_id)


# -------------------- Регистрация пользователя --------------------

def register_user(user_id):

    add_user(user_id)

    return {
        "success": True,
        "message": (
            "👋 Добро пожаловать в мини-магазин!\n\n"
            "Нажмите кнопки ниже или используйте команды:\n\n"
            "/help — список всех команд\n"
            "/profile — профиль покупателя\n"
            "/balance — баланс\n"
            "/shop — магазин\n"
            "/history — история покупок\n"
            "/top_products — популярные товары\n"
        )
    }


# -------------------- Помощь пользователю --------------------

def get_user_help_text():

    return (
        "🛒 Помощь по магазину\n\n"

        "📌 Основные команды:\n"
        "/start — открыть главное меню\n"
        "/help — помощь по магазину\n"
        "/myid — узнать свой Telegram ID\n"
        "/profile — профиль покупателя\n"
        "/balance — посмотреть баланс\n"
        "/shop — открыть магазин\n"
        "/history — история покупок\n"
        "/top_products — популярные товары\n\n"

        "🔘 Кнопки меню:\n"
        "💰 Баланс — посмотреть текущий баланс\n"
        "🛒 Магазин — открыть каталог товаров\n"
        "📦 Мои покупки — посмотреть историю покупок\n"
        "👤 Профиль — профиль покупателя\n"
        "🏆 Топ товаров — популярные товары\n\n"

        "🛍 Как купить товар:\n"
        "1. Откройте 🛒 Магазин\n"
        "2. Выберите товар\n"
        "3. Посмотрите карточку товара\n"
        "4. Нажмите 🛒 Купить\n\n"

        "Если на балансе недостаточно средств, обратитесь к администратору."
    )
