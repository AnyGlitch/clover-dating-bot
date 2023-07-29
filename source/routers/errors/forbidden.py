from __future__ import annotations

from typing import TYPE_CHECKING

from aiogram import Router
from aiogram.filters import KICKED, ChatMemberUpdatedFilter

from source.database.services import UserService
from source.filters import UserFilter

if TYPE_CHECKING:
    from aiogram.fsm.context import FSMContext

    from source.database.models import UserModel

__all__ = ["forbidden_error_router"]

forbidden_error_router = Router(name=__name__)


@forbidden_error_router.my_chat_member(
    ChatMemberUpdatedFilter(KICKED),
    UserFilter(),
)
async def forbidden_error_handler(
    _,
    state: FSMContext,
    user: UserModel,
) -> None:
    await UserService.delete(user)
    await state.clear()
