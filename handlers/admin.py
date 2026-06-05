from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from states.admin_states import AddProduct, EditProductPhoto

from services.admin_service import (
    add_balance_to_user,
    get_user_profile_text,
    get_all_users_text,
    add_product_logic,
    delete_product_logic,
    restore_product_logic,
    get_products_admin_text,
    restock_product_logic,
    edit_product_price_logic,
    edit_product_name_logic,
    edit_product_description_logic,
    start_edit_product_photo_logic,
    edit_product_photo_logic,
    get_shop_stats_text,
    get_admin_help_text,
    get_user_transactions_text
)

from filters.admin_filter import AdminFilter


# -------------------- Роутер администратора --------------------

router = Router()


# -------------------- Пополнение баланса --------------------

@router.message(Command("add_balance"), AdminFilter())
async def add_balance_command(message: Message):

    text = message.text

    if text is None:
        await message.answer("Введите команду текстом")
        return

    parts = text.split()

    if len(parts) != 3:
        await message.answer("Формат: /add_balance user_id amount")
        return

    try:
        user_id = int(parts[1])
        amount = int(parts[2])
    except ValueError:
        await message.answer(
            "ID и сумма должны быть числами"
        )
        return

    result = add_balance_to_user(user_id, amount)

    await message.answer(result["message"])


# -------------------- Просмотр пользователя --------------------

@router.message(Command("user"), AdminFilter())
async def user_command(message: Message):

    text = message.text

    if text is None:
        await message.answer("Введите команду текстом")
        return

    parts = text.split()

    if len(parts) != 2:
        await message.answer("Формат: /user user_id")
        return

    try:
        user_id = int(parts[1])
    except ValueError:
        await message.answer(
            "ID должен быть числом"
        )
        return

    text = get_user_profile_text(user_id)

    await message.answer(text)


# -------------------- Список пользователей --------------------

@router.message(Command("users"), AdminFilter())
async def users_command(message: Message):

    text = get_all_users_text()

    await message.answer(text)


# -------------------- Добавление товара --------------------

@router.message(Command("add_product"), AdminFilter())
async def add_product_start(message: Message, state: FSMContext):

    await state.set_state(AddProduct.name)
    await message.answer("Введите название товара:")


# -------------------- Ввод названия товара --------------------

@router.message(AddProduct.name)
async def add_product_name(message: Message, state: FSMContext):

    product_name = message.text

    await state.update_data(name=product_name)
    await state.set_state(AddProduct.description)
    await message.answer("Введите описание товара:")


# -------------------- Ввод описания товара --------------------

@router.message(AddProduct.description)
async def add_product_description(message: Message, state: FSMContext):

    text = message.text

    if text is None:
        await message.answer("Описание должно быть текстом")
        return

    description = text.strip()

    if not description:
        await message.answer("Описание не может быть пустым")
        return

    await state.update_data(description=description)
    await state.set_state(AddProduct.price)
    await message.answer("Введите цену товара:")


# -------------------- Ввод цены товара --------------------

@router.message(AddProduct.price)
async def add_product_price(message: Message, state: FSMContext):

    text = message.text

    if text is None:
        await message.answer("Цена должна быть текстом/числом")
        return

    if not text.isdigit():
        await message.answer("Цена должна быть числом")
        return

    price = int(text)

    if price <= 0:
        await message.answer("Цена должна быть больше 0")
        return

    await state.update_data(price=price)
    await state.set_state(AddProduct.stock)
    await message.answer("Введите количество товара:")


# -------------------- Ввод количества товара --------------------

@router.message(AddProduct.stock)
async def add_product_stock(message: Message, state: FSMContext):

    text = message.text

    if text is None:
        await message.answer("Количество должно быть текстом/числом")
        return

    if not text.isdigit():
        await message.answer("Количество должно быть числом")
        return

    stock = int(text)

    if stock <= 0:
        await message.answer("Количество должно быть больше 0")
        return

    await state.update_data(stock=stock)

    await state.set_state(AddProduct.photo)

    await message.answer(
        "Отправьте фото товара или напишите: пропустить"
    )

# -------------------- Ввод фото товара --------------------

@router.message(AddProduct.photo)
async def add_product_photo(message: Message, state: FSMContext):

    if message.photo:
        photo_id = message.photo[-1].file_id

    elif message.text and message.text.lower().strip() == "пропустить":
        photo_id = None

    else:
        await message.answer(
            "Отправьте фото товара или напишите: пропустить"
        )
        return

    data = await state.get_data()

    name = data["name"]
    description = data["description"]
    price = data["price"]
    stock = data["stock"]

    result = add_product_logic(
        name=name,
        description=description,
        price=price,
        stock=stock,
        photo_id=photo_id
    )

    await state.clear()

    await message.answer(result["message"])


# -------------------- Удаление товара --------------------

@router.message(Command("delete_product"), AdminFilter())
async def delete_product_command(message: Message):

    text = message.text

    if text is None:
        await message.answer("Введите команду текстом")
        return

    parts = text.split()

    if len(parts) != 2:
        await message.answer("Формат: /delete_product product_id")
        return

    try:
        product_id = int(parts[1])
    except ValueError:
        await message.answer("ID товара должен быть числом")
        return

    result = delete_product_logic(product_id)

    await message.answer(result["message"])


# -------------------- Восстановление товара из архива --------------------

@router.message(Command("restore_product"), AdminFilter())
async def restore_product_command(message: Message):

    text = message.text

    if text is None:
        await message.answer("Введите команду текстом")
        return

    parts = text.split()

    if len(parts) != 2:
        await message.answer("Формат: /restore_product product_id")
        return

    try:
        product_id = int(parts[1])
    except ValueError:
        await message.answer("ID товара должен быть числом")
        return

    result = restore_product_logic(product_id)

    await message.answer(result["message"])


# -------------------- Список товаров --------------------

@router.message(Command("products"), AdminFilter())
async def products_command(message: Message):

    text = get_products_admin_text()

    await message.answer(text)


# -------------------- Пополнение остатка товара --------------------

@router.message(Command("restock"), AdminFilter())
async def restock_command(message: Message):

    text = message.text

    if text is None:
        await message.answer("Введите команду текстом")
        return

    parts = text.split()

    if len(parts) != 3:
        await message.answer("Формат: /restock product_id amount")
        return

    try:
        product_id = int(parts[1])
        amount = int(parts[2])
    except ValueError:
        await message.answer("ID товара и количество должны быть числами")
        return

    result = restock_product_logic(product_id, amount)

    await message.answer(result["message"])


# -------------------- Изменение цены товара --------------------

@router.message(Command("edit_price"), AdminFilter())
async def edit_price_command(message: Message):

    text = message.text

    if text is None:
        await message.answer("Введите команду текстом")
        return

    parts = text.split()

    if len(parts) != 3:
        await message.answer("Формат: /edit_price product_id new_price")
        return

    try:
        product_id = int(parts[1])
        new_price = int(parts[2])
    except ValueError:
        await message.answer("ID товара и цена должны быть числами")
        return

    result = edit_product_price_logic(product_id, new_price)

    await message.answer(result["message"])


# -------------------- Изменение названия товара --------------------

@router.message(Command("edit_name"), AdminFilter())
async def edit_name_command(message: Message):

    text = message.text

    if text is None:
        await message.answer("Введите команду текстом")
        return

    parts = text.split(maxsplit=2)

    if len(parts) != 3:
        await message.answer("Формат: /edit_name product_id новое_название")
        return

    try:
        product_id = int(parts[1])
    except ValueError:
        await message.answer("ID товара должен быть числом")
        return

    new_name = parts[2]

    result = edit_product_name_logic(product_id, new_name)

    await message.answer(result["message"])


# -------------------- Изменение описания товара --------------------

@router.message(Command("edit_description"), AdminFilter())
async def edit_description_command(message: Message):

    text = message.text

    if text is None:
        await message.answer("Введите команду текстом")
        return

    parts = text.split(maxsplit=2)

    if len(parts) != 3:
        await message.answer("Формат: /edit_description product_id новое_описание")
        return

    try:
        product_id = int(parts[1])
    except ValueError:
        await message.answer("ID товара должен быть числом")
        return

    new_description = parts[2]

    result = edit_product_description_logic(
        product_id,
        new_description
    )

    await message.answer(result["message"])


# -------------------- Изменение фото товара --------------------

@router.message(Command("edit_photo"), AdminFilter())
async def edit_photo_command(message: Message, state: FSMContext):

    text = message.text

    if text is None:
        await message.answer("Введите команду текстом")
        return

    parts = text.split()

    if len(parts) != 2:
        await message.answer("Формат: /edit_photo product_id")
        return

    try:
        product_id = int(parts[1])
    except ValueError:
        await message.answer("ID товара должен быть числом")
        return

    result = start_edit_product_photo_logic(product_id)

    if not result["success"]:
        await message.answer(result["message"])
        return

    await state.update_data(product_id=product_id)

    await state.set_state(EditProductPhoto.photo)

    await message.answer(result["message"])


# -------------------- Получение нового фото товара --------------------

@router.message(EditProductPhoto.photo)
async def edit_photo_save(message: Message, state: FSMContext):

    data = await state.get_data()

    product_id = data["product_id"]

    if message.photo:
        photo_id = message.photo[-1].file_id

    elif message.text and message.text.lower().strip() == "удалить":
        photo_id = None

    else:
        await message.answer(
            "Отправьте новое фото товара или напишите: удалить"
        )
        return

    result = edit_product_photo_logic(
        product_id=product_id,
        photo_id=photo_id
    )

    await state.clear()

    await message.answer(result["message"])


# -------------------- Статистика магазина --------------------

@router.message(Command("stats"), AdminFilter())
async def stats_command(message: Message):

    text = get_shop_stats_text()

    await message.answer(text)


# -------------------- Помощь администратору --------------------

@router.message(Command("help_admin"), AdminFilter())
async def help_admin_command(message: Message):

    text = get_admin_help_text()

    await message.answer(text)


# -------------------- Финансовые операции пользователя --------------------

@router.message(Command("transactions"), AdminFilter())
async def transactions_command(message: Message):

    text = message.text

    if text is None:
        await message.answer("Введите команду текстом")
        return

    parts = text.split()

    if len(parts) != 2:
        await message.answer("Формат: /transactions user_id")
        return

    try:
        user_id = int(parts[1])
    except ValueError:
        await message.answer("ID пользователя должен быть числом")
        return

    result_text = get_user_transactions_text(user_id)

    await message.answer(result_text)


