from __future__ import annotations

from typing import TYPE_CHECKING

from aiogram import F, Router
from aiogram.enums import ParseMode

from source.database.services import ReactionService, UserService
from source.filters import UserFilter
from source.keyboards import get_reaction_keyboard, menu_keyboard
from source.messages import (
    get_me_message,
    reaction_to_reciprocity_message,
    reaction_to_user_message,
    search_not_found_error_message,
)
from source.states import ReactionState
from source.types import Reaction

if TYPE_CHECKING:
    import datetime

    from aiogram import Bot
    from aiogram.fsm.context import FSMContext
    from aiogram.types import Message

    from source.database.models import UserModel

__all__ = ["search_router"]

search_router = Router(name=__name__)

search_router.message.filter(UserFilter())


@search_router.message(F.text == "🛸Смотреть")
async def search_handler(
    message: Message,
    state: FSMContext,
    user: UserModel,
) -> None:
    next_user, reaction = await UserService.get_next_user_by_filters(user)

    if not (next_user and reaction):
        await message.answer(
            search_not_found_error_message,
            reply_markup=menu_keyboard,
        )
        return

    reactions_to_states = {
        Reaction.RECIPROCITY: ReactionState.RECIPROCITY,
        Reaction.FOLLOWER: ReactionState.FOLLOWER,
        Reaction.USER: ReactionState.USER,
        Reaction.OTHER: ReactionState.OTHER,
    }

    await message.answer_photo(
        photo=next_user.photo,
        caption=get_me_message(
            name=next_user.name,
            bio=next_user.bio,
            age=next_user.age,
            city=next_user.city,
        ),
        reply_markup=get_reaction_keyboard(reaction),
    )

    await state.update_data(
        receiver_id=next_user.id,
        receiver_link=next_user.link,
    )
    await state.set_state(reactions_to_states[reaction])


@search_router.message(ReactionState.RECIPROCITY, F.text == "❤️")
async def like_to_reciprocity_handler(
    message: Message,
    state: FSMContext,
    user: UserModel,
) -> None:
    data = await state.get_data()

    receiver_id = data["receiver_id"]
    receiver_link = data["receiver_link"]

    await ReactionService.read(sender_id=receiver_id, receiver_id=user.id)

    await message.answer(
        reaction_to_reciprocity_message.format(receiver_link=receiver_link),
        parse_mode=ParseMode.HTML,
    )

    await search_handler(message, state, user)


@search_router.message(
    ReactionState.FOLLOWER,
    F.text == "👍",
    F.date.as_("date"),
)
async def like_to_follower_handler(
    message: Message,
    state: FSMContext,
    bot: Bot,
    user: UserModel,
    date: datetime.date,
) -> None:
    data = await state.get_data()

    receiver_id = data["receiver_id"]
    receiver_link = data["receiver_link"]

    await ReactionService.update(
        type_=Reaction.RECIPROCITY,
        is_read=True,
        date=date,
        sender_id=receiver_id,
        receiver_id=user.id,
    )
    await ReactionService.create(
        type_=Reaction.RECIPROCITY,
        date=date,
        sender_id=user.id,
        receiver_id=receiver_id,
    )

    await bot.send_message(receiver_id, reaction_to_user_message)

    await message.answer(
        reaction_to_reciprocity_message.format(receiver_link=receiver_link),
        parse_mode=ParseMode.HTML,
    )

    await search_handler(message, state, user)


@search_router.message(
    ReactionState.FOLLOWER,
    F.text == "👎",
    F.date.as_("date"),
)
async def dislike_to_follower_handler(
    message: Message,
    state: FSMContext,
    user: UserModel,
    date: datetime.date,
) -> None:
    data = await state.get_data()

    receiver_id = data["receiver_id"]

    await ReactionService.read(sender_id=receiver_id, receiver_id=user.id)
    await ReactionService.create(
        type_=Reaction.HATER,
        date=date,
        sender_id=user.id,
        receiver_id=receiver_id,
    )

    await search_handler(message, state, user)


@search_router.message(
    ReactionState.USER,
    F.text == "👍",
    F.date.as_("date"),
)
async def like_to_user_handler(
    message: Message,
    state: FSMContext,
    bot: Bot,
    user: UserModel,
    date: datetime.date,
) -> None:
    data = await state.get_data()

    receiver_id = data["receiver_id"]

    await ReactionService.create(
        type_=Reaction.FOLLOWER,
        date=date,
        sender_id=user.id,
        receiver_id=receiver_id,
    )

    await bot.send_message(receiver_id, reaction_to_user_message)

    await search_handler(message, state, user)


@search_router.message(
    ReactionState.USER,
    F.text == "👎",
    F.date.as_("date"),
)
async def dislike_to_user_handler(
    message: Message,
    state: FSMContext,
    user: UserModel,
    date: datetime.date,
) -> None:
    data = await state.get_data()

    receiver_id = data["receiver_id"]

    await ReactionService.create(
        type_=Reaction.HATER,
        date=date,
        sender_id=user.id,
        receiver_id=receiver_id,
    )

    await search_handler(message, state, user)


@search_router.message(
    ReactionState.OTHER,
    F.text == "👍",
    F.date.as_("date"),
)
async def like_to_other_handler(
    message: Message,
    state: FSMContext,
    bot: Bot,
    user: UserModel,
    date: datetime.date,
) -> None:
    data = await state.get_data()

    receiver_id = data["receiver_id"]

    await ReactionService.update(
        type_=Reaction.FOLLOWER,
        is_read=False,
        date=date,
        sender_id=user.id,
        receiver_id=receiver_id,
    )
    await ReactionService.delete(sender_id=receiver_id, receiver_id=user.id)

    await bot.send_message(receiver_id, reaction_to_user_message)

    await search_handler(message, state, user)


@search_router.message(
    ReactionState.OTHER,
    F.text == "👎",
    F.date.as_("date"),
)
async def dislike_to_other_handler(
    message: Message,
    state: FSMContext,
    user: UserModel,
    date: datetime.date,
) -> None:
    data = await state.get_data()

    receiver_id = data["receiver_id"]

    await ReactionService.update(
        type_=Reaction.HATER,
        is_read=False,
        date=date,
        sender_id=user.id,
        receiver_id=receiver_id,
    )
    await ReactionService.update(
        type_=Reaction.USER,
        is_read=True,
        date=date,
        sender_id=receiver_id,
        receiver_id=user.id,
    )

    await search_handler(message, state, user)
