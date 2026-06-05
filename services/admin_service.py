from database import (
    get_balance,
    get_all_users,
    add_product,
    archive_product,
    get_product_buy_id,
    get_product_by_id,
    restore_product,
    get_all_products_for_admin,
    restock_product,
    update_product_price,
    update_product_name,
    update_product_description,
    update_product_photo,
    get_users_count,
    get_products_count_by_status,
    get_purchases_count,
    get_total_revenue,
    get_active_stock_sum,
    get_user_balance_transactions,
    get_total_spent,
    get_user_purchases_count,
    user_exists,
    add_balance_transaction_logic
)


# -------------------- Пополнение баланса --------------------

def add_balance_to_user(user_id, amount):

    if amount <= 0:
        return {
            "success": False,
            "message": "❌ Сумма должна быть больше 0"
        }

    result = add_balance_transaction_logic(
        user_id=user_id,
        amount=amount
    )

    if not result["success"]:
        return result

    return {
        "success": True,
        "message": (
            f"✅ Баланс пополнен\n"
            f"Пользователь: {user_id}\n"
            f"Сумма: {amount} ₽\n"
            f"Новый баланс: {result['new_balance']} ₽"
        ),
        "new_balance": result["new_balance"]
    }


# -------------------- Просмотр профиля пользователя --------------------

def get_user_profile_text(user_id):

    if not user_exists(user_id):
        return "❌ Пользователь не найден"

    balance = get_balance(user_id)

    purchases_count = get_user_purchases_count(user_id)

    total_spent = get_total_spent(user_id)

    return (
        f"👤 Пользователь магазина\n\n"
        f"🆔 Telegram ID: {user_id}\n"
        f"💰 Баланс: {balance} ₽\n"
        f"📦 Покупок: {purchases_count}\n"
        f"🛒 Всего потрачено: {total_spent} ₽"
    )


# -------------------- Список пользователей --------------------

def get_all_users_text():

    users = get_all_users()

    if not users:
        return "Пользователей нет"

    text = "👥 Пользователи:\n\n"

    for user_id, balance in users:

        purchases_count = get_user_purchases_count(user_id)

        total_spent = get_total_spent(user_id)

        text += (
            f"ID: {user_id}\n"
            f"Баланс: {balance} ₽\n"
            f"Покупок: {purchases_count}\n"
            f"Потрачено: {total_spent} ₽\n\n"
        )

    return text


# -------------------- Добавление товара --------------------

def add_product_logic(name, description, price, stock, photo_id=None):

    add_product(
        name=name,
        price=price,
        stock=stock,
        description=description,
        photo_id=photo_id
    )

    photo_text = "✅ Фото добавлено" if photo_id else "Без фото"

    return {
        "success": True,
        "message": (
            f"✅ Товар добавлен:\n"
            f"Название: {name}\n"
            f"Описание: {description}\n"
            f"Цена: {price} ₽\n"
            f"Количество: {stock} шт.\n"
            f"Фото: {photo_text}"
        )
    }


# -------------------- Архивация товара --------------------

def delete_product_logic(product_id):

    product = get_product_buy_id(product_id)

    if product is None:
        return {
            "success": False,
            "message": "❌ Товар не найден"
        }

    product_id, product_name, product_price, product_stock = product

    archive_product(product_id)

    return {
        "success": True,
        "message": (
            f"📦 Товар отправлен в архив\n"
            f"ID: {product_id}\n"
            f"Название: {product_name}"
        )
    }


# -------------------- Восстановление товара из архива --------------------

def restore_product_logic(product_id):

    product = get_product_by_id(product_id)

    if product is None:
        return {
            "success": False,
            "message": "❌ Товар не найден"
        }

    product_id, product_name, product_price, product_stock, status = product

    if status == "active":
        return {
            "success": False,
            "message": (
                f"ℹ️ Товар уже активен\n"
                f"ID: {product_id}\n"
                f"Название: {product_name}"
            )
        }

    restore_product(product_id)

    if product_stock <= 0:
        stock_text = "\n\n⚠️ Внимание: остаток товара 0 шт. Сделайте restock."
    else:
        stock_text = ""

    return {
        "success": True,
        "message": (
            f"✅ Товар восстановлен из архива\n"
            f"ID: {product_id}\n"
            f"Название: {product_name}\n"
            f"Остаток: {product_stock} шт."
            f"{stock_text}"
        )
    }


# -------------------- Список товаров для админа --------------------

def get_products_admin_text():

    products = get_all_products_for_admin()

    if not products:
        return "Товаров пока нет"

    text = "📦 Список товаров:\n\n"

    for product in products:
        product_id, name, price, stock, status = product

        text += (
            f"ID: {product_id}\n"
            f"Название: {name}\n"
            f"Цена: {price} ₽\n"
            f"Остаток: {stock} шт.\n"
            f"Статус: {status}\n\n"
        )

    return text


# -------------------- Пополнение остатка товара --------------------

def restock_product_logic(product_id, amount):

    if amount <= 0:
        return {
            "success": False,
            "message": "❌ Количество должно быть больше 0"
        }

    product = get_product_by_id(product_id)

    if product is None:
        return {
            "success": False,
            "message": "❌ Товар не найден"
        }

    product_id, product_name, product_price, product_stock, status = product

    restock_product(product_id, amount)

    new_stock = product_stock + amount

    return {
        "success": True,
        "message": (
            f"✅ Остаток товара пополнен\n"
            f"ID: {product_id}\n"
            f"Название: {product_name}\n"
            f"Было: {product_stock} шт.\n"
            f"Добавлено: {amount} шт.\n"
            f"Стало: {new_stock} шт.\n"
            f"Статус: {status}"
        )
    }


# -------------------- Изменение цены товара --------------------

def edit_product_price_logic(product_id, new_price):

    if new_price <= 0:
        return {
            "success": False,
            "message": "❌ Цена должна быть больше 0"
        }

    product = get_product_by_id(product_id)

    if product is None:
        return {
            "success": False,
            "message": "❌ Товар не найден"
        }

    product_id, product_name, old_price, product_stock, status = product

    update_product_price(product_id, new_price)

    return {
        "success": True,
        "message": (
            f"✅ Цена товара изменена\n"
            f"ID: {product_id}\n"
            f"Название: {product_name}\n"
            f"Старая цена: {old_price} ₽\n"
            f"Новая цена: {new_price} ₽\n"
            f"Статус: {status}"
        )
    }


# -------------------- Изменение названия товара --------------------

def edit_product_name_logic(product_id, new_name):

    new_name = new_name.strip()

    if not new_name:
        return {
            "success": False,
            "message": "❌ Название не может быть пустым"
        }

    product = get_product_by_id(product_id)

    if product is None:
        return {
            "success": False,
            "message": "❌ Товар не найден"
        }

    product_id, old_name, product_price, product_stock, status = product

    update_product_name(product_id, new_name)

    return {
        "success": True,
        "message": (
            f"✅ Название товара изменено\n"
            f"ID: {product_id}\n"
            f"Старое название: {old_name}\n"
            f"Новое название: {new_name}\n"
            f"Статус: {status}"
        )
    }


# -------------------- Изменение описания товара --------------------

def edit_product_description_logic(product_id, new_description):

    new_description = new_description.strip()

    if not new_description:
        return {
            "success": False,
            "message": "❌ Описание не может быть пустым"
        }

    product = get_product_by_id(product_id)

    if product is None:
        return {
            "success": False,
            "message": "❌ Товар не найден"
        }

    product_id, product_name, product_price, product_stock, status = product

    update_product_description(product_id, new_description)

    return {
        "success": True,
        "message": (
            f"✅ Описание товара изменено\n"
            f"ID: {product_id}\n"
            f"Название: {product_name}\n"
            f"Новое описание: {new_description}\n"
            f"Статус: {status}"
        )
    }


# -------------------- Старт изменения фото товара --------------------

def start_edit_product_photo_logic(product_id):

    product = get_product_by_id(product_id)

    if product is None:
        return {
            "success": False,
            "message": "❌ Товар не найден"
        }

    product_id, product_name, product_price, product_stock, status = product

    return {
        "success": True,
        "message": (
            f"📸 Изменение фото товара\n\n"
            f"ID: {product_id}\n"
            f"Название: {product_name}\n\n"
            f"Отправьте новое фото товара или напишите: удалить"
        )
    }


# -------------------- Сохранение фото товара --------------------

def edit_product_photo_logic(product_id, photo_id):

    product = get_product_by_id(product_id)

    if product is None:
        return {
            "success": False,
            "message": "❌ Товар не найден"
        }

    product_id, product_name, product_price, product_stock, status = product

    update_product_photo(product_id, photo_id)

    photo_text = "✅ Фото обновлено" if photo_id else "🗑 Фото удалено"

    return {
        "success": True,
        "message": (
            f"{photo_text}\n"
            f"ID: {product_id}\n"
            f"Название: {product_name}"
        )
    }


# -------------------- Статистика магазина --------------------

def get_shop_stats_text():

    users_count = get_users_count()

    active_products_count = get_products_count_by_status("active")

    archived_products_count = get_products_count_by_status("archived")

    purchases_count = get_purchases_count()

    total_revenue = get_total_revenue()

    active_stock_sum = get_active_stock_sum()

    return (
        f"📊 Статистика магазина\n\n"
        f"👥 Пользователей: {users_count}\n"
        f"📦 Активных товаров: {active_products_count}\n"
        f"🗄 Архивных товаров: {archived_products_count}\n"
        f"🛒 Покупок: {purchases_count}\n"
        f"💰 Выручка: {total_revenue} ₽\n"
        f"📊 Остаток активных товаров: {active_stock_sum} шт."
    )


# -------------------- Помощь администратору --------------------

def get_admin_help_text():

    return (
        "🛠 Админ-панель магазина\n\n"

        "👥 Пользователи:\n"
        "/users — список всех пользователей\n"
        "/user user_id — профиль пользователя\n"
        "/add_balance user_id amount — пополнить баланс пользователю\n"
        "/transactions user_id — финансовые операции пользователя\n\n"

        "📦 Товары:\n"
        "/products — список всех товаров с ID\n"
        "/add_product — добавить новый товар\n"
        "/delete_product product_id — отправить товар в архив\n"
        "/restore_product product_id — восстановить товар из архива\n"
        "/restock product_id amount — пополнить остаток товара\n\n"

        "✏️ Редактирование товара:\n"
        "/edit_price product_id new_price — изменить цену товара\n"
        "/edit_name product_id новое_название — изменить название товара\n"
        "/edit_description product_id новое_описание — изменить описание товара\n"
        "/edit_photo product_id — изменить или удалить фото товара\n\n"

        "📊 Статистика:\n"
        "/stats — статистика магазина\n\n"

        "🧩 Служебное:\n"
        "/help_admin — список админ-команд\n"
        "/myid — узнать свой Telegram ID\n\n"

        "Примеры:\n"
        "/add_balance 123456789 500\n"
        "/transactions 123456789\n"
        "/restock 5 10\n"
        "/edit_price 5 2500\n"
        "/edit_name 5 Игровая мышка Logitech\n"
        "/edit_description 5 Беспроводная мышка с RGB-подсветкой\n"
        "/edit_photo 5"
    )


# -------------------- История финансовых операций --------------------

def get_user_transactions_text(user_id):

    transactions = get_user_balance_transactions(user_id)

    if not transactions:
        return "У пользователя пока нет финансовых операций"

    text = f"💳 Финансовые операции пользователя {user_id}:\n\n"

    for index, transaction in enumerate(transactions, start=1):

        operation_type = transaction[0]
        amount = transaction[1]
        balance_before = transaction[2]
        balance_after = transaction[3]
        comment = transaction[4]
        created_at = transaction[5]

        text += (
            f"{index}. {operation_type}\n"
            f"Сумма: {amount} ₽\n"
            f"Баланс: {balance_before} ₽ → {balance_after} ₽\n"
            f"Комментарий: {comment}\n"
            f"Дата: {created_at}\n\n"
        )

    return text