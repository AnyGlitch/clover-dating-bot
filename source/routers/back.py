from __future__ import annotations

from typing import TYPE_CHECKING

from aiogram import F, Router

from source.keyboards import menu_keyboard
from source.messages import back_message

if TYPE_CHECKING:
    from aiogram.fsm.context import FSMContext
    from aiogram.types import Message

__all__ = ["back_router"]

back_router = Router(name=__name__)


@back_router.message(F.text == "🔽")
async def back_handler(message: Message, state: FSMContext) -> None:
    await message.answer(back_message, reply_markup=menu_keyboard)
    await state.clear()
