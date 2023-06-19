from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

__all__ = ["start_settings_keyboard"]

start_settings_keyboard = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[
        [KeyboardButton(text="🧩Основное"), KeyboardButton(text="🔎Фильтры")],
        [KeyboardButton(text="🔽")],
    ],
)
