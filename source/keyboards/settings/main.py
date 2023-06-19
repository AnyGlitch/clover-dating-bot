from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

__all__ = ["get_main_settings_keyboard"]


def get_main_settings_keyboard(
    name: str,
    age: int,
    sex_emoji: str,
    city: str,
) -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        resize_keyboard=True,
        keyboard=[
            [
                KeyboardButton(text=f"🎓{name}"),
                KeyboardButton(text="📨Описание"),
                KeyboardButton(text="🪄Фото"),
            ],
            [KeyboardButton(text=f"🧸{age}"), KeyboardButton(text=sex_emoji)],
            [KeyboardButton(text=f"🗺️{city}", request_location=True)],
            [KeyboardButton(text="🔽")],
        ],
    )
