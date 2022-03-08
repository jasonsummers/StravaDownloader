from typing import Any
from dataclasses import dataclass, field
from sqlalchemy import Column, Integer, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from Entities import PrimaryPhoto, Base


@Base.Registry.mapped
@dataclass
class Photos:
    __tablename__ = "photos"
    __sa_dataclass_metadata_key__ = "sa"

    id: int = field(init=False, metadata={"sa": Column(Integer, primary_key=True)})
    activity_id: int = field(metadata={"sa": Column(Integer, ForeignKey("activities.id"))})
    primary: PrimaryPhoto = field(metadata={"sa": relationship("PrimaryPhoto")})
    use_primary_photo: bool = field(metadata={"sa": Column(Boolean)})
    count: int = field(metadata={"sa": Column(Integer)})

    @staticmethod
    def from_dict(obj: Any) -> 'Photos':
        _primary = PrimaryPhoto.from_dict(obj.get("primary"))
        _use_primary_photo = bool(obj.get("use_primary_photo"))
        _count = int(obj.get("count"))
        return Photos(None, _primary, _use_primary_photo, _count)
