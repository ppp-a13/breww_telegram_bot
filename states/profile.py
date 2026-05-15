from aiogram.fsm.state import StatesGroup, State


class UserDepositState(StatesGroup):
    INPUT_AMOUNT = State()
    APPLY_DEPOSIT = State()
