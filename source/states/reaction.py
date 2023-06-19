from aiogram.fsm.state import State, StatesGroup

__all__ = ["ReactionState"]


class ReactionState(StatesGroup):
    RECIPROCITY = State()
    FOLLOWER = State()
    USER = State()
    OTHER = State()
