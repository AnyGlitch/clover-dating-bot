from __future__ import annotations

from typing import TYPE_CHECKING

from aiogram import F, Router

from source.keyboards import start_settings_keyboard
from source.messages import start_settings_message

if TYPE_CHECKING:
    from aiogram.types import Message

__all__ = ["start_settings_router"]

start_settings_router = Router(name=__name__)


@start_settings_router.message(F.text == "⚙️")
async def start_settings_handler(message: Message) -> None:
    await message.answer(
        start_settings_message,
        reply_markup=start_settings_keyboard,
    )
