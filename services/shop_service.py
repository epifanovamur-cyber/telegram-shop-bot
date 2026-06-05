from database import (
    get_purchases,
    get_history,
    get_top_products,
    get_all_products,
    get_product_card,
    buy_product_transaction
)


def build_purchase_text(purchases, title, total_text):

    if not purchases:
        return "У вас пока нет покупок"

    text = f"{title}\n\n"
    total = 0

    for index, purchase in enumerate(purchases, start=1):

        product_name = purchase[0]
        price = purchase[1]
        created_at = purchase[2]

        if created_at is None:
            created_at = "Дата неизвестна"

        total += price

        text += (
            f"{index}. {product_name} — {price} ₽\n"
            f"Дата: {created_at}\n\n"
        )

    text += f"{total_text}: {total} ₽"

    return text


# -------------------- История покупок --------------------

def get_purchases_text(user_id):

    purchases = get_purchases(user_id)

    return build_purchase_text(
        purchases,
        "📦 Ваши покупки:",
        "Итого"
    )


# -------------------- История операций --------------------

def get_history_text(user_id):

    history = get_history(user_id)

    return build_purchase_text(
        history,
        "📦 Статистика покупок:",
        "💰 Всего потрачено"
    )


# -------------------- Покупка товара из базы данных --------------------

def buy_database_product_logic(user_id, product_id):

    result = buy_product_transaction(
        user_id=user_id,
        product_id=product_id
    )

    if not result["success"]:
        return result

    return {
        "success": True,
        "message": (
            f"✅ Покупка успешна!\n\n"
            f"Товар: {result['product_name']}\n"
            f"Цена: {result['product_price']} ₽\n"
            f"Баланс: {result['new_balance']} ₽\n"
            f"Осталось: {result['new_stock']} шт."
        )
    }


# -------------------- Топ продуктов --------------------

def get_top_products_text():
    top_products = get_top_products()

    if not top_products:
        return "Покупок ещё не было."

    text = "🏆 Популярные товары\n\n"

    for index, (product_name, count) in enumerate(
            top_products,
            start=1
    ):
        word = get_purchase_word(count)

        text += (
            f"{index}. "
            f"{product_name} - {count} {word}\n"
        )

    return text


# -------------------- Топ продуктов (Хэлпер) --------------------

def get_purchase_word(count):

    if 11 <= count % 100 <= 14:
        return "покупок"

    if count % 10 == 1:
        return "покупка"

    if 2 <= count % 10 <= 4:
        return "покупки"

    return "покупок"


# -------------------- Доступные товары --------------------

def get_available_products():

    products = get_all_products()

    available_products = []

    for product in products:
        stock = product[3]

        if stock > 0:
            available_products.append(product)

    return available_products


# -------------------- Карточка товара --------------------

def get_product_card_logic(product_id):

    product = get_product_card(product_id)

    if product is None:
        return {
            "success": False,
            "message": "❌ Товар не найден"
        }

    product_id, name, description, price, stock, photo_id = product

    if not description:
        description = "Описание пока не добавлено"

    return {
        "success": True,
        "product_id": product_id,
        "name": name,
        "description": description,
        "price": price,
        "stock": stock,
        "photo_id": photo_id,
        "message": (
            f"📦 {name}\n\n"
            f"📝 Описание: {description}\n"
            f"💰 Цена: {price} ₽\n"
            f"📊 Остаток: {stock} шт."
        )
    }