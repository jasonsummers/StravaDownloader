from typing import Any
from dataclasses import dataclass, field
from sqlalchemy import Column, Integer, String, ForeignKey

from Entities import Base


@Base.Registry.mapped
@dataclass
class PrimaryPhoto:
    __tablename__ = "primary_photo"
    __sa_dataclass_metadata_key__ = "sa"

    unique_id: str = field(metadata={"sa": Column(String(50), primary_key=True)})
    photos_id: int = field(init=False, metadata={"sa": Column(Integer, ForeignKey("photos.id"))})
    small_url: str = field(metadata={"sa": Column(String(250))})
    large_url: str = field(metadata={"sa": Column(String(250))})
    source: int = field(metadata={"sa": Column(Integer)})

    @staticmethod
    def from_dict(obj: Any) -> 'PrimaryPhoto':
        if obj is None or obj.get("unique_id") is None:
            return

        _unique_id = str(obj.get("unique_id"))
        _small_url = str(obj.get("urls")["100"])
        _large_url = str(obj.get("urls")["600"])
        _source = int(obj.get("source"))
        return PrimaryPhoto(_unique_id, _small_url, _large_url, _source)
