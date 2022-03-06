from typing import Any
from dataclasses import dataclass
from Entities import PrimaryPhoto


@dataclass
class Photos:
    activity_id: int
    primary: PrimaryPhoto
    use_primary_photo: bool
    count: int

    @staticmethod
    def from_dict(obj: Any) -> 'Photos':
        _primary = PrimaryPhoto.PrimaryPhoto.from_dict(obj.get("primary"))
        _use_primary_photo = bool(obj.get("use_primary_photo"))
        _count = int(obj.get("count"))
        return Photos(None, _primary, _use_primary_photo, _count)