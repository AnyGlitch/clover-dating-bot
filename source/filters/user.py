from __future__ import annotations

from typing import TYPE_CHECKING

from aiogram.filters import Filter

from source.database.services import UserService

if TYPE_CHECKING:
    from aiogram.types import Message

    from source.database.models import UserModel

__all__ = ["UserFilter"]


class UserFilter(Filter):
    async def __call__(self, message: Message) -> bool | dict[str, UserModel]:
        from_user = message.from_user
        if not from_user:
            return False
        user = await UserService.get_or_none_by_id(from_user.id)
        return {"user": user} if user else False
