from __future__ import annotations

from typing import TYPE_CHECKING

from aiogram import F, Router
from aiogram.filters import CommandStart
from pydantic import ValidationError

from source.database.services import UserService
from source.filters import UserFilter
from source.helpers import EmojiHelper, LocationHelper
from source.keyboards import (
    empty_keyboard,
    location_keyboard,
    menu_keyboard,
    sex_keyboard,
)
from source.messages import (
    finish_message,
    get_age_message,
    get_location_message,
    get_photo_message,
    get_sex_message,
    location_validation_error_message,
    start_message,
    start_to_run_message,
)
from source.states import SignUpState

if TYPE_CHECKING:
    from aiogram import Bot
    from aiogram.fsm.context import FSMContext
    from aiogram.types import Location, Message, PhotoSize, User

__all__ = ["sign_up_router"]

sign_up_router = Router(name=__name__)


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

    photo = None
    if photos := profile.photos:
        size = photos[0][-1]
        photo = size.file_id

    await message.answer(start_message.format(name=user.first_name))
    await message.answer(get_age_message)

    await state.update_data(
        id=user.id,
        name=user.first_name,
        bio=chat.bio,
        photo=photo,
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
    await message.answer(get_sex_message, reply_markup=sex_keyboard)
    await state.update_data(age=age, need_age=age)
    await state.set_state(SignUpState.SEX)


@sign_up_router.message(
    SignUpState.SEX,
    F.text.as_("emoji"),
    F.text.in_({"🙋‍♀️", "🙋‍♂️"}),
)
async def sex_handler(message: Message, state: FSMContext, emoji: str) -> None:
    data = await state.get_data()

    sex = EmojiHelper.get_sex(emoji)
    need_sex = EmojiHelper.get_opposite_sex(emoji)

    if data["photo"]:
        to_state = SignUpState.LOCATION
        text, keyboard = get_location_message, location_keyboard
    else:
        to_state = SignUpState.PHOTO
        text, keyboard = get_photo_message, empty_keyboard  # type: ignore

    await message.answer(text, reply_markup=keyboard)
    await state.update_data(sex=sex, need_sex=need_sex)
    await state.set_state(to_state)


@sign_up_router.message(SignUpState.PHOTO, F.photo.pop().as_("photo"))
async def photo_handler(
    message: Message,
    state: FSMContext,
    photo: PhotoSize,
) -> None:
    await message.answer(get_location_message, reply_markup=location_keyboard)
    await state.update_data(photo=photo.file_id)
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
        await message.answer(location_validation_error_message)
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
        **address.dict(),
    )
    await message.answer(finish_message, reply_markup=menu_keyboard)
    await state.clear()
