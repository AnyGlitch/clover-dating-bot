from aiogram.fsm.state import State, StatesGroup

__all__ = ["FilterSettingsState"]


class FilterSettingsState(StatesGroup):
    CHANGE_NEED_AGE = State()
    CHANGE_NEED_SEX = State()
