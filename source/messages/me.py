__all__ = ["get_me_message"]


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
