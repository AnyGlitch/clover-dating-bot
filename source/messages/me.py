__all__ = ["bad_photo_message", "get_me_message"]

bad_photo_message = "С твоей фотографией что-то не так, отправь мне новую:"


def get_me_message(
    name: str,
    age: int,
    city: str,
    bio: str | None = None,
) -> str:
    short_info_message = f"{name}, {age} y.o, {city}"
    if bio:
        short_info_message += f" - {bio}"
    return short_info_message
