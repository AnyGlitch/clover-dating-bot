from source.routers.back import back_router
from source.routers.me import me_router
from source.routers.search import search_router
from source.routers.settings import (
    filter_settings_router,
    main_settings_router,
    start_settings_router,
)
from source.routers.sign_up import sign_up_router

__all__ = [
    "back_router",
    "filter_settings_router",
    "main_settings_router",
    "me_router",
    "search_router",
    "sign_up_router",
    "start_settings_router",
]
