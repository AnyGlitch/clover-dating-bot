from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

__all__ = ["location_keyboard"]

location_keyboard = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[[KeyboardButton(text="🗺️", request_location=True)]],
)
