from __future__ import annotations

from geopy.adapters import AioHTTPAdapter
from geopy.extra.rate_limiter import AsyncRateLimiter
from geopy.geocoders import Nominatim

from source.types import Address

__all__ = ["LocationHelper"]


class LocationHelper:
    @staticmethod
    async def get_address(latitude: float, longitude: float) -> Address:
        async with Nominatim(
            user_agent="whyglitches@gmail",
            adapter_factory=AioHTTPAdapter,
        ) as geolocator:
            geocode = AsyncRateLimiter(geolocator.geocode, min_delay_seconds=5)
            location = await geocode(
                f"{latitude}, {longitude}",
                language="ru",
                addressdetails=True,
            )
        data = location.raw["address"]
        return Address(
            country=data["country"],
            state=data["state"],
            city=data.get("city") or data.get("town"),
            latitude=latitude,
            longitude=longitude,
        )
