from __future__ import annotations

from typing import TYPE_CHECKING, TypeAlias

from source.database.models import ReactionModel

if TYPE_CHECKING:
    import datetime

    from source.types import Reaction

__all__ = ["ReactionService"]

MODEL: TypeAlias = ReactionModel


class ReactionService:
    @staticmethod
    async def create(
        type_: Reaction,
        date: datetime.date,
        sender_id: int,
        receiver_id: int,
    ) -> None:
        await MODEL.create(
            type=type_,
            is_read=False,
            date=date,
            sender_id=sender_id,
            receiver_id=receiver_id,
        )

    @staticmethod
    async def read(sender_id: int, receiver_id: int) -> None:
        await MODEL.filter(sender_id=sender_id, receiver_id=receiver_id).update(
            is_read=True,
        )

    @staticmethod
    async def update(
        type_: Reaction,
        is_read: bool,
        date: datetime.date,
        sender_id: int,
        receiver_id: int,
    ) -> None:
        await MODEL.filter(sender_id=sender_id, receiver_id=receiver_id).update(
            type=type_,
            is_read=is_read,
            date=date,
        )

    @staticmethod
    async def update_or_create(
        type_: Reaction,
        is_read: bool,
        date: datetime.date,
        sender_id: int,
        receiver_id: int,
    ) -> tuple[MODEL, bool]:
        return await MODEL.update_or_create(
            defaults={"type": type_, "is_read": is_read, "date": date},
            sender_id=sender_id,
            receiver_id=receiver_id,
        )

    @staticmethod
    async def delete(sender_id: int, receiver_id: int) -> None:
        await MODEL.filter(
            sender_id=sender_id,
            receiver_id=receiver_id,
        ).delete()
