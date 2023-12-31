from __future__ import annotations

from typing import TYPE_CHECKING

from aiogram import F, Router
from pydantic import ValidationError

from source.database.services import UserService
from source.filters import UserFilter
from source.helpers import EmojiHelper, LocationHelper
from source.keyboards import empty_keyboard, get_main_settings_keyboard
from source.messages import (
    change_main_settings_message,
    get_age_settings_message,
    get_bio_settings_message,
    get_name_settings_message,
    get_photo_settings_message,
    location_validation_error_message,
    main_settings_message,
)
from source.states import MainSettingsState

if TYPE_CHECKING:
    from aiogram.fsm.context import FSMContext
    from aiogram.types import Location, Message, PhotoSize

    from source.database.models import UserModel

__all__ = ["main_settings_router"]

main_settings_router = Router(name=__name__)

main_settings_router.message.filter(UserFilter())


@main_settings_router.message(F.text == "🧩Основное")
async def main_settings_handler(message: Message, user: UserModel) -> None:
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
    await message.answer(get_name_settings_message, reply_markup=empty_keyboard)
    await state.set_state(MainSettingsState.CHANGE_NAME)


@main_settings_router.message(
    MainSettingsState.CHANGE_NAME,
    F.text.as_("new_name"),
    F.text.len() <= 64,
)
async def change_name_handler(
    message: Message,
    state: FSMContext,
    user: UserModel,
    new_name: str,
) -> None:
    sex_emoji = EmojiHelper.get_by_sex(user.sex)
    await UserService.update(user, name=new_name)
    await message.answer(
        change_main_settings_message,
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
    await message.answer(get_bio_settings_message, reply_markup=empty_keyboard)
    await state.set_state(MainSettingsState.CHANGE_BIO)


@main_settings_router.message(
    MainSettingsState.CHANGE_BIO,
    F.text.as_("new_bio"),
    F.text.len() <= 512,
)
async def change_bio_handler(
    message: Message,
    state: FSMContext,
    user: UserModel,
    new_bio: str,
) -> None:
    sex_emoji = EmojiHelper.get_by_sex(user.sex)
    await UserService.update(user, bio=new_bio)
    await message.answer(
        change_main_settings_message,
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
    await message.answer(
        get_photo_settings_message,
        reply_markup=empty_keyboard,
    )
    await state.set_state(MainSettingsState.CHANGE_PHOTO)


@main_settings_router.message(
    MainSettingsState.CHANGE_PHOTO,
    F.photo.pop().as_("new_photo"),
)
async def change_photo_handler(
    message: Message,
    state: FSMContext,
    user: UserModel,
    new_photo: PhotoSize,
) -> None:
    sex_emoji = EmojiHelper.get_by_sex(user.sex)
    await UserService.update(user, photo=new_photo.file_id)
    await message.answer(
        change_main_settings_message,
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
    await message.answer(get_age_settings_message, reply_markup=empty_keyboard)
    await state.set_state(MainSettingsState.CHANGE_AGE)


@main_settings_router.message(
    MainSettingsState.CHANGE_AGE,
    F.text.cast(int).as_("new_age"),
    F.text.cast(int).in_(range(16, 33)),
)
async def change_age_handler(
    message: Message,
    state: FSMContext,
    user: UserModel,
    new_age: int,
) -> None:
    sex_emoji = EmojiHelper.get_by_sex(user.sex)
    await UserService.update(user, age=new_age)
    await message.answer(
        change_main_settings_message,
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
    user: UserModel,
    emoji: str,
) -> None:
    new_sex = EmojiHelper.get_opposite_sex(emoji)
    sex_emoji = EmojiHelper.get_by_sex(new_sex)
    await UserService.update(user, sex=new_sex)
    await message.answer(
        change_main_settings_message,
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
    user: UserModel,
    location: Location,
) -> None:
    sex_emoji = EmojiHelper.get_by_sex(user.sex)

    try:
        new_address = await LocationHelper.get_address(
            location.latitude,
            location.longitude,
        )
    except ValidationError:
        await message.answer(location_validation_error_message)
        return

    await UserService.update(user, **new_address.dict())
    await message.answer(
        change_main_settings_message,
        reply_markup=get_main_settings_keyboard(
            user.name,
            user.age,
            sex_emoji,
            user.city,
        ),
    )
