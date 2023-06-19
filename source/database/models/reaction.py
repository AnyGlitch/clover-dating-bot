from __future__ import annotations

from typing import TYPE_CHECKING

from tortoise import Model
from tortoise.fields import (
    BigIntField,
    BooleanField,
    DateField,
    ForeignKeyField,
    IntEnumField,
)

from source.types import Reaction

if TYPE_CHECKING:
    from tortoise.fields import ForeignKeyRelation

    from source.database.models import UserModel

__all__ = ["ReactionModel"]


class ReactionModel(Model):
    id = BigIntField(pk=True)
    type = IntEnumField(Reaction)
    is_read = BooleanField()
    date = DateField()

    sender: ForeignKeyRelation[UserModel] = ForeignKeyField(
        "models.UserModel",
        related_name="sent_reactions",
    )
    receiver: ForeignKeyRelation[UserModel] = ForeignKeyField(
        "models.UserModel",
        related_name="received_reactions",
    )

    class Meta:
        table = "reactions"
