from __future__ import annotations

from typing import TYPE_CHECKING

from aiogram import F, Router
from aiogram.filters import KICKED, ChatMemberUpdatedFilter

from source.database.services import UserService

if TYPE_CHECKING:
    from aiogram.fsm.context import FSMContext
    from aiogram.types import User

__all__ = ["forbidden_error_router"]

forbidden_error_router = Router(name=__name__)


@forbidden_error_router.my_chat_member(
    ChatMemberUpdatedFilter(KICKED),
    F.from_user.as_("user"),
)
async def forbidden_error_handler(_, state: FSMContext, user: User) -> None:
    await UserService.delete(user.id)
    await state.clear()
