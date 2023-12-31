from __future__ import annotations

from typing import TYPE_CHECKING

from aiogram import F, Router

from source.filters import UserFilter
from source.messages import get_me_message

if TYPE_CHECKING:
    from aiogram.types import Message

    from source.database.models import UserModel

__all__ = ["me_router"]

me_router = Router(name=__name__)


@me_router.message(F.text == "🙄", UserFilter())
async def me_handler(message: Message, user: UserModel) -> None:
    await message.answer_photo(
        photo=user.photo,
        caption=get_me_message(
            name=user.name,
            bio=user.bio,
            age=user.age,
            city=user.city,
        ),
    )
