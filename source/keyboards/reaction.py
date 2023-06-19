from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

from source.types import Reaction

__all__ = ["get_reaction_keyboard"]

reaction_to_reciprocity_keyboard = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[[KeyboardButton(text="❤️")], [KeyboardButton(text="🔽")]],
)

reaction_to_user_keyboard = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[
        [KeyboardButton(text="👍"), KeyboardButton(text="👎")],
        [KeyboardButton(text="🔽")],
    ],
)


def get_reaction_keyboard(reaction: Reaction) -> ReplyKeyboardMarkup:
    if reaction == Reaction.RECIPROCITY:
        return reaction_to_reciprocity_keyboard
    return reaction_to_user_keyboard
