from __future__ import annotations

from typing import TYPE_CHECKING

from aiogram import F, Router
from aiogram.filters import StateFilter

from source.database.services import UserService
from source.filters import UserFilter
from source.helpers import EmojiHelper
from source.keyboards import (
    empty_keyboard,
    get_filter_settings_keyboard,
    need_sex_keyboard,
)
from source.messages import (
    change_filter_settings_message,
    filter_settings_message,
    get_need_age_settings_message,
    get_need_sex_settings_message,
)
from source.states import FilterSettingsState

if TYPE_CHECKING:
    from aiogram.fsm.context import FSMContext
    from aiogram.types import Message

    from source.database.models import UserModel

__all__ = ["filter_settings_router"]

filter_settings_router = Router(name="Filter Settings Router")

filter_settings_router.message.filter(UserFilter())


@filter_settings_router.message(F.text == "🔎Фильтры")
async def filter_settings_handler(message: Message, user: UserModel) -> None:
    sex_emoji = EmojiHelper.get_by_sex(user.need_sex)
    await message.answer(
        filter_settings_message,
        reply_markup=get_filter_settings_keyboard(user.need_age, sex_emoji),
    )


@filter_settings_router.message(F.text.startswith("🔎🧸"))
async def need_age_settings_handler(
    message: Message,
    state: FSMContext,
) -> None:
    await message.answer(
        get_need_age_settings_message,
        reply_markup=empty_keyboard,
    )
    await state.set_state(FilterSettingsState.CHANGE_NEED_AGE)


@filter_settings_router.message(
    FilterSettingsState.CHANGE_NEED_AGE,
    F.text.cast(int).as_("new_need_age"),
    F.text.cast(int).in_(range(16, 33)),
)
async def change_need_age_handler(
    message: Message,
    state: FSMContext,
    user: UserModel,
    new_need_age: int,
) -> None:
    sex_emoji = EmojiHelper.get_by_sex(user.need_sex)
    await UserService.update_need_age(user, new_need_age)
    await message.answer(
        change_filter_settings_message,
        reply_markup=get_filter_settings_keyboard(user.need_age, sex_emoji),
    )
    await state.clear()


@filter_settings_router.message(
    ~StateFilter(FilterSettingsState.CHANGE_NEED_SEX),
    F.text.in_({"🔎🙋‍♀️", "🔎🙋‍♂️", "🔎❤️"}),
)
async def need_sex_settings_handler(
    message: Message,
    state: FSMContext,
) -> None:
    await message.answer(
        get_need_sex_settings_message,
        reply_markup=need_sex_keyboard,
    )
    await state.set_state(FilterSettingsState.CHANGE_NEED_SEX)


@filter_settings_router.message(
    FilterSettingsState.CHANGE_NEED_SEX,
    F.text.as_("emoji"),
    F.text.in_({"🔎🙋‍♀️", "🔎🙋‍♂️", "🔎❤️"}),
)
async def change_sex_handler(
    message: Message,
    state: FSMContext,
    user: UserModel,
    emoji: str,
) -> None:
    new_need_sex = EmojiHelper.get_sex(emoji[1:])
    sex_emoji = EmojiHelper.get_by_sex(new_need_sex)
    await UserService.update_need_sex(user, new_need_sex)
    await message.answer(
        change_filter_settings_message,
        reply_markup=get_filter_settings_keyboard(user.need_age, sex_emoji),
    )
    await state.clear()
