from __future__ import annotations

from typing import TYPE_CHECKING

from aiogram import F, Router
from aiogram.filters import CommandStart
from pydantic import ValidationError

from source.database.services import UserService
from source.filters import UserFilter
from source.helpers import EmojiHelper, LocationHelper
from source.keyboards import location_keyboard, menu_keyboard, sex_keyboard
from source.messages import (
    age_message,
    location_message,
    location_not_found_message,
    photo_not_found_message,
    sex_message,
    start_message,
    start_to_run_message,
)
from source.states import SignUpState

if TYPE_CHECKING:
    from aiogram import Bot
    from aiogram.fsm.context import FSMContext
    from aiogram.types import Location, Message, User

__all__ = ["sign_up_router"]

sign_up_router = Router(name="Sign Up Router")


@sign_up_router.message(
    CommandStart(),
    ~UserFilter(),
    F.from_user.as_("user"),
)
async def start_handler(
    message: Message,
    state: FSMContext,
    bot: Bot,
    user: User,
) -> None:
    chat = await bot.get_chat(user.id)
    profile = await user.get_profile_photos(limit=1)

    if not profile.photos:
        await message.answer(photo_not_found_message)
        return

    photo = profile.photos[0][-1]
    await message.answer(start_message.format(name=user.first_name))
    await state.update_data(
        id=user.id,
        name=user.first_name,
        bio=chat.bio,
        photo=photo.file_id,
    )
    await state.set_state(SignUpState.AGE)


@sign_up_router.message(CommandStart(), UserFilter())
async def start_to_run(message: Message, state: FSMContext) -> None:
    await message.answer(start_to_run_message, reply_markup=menu_keyboard)
    await state.clear()


@sign_up_router.message(
    SignUpState.AGE,
    F.text.cast(int).as_("age"),
    F.text.cast(int).in_(range(16, 33)),
)
async def age_handler(message: Message, state: FSMContext, age: int) -> None:
    await message.answer(age_message, reply_markup=sex_keyboard)
    await state.update_data(age=age, need_age=age)
    await state.set_state(SignUpState.SEX)


@sign_up_router.message(
    SignUpState.SEX,
    F.text.as_("emoji"),
    F.text.in_({"🙋‍♀️", "🙋‍♂️"}),
)
async def sex_handler(message: Message, state: FSMContext, emoji: str) -> None:
    sex = EmojiHelper.get_sex(emoji)
    need_sex = EmojiHelper.get_opposite_sex(emoji)
    await message.answer(sex_message, reply_markup=location_keyboard)
    await state.update_data(sex=sex, need_sex=need_sex)
    await state.set_state(SignUpState.LOCATION)


@sign_up_router.message(SignUpState.LOCATION, F.location.as_("location"))
async def location_handler(
    message: Message,
    state: FSMContext,
    location: Location,
) -> None:
    data = await state.get_data()

    try:
        address = await LocationHelper.get_address(
            location.latitude,
            location.longitude,
        )
    except ValidationError:
        await message.answer(location_not_found_message)
        return

    await UserService.create(
        pk=data["id"],
        name=data["name"],
        bio=data["bio"],
        photo=data["photo"],
        age=data["age"],
        need_age=data["need_age"],
        sex=data["sex"],
        need_sex=data["need_sex"],
        address=address,
    )
    await message.answer(location_message, reply_markup=menu_keyboard)
    await state.clear()
