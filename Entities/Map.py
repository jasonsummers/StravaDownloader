from typing import Any
from dataclasses import dataclass, field
from sqlalchemy import Column, String, Text, Integer, ForeignKey
from Entities import Base


@Base.Registry.mapped
@dataclass
class Map:
    __tablename__ = "maps"
    __sa_dataclass_metadata_key__ = "sa"

    id: str = field(metadata={"sa": Column(String(25), primary_key=True)})
    activity_id: int = field(metadata={"sa": Column(Integer, ForeignKey('activities.id'))})
    polyline: str = field(metadata={"sa": Column(Text)})
    summary_polyline: str = field(metadata={"sa": Column(Text)})

    @staticmethod
    def from_dict(obj: Any) -> 'Map':
        _id = str(obj.get("id"))
        _polyline = str(obj.get("polyline"))
        _summary_polyline = str(obj.get("summary_polyline"))
        return Map(_id, _polyline, _summary_polyline)
