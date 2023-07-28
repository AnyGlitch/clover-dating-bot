from aiogram import Bot, Dispatcher, F
from aiogram.enums import ChatType
from aiogram.fsm.storage.redis import RedisStorage

from source.config import GROUP_TOKEN, REDIS_URL
from source.database.engine import close_orm, init_orm
from source.routers import (
    back_router,
    filter_settings_router,
    forbidden_error_router,
    main_settings_router,
    me_router,
    request_error_router,
    search_router,
    sign_up_router,
    start_settings_router,
)

__all__ = ["main"]


def main() -> None:
    bot = Bot(GROUP_TOKEN)

    storage = RedisStorage.from_url(REDIS_URL)

    dp = Dispatcher(storage=storage)

    dp.message.filter(F.chat.type == ChatType.PRIVATE)

    dp.startup.register(init_orm)
    dp.shutdown.register(close_orm)

    dp.include_routers(
        sign_up_router,
        me_router,
        search_router,
        start_settings_router,
        main_settings_router,
        filter_settings_router,
        back_router,
        forbidden_error_router,
        request_error_router,
    )

    dp.run_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == "__main__":
    main()
