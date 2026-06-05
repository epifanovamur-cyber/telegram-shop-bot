from aiogram.fsm.state import StatesGroup, State


class AddProduct(StatesGroup):

    name = State()

    description = State()

    price = State()

    stock = State()

    photo = State()


class EditProductPhoto(StatesGroup):

    photo = State()