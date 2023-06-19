from __future__ import annotations

from typing import TYPE_CHECKING, TypeAlias

from pypika import Interval, Parameter
from tortoise.expressions import Q

from source.database.models import UserModel
from source.types import Reaction, Sex

if TYPE_CHECKING:
    from source.types import Address

__all__ = ["MODEL", "UserService"]

MODEL: TypeAlias = UserModel


class UserService:
    @staticmethod
    async def create(
        pk: int,
        name: str,
        photo: str,
        age: int,
        need_age: int,
        sex: Sex,
        need_sex: Sex,
        address: Address,
        bio: str | None = None,
    ) -> MODEL:
        return await MODEL.create(
            id=pk,
            name=name,
            bio=bio,
            photo=photo,
            age=age,
            need_age=need_age,
            sex=sex,
            need_sex=need_sex,
            country=address.country,
            state=address.state,
            city=address.city,
            latitude=address.latitude,
            longitude=address.longitude,
        )

    @staticmethod
    async def get_or_none_by_id(pk: int) -> MODEL | None:
        return await MODEL.get_or_none(id=pk)

    @staticmethod
    async def get_next_user_by_filters(
        user: MODEL,
    ) -> tuple[MODEL, Reaction] | tuple[None, None]:
        next_reciprocity = await UserService.get_next_reciprocity(user)
        if next_reciprocity:
            return next_reciprocity, Reaction.RECIPROCITY

        next_follower = await UserService.get_next_follower(user)
        if next_follower:
            return next_follower, Reaction.FOLLOWER

        next_user = await UserService.get_next_user(user)
        if next_user:
            return next_user, Reaction.USER

        next_other = await UserService.get_next_other(user)
        if next_other:
            return next_other, Reaction.OTHER

        return None, None

    @staticmethod
    async def get_next_reciprocity(user: MODEL) -> MODEL | None:
        return await MODEL.filter(
            sent_reactions__receiver=user,
            sent_reactions__type=Reaction.RECIPROCITY,
            sent_reactions__is_read=False,
        ).first()

    @staticmethod
    async def get_next_follower(user: MODEL) -> MODEL | None:
        return await MODEL.filter(
            sent_reactions__receiver=user,
            sent_reactions__type=Reaction.FOLLOWER,
            sent_reactions__is_read=False,
        ).first()

    @staticmethod
    async def get_next_user(user: MODEL) -> MODEL | None:
        await user.fetch_related(
            "sent_reactions__receiver",
            "received_reactions__sender",
        )
        senders = {reaction.sender.id for reaction in user.received_reactions}
        receivers = {reaction.receiver.id for reaction in user.sent_reactions}
        query = MODEL.filter(
            ~Q(id__in=senders | receivers | {user.id}),
            Q(age__range=(user.need_age, user.need_age + 3)),
            Q(city=user.city) | Q(state=user.state) | Q(country=user.country),
        )
        if user.need_sex != Sex.ANY:
            query = query.filter(sex=user.need_sex, need_sex=user.sex)
        else:
            query = query.filter(need_sex__in={Sex.ANY, user.sex})
        return await query.first()

    @staticmethod
    async def get_next_other(user: MODEL) -> MODEL | None:
        return await MODEL.filter(
            sent_reactions__receiver=user,
            sent_reactions__type__in={
                Reaction.FOLLOWER,
                Reaction.USER,
                Reaction.HATER,
            },
            sent_reactions__date__lte=Parameter("CURRENT_DATE")
            - Interval(days=1),
        ).first()

    @staticmethod
    async def update_name(user: MODEL, new_name: str) -> None:
        user.name = new_name
        await user.save()

    @staticmethod
    async def update_bio(user: MODEL, new_bio: str) -> None:
        user.bio = new_bio
        await user.save()

    @staticmethod
    async def update_photo(user: MODEL, new_photo: str) -> None:
        user.photo = new_photo
        await user.save()

    @staticmethod
    async def update_age(user: MODEL, new_age: int) -> None:
        user.age = new_age
        await user.save()

    @staticmethod
    async def update_sex(user: MODEL, new_sex: Sex) -> None:
        user.sex = new_sex
        await user.save()

    @staticmethod
    async def update_location(user: MODEL, new_address: Address) -> None:
        user.country = new_address.country
        user.state = new_address.state
        user.city = new_address.city
        user.latitude = new_address.latitude
        user.longitude = new_address.longitude
        await user.save()

    @staticmethod
    async def update_need_age(user: MODEL, new_need_age: int) -> None:
        user.need_age = new_need_age
        await user.save()

    @staticmethod
    async def update_need_sex(user: MODEL, new_need_sex: Sex) -> None:
        user.need_sex = new_need_sex
        await user.save()

    @staticmethod
    async def delete(pk: int) -> None:
        user = await MODEL.get(id=pk)
        await user.delete()
