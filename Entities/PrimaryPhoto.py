from typing import Any
from dataclasses import dataclass
from Entities import PhotoUrls


@dataclass
class PrimaryPhoto:
    id: str
    activity_id: int
    unique_id: str
    urls: PhotoUrls
    source: int

    @staticmethod
    def from_dict(obj: Any) -> 'PrimaryPhoto':
        if obj is None or obj.get("id") is None:
            return

        _id = str(obj.get("id"))
        _unique_id = str(obj.get("unique_id"))
        _urls = PhotoUrls.PhotoUrls.from_dict(obj.get("urls"))
        _source = int(obj.get("source"))
        return PrimaryPhoto(_id, None, _unique_id, _urls, _source)