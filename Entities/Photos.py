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

    id: int = field(metadata={"sa": Column(Integer, primary_key=True)})
    activity_id: int = field(metadata={"sa": Column(Integer, ForeignKey("activities.id"))})
    primary: PrimaryPhoto = field(metadata={"sa": relationship("PrimaryPhoto", uselist=False)})
    use_primary_photo: bool = field(metadata={"sa": Column(Boolean)})
    count: int = field(metadata={"sa": Column(Integer)})

    @staticmethod
    def from_dict(obj: Any, activity_id: int) -> 'Photos':
        if obj is None or obj.get("id") is None:
            return

        _count = int(obj.get("count"))

        if _count == 0:
            return

        _primary = PrimaryPhoto.PrimaryPhoto.from_dict(obj.get("primary"))
        _use_primary_photo = bool(obj.get("use_primary_photo"))
        return Photos(activity_id, activity_id, _primary, _use_primary_photo, _count)
