from typing import Any
from dataclasses import dataclass


@dataclass
class PhotoUrls:
    photo_id: int
    small_image: str
    large_image: str

    @staticmethod
    def from_dict(obj: Any) -> 'Urls':
        small_image = str(obj.get("100"))
        large_image = str(obj.get("600"))
        return PhotoUrls(None, small_image, large_image)