from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

__all__ = ["get_filter_settings_keyboard"]


def get_filter_settings_keyboard(
    age: int,
    sex_emoji: str,
) -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        resize_keyboard=True,
        keyboard=[
            [
                KeyboardButton(text=f"🔎🧸{age}"),
                KeyboardButton(text=f"🔎{sex_emoji}"),
            ],
            [KeyboardButton(text="🔽")],
        ],
    )
