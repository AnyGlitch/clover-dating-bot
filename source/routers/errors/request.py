from __future__ import annotations

from typing import TYPE_CHECKING

from aiogram import F, Router
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import ExceptionTypeFilter

from source.database.services import ReactionService
from source.keyboards import empty_keyboard
from source.messages import (
    photo_expired_error_message,
    search_not_found_error_message,
)
from source.states import MainSettingsState, ReactionState
from source.types import Reaction

if TYPE_CHECKING:
    from aiogram.fsm.context import FSMContext
    from aiogram.types import Message, User

__all__ = ["request_error_router"]

request_error_router = Router(name=__name__)

request_error_router.errors.filter(
    ExceptionTypeFilter(TelegramBadRequest),
    F.update.message.as_("message"),
)


@request_error_router.errors(F.update.message.text == "🙄")
async def request_error_handler(_, message: Message, state: FSMContext) -> None:
    await message.answer(
        photo_expired_error_message,
        reply_markup=empty_keyboard,
    )
    await state.set_state(MainSettingsState.CHANGE_PHOTO)


@request_error_router.errors(
    ReactionState(),
    F.update.message.from_user.as_("user"),
)
async def request_error_inside_search_handler(
    _,
    message: Message,
    state: FSMContext,
    user: User,
) -> None:
    data = await state.get_data()

    receiver_id = data["receiver_id"]

    await ReactionService.read(sender_id=receiver_id, receiver_id=user.id)
    await ReactionService.update_or_create(
        type_=Reaction.HATER,
        is_read=False,
        date=message.date,
        sender_id=user.id,
        receiver_id=receiver_id,
    )

    await message.answer(search_not_found_error_message)
    await state.clear()
