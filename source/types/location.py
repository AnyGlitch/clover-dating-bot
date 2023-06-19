from pydantic import BaseModel

__all__ = ["Address"]


class Address(BaseModel):
    country: str
    state: str
    city: str
    latitude: float
    longitude: float
