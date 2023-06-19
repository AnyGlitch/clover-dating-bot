from aiogram.fsm.state import State, StatesGroup

__all__ = ["SignUpState"]


class SignUpState(StatesGroup):
    PHOTO = State()
    AGE = State()
    SEX = State()
    LOCATION = State()
