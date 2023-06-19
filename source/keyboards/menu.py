from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

__all__ = ["menu_keyboard"]

menu_keyboard = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[
        [KeyboardButton(text="🛸Смотреть")],
        [KeyboardButton(text="🙄"), KeyboardButton(text="⚙️")],
    ],
)
