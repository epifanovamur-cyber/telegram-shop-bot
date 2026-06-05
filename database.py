import sqlite3


# -------------------- Подключение к базе --------------------

db = sqlite3.connect("shop.db")
cursor = db.cursor()


# -------------------- Таблицы --------------------

cursor.execute("""
CREATE TABLE IF NOT EXISTS purchases (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    product_name TEXT,
    price INTEGER
)
""")


cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    balance INTEGER
)
""")


cursor.execute("""
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    price INTEGER,
    stock INTEGER
)
""")


cursor.execute("""
CREATE TABLE IF NOT EXISTS balance_transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    type TEXT,
    amount INTEGER,
    balance_before INTEGER,
    balance_after INTEGER,
    comment TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
)
""")


# -------------------- Финансовые операции --------------------

def add_balance_transaction(
    user_id,
    operation_type,
    amount,
    balance_before,
    balance_after,
    comment
):

    cursor.execute(
        """
        INSERT INTO balance_transactions (
            user_id,
            type,
            amount,
            balance_before,
            balance_after,
            comment
        )
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            user_id,
            operation_type,
            amount,
            balance_before,
            balance_after,
            comment
        )
    )


# -------------------- Обновление структуры таблиц --------------------

def add_column_if_not_exists(table_name, column_name, column_definition):

    cursor.execute(f"PRAGMA table_info({table_name})")

    columns = cursor.fetchall()

    column_names = []

    for column in columns:
        column_names.append(column[1])

    if column_name not in column_names:
        cursor.execute(
            f"ALTER TABLE {table_name} ADD COLUMN {column_name} {column_definition}"
        )

    db.commit()


add_column_if_not_exists(
    "products",
    "description",
    "TEXT DEFAULT ''"
)

add_column_if_not_exists(
    "products",
    "photo_id",
    "TEXT"
)

add_column_if_not_exists(
    "products",
    "status",
    "TEXT DEFAULT 'active'"
)

add_column_if_not_exists(
    "purchases",
    "product_id",
    "INTEGER"
)

add_column_if_not_exists(
    "purchases",
    "created_at",
    "TEXT"
)


# -------------------- Пользователи --------------------

def add_user(user_id):

    cursor.execute(
        "SELECT * FROM users WHERE user_id = ?",
        (user_id,)
    )

    user = cursor.fetchone()

    if user is None:

        cursor.execute(
            "INSERT INTO users (user_id, balance) VALUES (?, ?)",
            (user_id, 1000)
        )

        db.commit()


def get_all_users():

    cursor.execute(
        """
        SELECT user_id, balance
        FROM users
        ORDER BY user_id DESC
        """
    )

    return cursor.fetchall()


# -------------------- Проверка существования пользователя --------------------

def user_exists(user_id):

    cursor.execute(
        """
        SELECT user_id
        FROM users
        WHERE user_id = ?
        """,
        (user_id,)
    )

    user = cursor.fetchone()

    return user is not None


# -------------------- Баланс --------------------

def get_balance(user_id):

    cursor.execute(
        "SELECT balance FROM users WHERE user_id = ?",
        (user_id,)
    )

    balance = cursor.fetchone()

    if balance is None:

        add_user(user_id)

        return 1000

    return balance[0]


def update_balance(user_id, new_balance):

    cursor.execute(
        "UPDATE users SET balance = ? WHERE user_id = ?",
        (new_balance, user_id)
    )

    db.commit()


# -------------------- Покупки --------------------

def add_purchase(user_id, product_id, product_name, price):

    cursor.execute(
        """
        INSERT INTO purchases (
            user_id,
            product_id,
            product_name,
            price,
            created_at
        )
        VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP)
        """,
        (
            user_id,
            product_id,
            product_name,
            price
        )
    )

    db.commit()


def get_purchases(user_id):

    cursor.execute(
        """
        SELECT product_name, price, created_at
        FROM purchases
        WHERE user_id = ?
        ORDER BY id DESC
        """,
        (user_id,)
    )

    return cursor.fetchall()


def get_history(user_id):

    cursor.execute(
        """
        SELECT product_name, price, created_at
        FROM purchases
        WHERE user_id = ?
        ORDER BY id DESC
        """,
        (user_id,)
    )

    return cursor.fetchall()


def get_total_spent(user_id):

    cursor.execute(
        "SELECT product_name, price FROM purchases WHERE user_id = ?",
        (user_id,)
    )

    purchases = cursor.fetchall()

    total = 0

    for purchase in purchases:

        price = purchase[1]

        total += price

    return total


# -------------------- Покупка товара транзакцией --------------------

def buy_product_transaction(user_id, product_id):

    try:
        cursor.execute("BEGIN IMMEDIATE")

        cursor.execute(
            """
            SELECT id, name, price, stock
            FROM products
            WHERE id = ?
            AND status = 'active'
            """,
            (product_id,)
        )

        product = cursor.fetchone()

        if product is None:
            db.rollback()

            return {
                "success": False,
                "message": "❌ Товар не найден"
            }

        product_id, product_name, product_price, product_stock = product

        if product_stock <= 0:
            db.rollback()

            return {
                "success": False,
                "message": "❌ Товар закончился"
            }

        cursor.execute(
            "SELECT balance FROM users WHERE user_id = ?",
            (user_id,)
        )

        balance_data = cursor.fetchone()

        if balance_data is None:
            balance = 1000

            cursor.execute(
                "INSERT INTO users (user_id, balance) VALUES (?, ?)",
                (user_id, balance)
            )
        else:
            balance = balance_data[0]

        if balance < product_price:
            db.rollback()

            return {
                "success": False,
                "message": (
                    f"❌ Недостаточно средств\n\n"
                    f"Баланс: {balance} ₽"
                )
            }

        cursor.execute(
            """
            UPDATE products
            SET stock = stock - 1
            WHERE id = ?
            AND stock > 0
            AND status = 'active'
            """,
            (product_id,)
        )

        if cursor.rowcount == 0:
            db.rollback()

            return {
                "success": False,
                "message": "❌ Товар уже закончился"
            }

        new_balance = balance - product_price
        new_stock = product_stock - 1

        cursor.execute(
            "UPDATE users SET balance = ? WHERE user_id = ?",
            (new_balance, user_id)
        )

        cursor.execute(
            """
            INSERT INTO purchases (
                user_id,
                product_id,
                product_name,
                price,
                created_at
            )
            VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP)
            """,
            (
                user_id,
                product_id,
                product_name,
                product_price
            )
        )

        add_balance_transaction(
            user_id=user_id,
            operation_type="purchase",
            amount=-product_price,
            balance_before=balance,
            balance_after=new_balance,
            comment=f"Покупка товара: {product_name}"
        )

        db.commit()

        return {
            "success": True,
            "product_name": product_name,
            "product_price": product_price,
            "new_balance": new_balance,
            "new_stock": new_stock
        }

    except Exception as error:
        db.rollback()

        print(f"Ошибка покупки товара: {error}")

        return {
            "success": False,
            "message": "❌ Ошибка базы данных. Попробуйте позже"
        }


# -------------------- Админское пополнение баланса транзакцией --------------------

def add_balance_transaction_logic(user_id, amount):

    try:
        cursor.execute("BEGIN IMMEDIATE")

        cursor.execute(
            """
            SELECT balance
            FROM users
            WHERE user_id = ?
            """,
            (user_id,)
        )

        balance_data = cursor.fetchone()

        if balance_data is None:
            db.rollback()

            return {
                "success": False,
                "message": "❌ Пользователь не найден"
            }

        current_balance = balance_data[0]

        new_balance = current_balance + amount

        cursor.execute(
            """
            UPDATE users
            SET balance = ?
            WHERE user_id = ?
            """,
            (new_balance, user_id)
        )

        add_balance_transaction(
            user_id=user_id,
            operation_type="admin_topup",
            amount=amount,
            balance_before=current_balance,
            balance_after=new_balance,
            comment="Админское пополнение баланса"
        )

        db.commit()

        return {
            "success": True,
            "new_balance": new_balance,
            "current_balance": current_balance
        }

    except Exception as error:
        db.rollback()

        print(f"Ошибка пополнения баланса: {error}")

        return {
            "success": False,
            "message": "❌ Ошибка базы данных. Попробуйте позже"
        }

# -------------------- Товары --------------------

def add_product(name, price, stock, description="", photo_id=None):

    cursor.execute(
        """
        INSERT INTO products (
            name,
            description,
            price,
            stock,
            photo_id,
            status
        )
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            name,
            description,
            price,
            stock,
            photo_id,
            "active"
        )
    )

    db.commit()


def get_all_products():

    cursor.execute(
        """
        SELECT id, name, price, stock
        FROM products
        WHERE status = 'active'
        """
    )

    return cursor.fetchall()


def get_product_buy_id(product_id):

    cursor.execute(
        """
        SELECT id, name, price, stock
        FROM products
        WHERE id = ?
        AND status = 'active'
        """,
        (product_id,)
    )

    return cursor.fetchone()


def update_product_stock(product_id, new_stock):
    cursor.execute(
        "UPDATE products SET stock = ? WHERE id = ?",
        (new_stock, product_id)
    )

    db.commit()


def get_top_products():

    conn = sqlite3.connect("shop.db")
    local_cursor = conn.cursor()

    local_cursor.execute(
        "SELECT product_name, COUNT(*) FROM purchases GROUP BY product_name ORDER BY COUNT(*) DESC LIMIT 3"
    )

    top_products = local_cursor.fetchall()
    conn.close()

    return top_products


def get_product_card(product_id):

    cursor.execute(
        """
        SELECT id, name, description, price, stock, photo_id
        FROM products
        WHERE id = ?
        AND status = 'active'
        """,
        (product_id,)
    )

    return cursor.fetchone()


def archive_product(product_id):

    cursor.execute(
        """
        UPDATE products
        SET status = 'archived'
        WHERE id = ?
        """,
        (product_id,)
    )

    db.commit()


# -------------------- Количество покупок пользователя --------------------

def get_user_purchases_count(user_id):

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM purchases
        WHERE user_id = ?
        """,
        (user_id,)
    )

    return cursor.fetchone()[0]


# -------------------- Получение товара по ID с любым статусом --------------------

def get_product_by_id(product_id):

    cursor.execute(
        """
        SELECT id, name, price, stock, status
        FROM products
        WHERE id = ?
        """,
        (product_id,)
    )

    return cursor.fetchone()


# -------------------- Восстановление товара из архива --------------------

def restore_product(product_id):

    cursor.execute(
        """
        UPDATE products
        SET status = 'active'
        WHERE id = ?
        """,
        (product_id,)
    )

    db.commit()


# -------------------- Все товары для админки --------------------

def get_all_products_for_admin():

    cursor.execute(
        """
        SELECT id, name, price, stock, status
        FROM products
        ORDER BY id DESC
        """
    )

    return cursor.fetchall()


# -------------------- Пополнение остатка товара --------------------

def restock_product(product_id, amount):

    cursor.execute(
        """
        UPDATE products
        SET stock = stock + ?
        WHERE id = ?
        """,
        (amount, product_id)
    )

    db.commit()


# -------------------- Изменение цены товара --------------------

def update_product_price(product_id, new_price):

    cursor.execute(
        """
        UPDATE products
        SET price = ?
        WHERE id = ?
        """,
        (new_price, product_id)
    )

    db.commit()


# -------------------- Изменение названия товара --------------------

def update_product_name(product_id, new_name):

    cursor.execute(
        """
        UPDATE products
        SET name = ?
        WHERE id = ?
        """,
        (new_name, product_id)
    )

    db.commit()


# -------------------- Изменение описания товара --------------------

def update_product_description(product_id, new_description):

    cursor.execute(
        """
        UPDATE products
        SET description = ?
        WHERE id = ?
        """,
        (new_description, product_id)
    )

    db.commit()


# -------------------- Изменение фото товара --------------------

def update_product_photo(product_id, photo_id):

    cursor.execute(
        """
        UPDATE products
        SET photo_id = ?
        WHERE id = ?
        """,
        (photo_id, product_id)
    )

    db.commit()


# -------------------- Статистика магазина --------------------

def get_users_count():

    cursor.execute(
        "SELECT COUNT(*) FROM users"
    )

    return cursor.fetchone()[0]


def get_products_count_by_status(status):

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM products
        WHERE status = ?
        """,
        (status,)
    )

    return cursor.fetchone()[0]


def get_purchases_count():

    cursor.execute(
        "SELECT COUNT(*) FROM purchases"
    )

    return cursor.fetchone()[0]


def get_total_revenue():

    cursor.execute(
        """
        SELECT COALESCE(SUM(price), 0)
        FROM purchases
        """
    )

    return cursor.fetchone()[0]


def get_active_stock_sum():

    cursor.execute(
        """
        SELECT COALESCE(SUM(stock), 0)
        FROM products
        WHERE status = 'active'
        """
    )

    return cursor.fetchone()[0]


# -------------------- Финансовые операции пользователя --------------------

def get_user_balance_transactions(user_id):

    cursor.execute(
        """
        SELECT type, amount, balance_before, balance_after, comment, created_at
        FROM balance_transactions
        WHERE user_id = ?
        ORDER BY id DESC
        LIMIT 20
        """,
        (user_id,)
    )

    return cursor.fetchall()