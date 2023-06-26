from __future__ import annotations

from typing import TYPE_CHECKING

from aiogram import F, Router
from aiogram.exceptions import TelegramBadRequest

from source.filters import UserFilter
from source.keyboards import empty_keyboard
from source.messages import bad_photo_message, get_me_message
from source.states import MainSettingsState

if TYPE_CHECKING:
    from aiogram.fsm.context import FSMContext
    from aiogram.types import Message

    from source.database.services import USER_MODEL

__all__ = ["me_router"]

me_router = Router(name="Me Router")


@me_router.message(F.text == "🙄", UserFilter())
async def me_handler(
    message: Message,
    state: FSMContext,
    user: USER_MODEL,
) -> None:
    try:
        await message.answer_photo(
            photo=user.photo,
            caption=get_me_message(
                name=user.name,
                bio=user.bio,
                age=user.age,
                city=user.city,
            ),
        )
    except TelegramBadRequest:
        await message.answer(bad_photo_message, reply_markup=empty_keyboard)
        await state.set_state(MainSettingsState.CHANGE_PHOTO)
