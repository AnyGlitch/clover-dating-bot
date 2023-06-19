from aiogram.fsm.state import State, StatesGroup

__all__ = ["MainSettingsState"]


class MainSettingsState(StatesGroup):
    CHANGE_NAME = State()
    CHANGE_BIO = State()
    CHANGE_PHOTO = State()
    CHANGE_AGE = State()
