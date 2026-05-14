from aiogram.fsm.state import State, StatesGroup

class AddTeaStates(StatesGroup):
    name = State()
    description = State()
    price = State()
    category_id = State()
    quantity = State()
    photo = State()

class EditTeaState(StatesGroup):
    choosing_field = State()
    new_value = State()