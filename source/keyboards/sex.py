from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

__all__ = ["need_sex_keyboard", "sex_keyboard"]

sex_keyboard = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[
        [KeyboardButton(text="🙋‍♀️"), KeyboardButton(text="🙋‍♂️")],
    ],
)

need_sex_keyboard = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[
        [
            KeyboardButton(text="🔎🙋‍♀️"),
            KeyboardButton(text="🔎🙋‍♂️"),
            KeyboardButton(text="🔎❤️"),
        ],
    ],
)
