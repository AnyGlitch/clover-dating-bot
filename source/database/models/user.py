from __future__ import annotations

from typing import TYPE_CHECKING

from aiogram import html
from aiogram.utils.link import create_tg_link
from tortoise import Model
from tortoise.fields import (
    BigIntField,
    CharField,
    FloatField,
    IntEnumField,
    SmallIntField,
    TextField,
)

from source.types import Sex

if TYPE_CHECKING:
    from tortoise.fields import ReverseRelation

    from source.database.models import ReactionModel

__all__ = ["UserModel"]


class UserModel(Model):
    id = BigIntField(pk=True)
    name = CharField(max_length=64)
    bio = CharField(max_length=512, null=True)
    photo = TextField()
    age = SmallIntField()
    need_age = SmallIntField()
    sex = IntEnumField(Sex)
    need_sex = IntEnumField(Sex)
    country = CharField(max_length=64)
    state = CharField(max_length=64)
    city = CharField(max_length=64)
    latitude = FloatField()
    longitude = FloatField()

    sent_reactions: ReverseRelation[ReactionModel]
    received_reactions: ReverseRelation[ReactionModel]

    @property
    def link(self) -> str:
        return html.link(self.name, create_tg_link("user", id=self.id))

    class Meta:
        table = "users"
