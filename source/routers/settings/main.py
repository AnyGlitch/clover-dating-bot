from __future__ import annotations

from typing import TYPE_CHECKING

from aiogram import F, Router
from pydantic import ValidationError

from source.database.services import UserService
from source.filters import UserFilter
from source.helpers import EmojiHelper, LocationHelper
from source.keyboards import empty_keyboard, get_main_settings_keyboard
from source.messages import (
    age_settings_message,
    bio_settings_message,
    change_age_message,
    change_bio_message,
    change_location_message,
    change_location_not_found_message,
    change_name_message,
    change_photo_message,
    change_sex_message,
    main_settings_message,
    name_settings_message,
    photo_settings_message,
)
from source.states import MainSettingsState

if TYPE_CHECKING:
    from aiogram.fsm.context import FSMContext
    from aiogram.types import Location, Message, PhotoSize

    from source.database.services import USER_MODEL

__all__ = ["main_settings_router"]

main_settings_router = Router(name="Main Settings Router")

main_settings_router.message.filter(UserFilter())


@main_settings_router.message(F.text == "🧩Основное")
async def main_settings_handler(message: Message, user: USER_MODEL) -> None:
    sex_emoji = EmojiHelper.get_by_sex(user.sex)
    await message.answer(
        main_settings_message,
        reply_markup=get_main_settings_keyboard(
            user.name,
            user.age,
            sex_emoji,
            user.city,
        ),
    )


@main_settings_router.message(F.text.startswith("🎓"))
async def name_settings_handler(message: Message, state: FSMContext) -> None:
    await message.answer(name_settings_message, reply_markup=empty_keyboard)
    await state.set_state(MainSettingsState.CHANGE_NAME)


@main_settings_router.message(
    MainSettingsState.CHANGE_NAME,
    F.text.as_("new_name"),
    F.text.len() <= 64,
)
async def change_name_handler(
    message: Message,
    state: FSMContext,
    user: USER_MODEL,
    new_name: str,
) -> None:
    sex_emoji = EmojiHelper.get_by_sex(user.sex)
    await UserService.update_name(user, new_name)
    await message.answer(
        change_name_message.format(name=new_name),
        reply_markup=get_main_settings_keyboard(
            user.name,
            user.age,
            sex_emoji,
            user.city,
        ),
    )
    await state.clear()


@main_settings_router.message(F.text == "📨Описание")
async def bio_settings_handler(message: Message, state: FSMContext) -> None:
    await message.answer(bio_settings_message, reply_markup=empty_keyboard)
    await state.set_state(MainSettingsState.CHANGE_BIO)


@main_settings_router.message(
    MainSettingsState.CHANGE_BIO,
    F.text.as_("new_bio"),
    F.text.len() <= 512,
)
async def change_bio_handler(
    message: Message,
    state: FSMContext,
    user: USER_MODEL,
    new_bio: str,
) -> None:
    sex_emoji = EmojiHelper.get_by_sex(user.sex)
    await UserService.update_bio(user, new_bio)
    await message.answer(
        change_bio_message,
        reply_markup=get_main_settings_keyboard(
            user.name,
            user.age,
            sex_emoji,
            user.city,
        ),
    )
    await state.clear()


@main_settings_router.message(F.text == "🪄Фото")
async def photo_settings_handler(message: Message, state: FSMContext) -> None:
    await message.answer(photo_settings_message, reply_markup=empty_keyboard)
    await state.set_state(MainSettingsState.CHANGE_PHOTO)


@main_settings_router.message(
    MainSettingsState.CHANGE_PHOTO,
    F.photo.pop().as_("new_photo"),
)
async def change_photo_handler(
    message: Message,
    state: FSMContext,
    user: USER_MODEL,
    new_photo: PhotoSize,
) -> None:
    sex_emoji = EmojiHelper.get_by_sex(user.sex)
    await UserService.update_photo(user, new_photo.file_id)
    await message.answer(
        change_photo_message,
        reply_markup=get_main_settings_keyboard(
            user.name,
            user.age,
            sex_emoji,
            user.city,
        ),
    )
    await state.clear()


@main_settings_router.message(F.text.startswith("🧸"))
async def age_settings_handler(message: Message, state: FSMContext) -> None:
    await message.answer(age_settings_message, reply_markup=empty_keyboard)
    await state.set_state(MainSettingsState.CHANGE_AGE)


@main_settings_router.message(
    MainSettingsState.CHANGE_AGE,
    F.text.cast(int).as_("new_age"),
    F.text.cast(int).in_(range(16, 33)),
)
async def change_age_handler(
    message: Message,
    state: FSMContext,
    user: USER_MODEL,
    new_age: int,
) -> None:
    sex_emoji = EmojiHelper.get_by_sex(user.sex)
    await UserService.update_age(user, new_age)
    await message.answer(
        change_age_message,
        reply_markup=get_main_settings_keyboard(
            user.name,
            user.age,
            sex_emoji,
            user.city,
        ),
    )
    await state.clear()


@main_settings_router.message(F.text.as_("emoji"), F.text.in_({"🙋‍♀️", "🙋‍♂️"}))
async def change_sex_handler(
    message: Message,
    user: USER_MODEL,
    emoji: str,
) -> None:
    new_sex = EmojiHelper.get_opposite_sex(emoji)
    sex_emoji = EmojiHelper.get_by_sex(new_sex)
    await UserService.update_sex(user, new_sex)
    await message.answer(
        change_sex_message,
        reply_markup=get_main_settings_keyboard(
            user.name,
            user.age,
            sex_emoji,
            user.city,
        ),
    )


@main_settings_router.message(F.location.as_("location"))
async def change_location_handler(
    message: Message,
    user: USER_MODEL,
    location: Location,
) -> None:
    sex_emoji = EmojiHelper.get_by_sex(user.sex)

    try:
        new_address = await LocationHelper.get_address(
            location.latitude,
            location.longitude,
        )
    except ValidationError:
        await message.answer(change_location_not_found_message)
        return

    await UserService.update_location(user, new_address)
    await message.answer(
        change_location_message,
        reply_markup=get_main_settings_keyboard(
            user.name,
            user.age,
            sex_emoji,
            user.city,
        ),
    )
