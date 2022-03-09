from typing import Any
from dataclasses import dataclass, field
from sqlalchemy import Column, Integer, Float, String, Boolean, ForeignKey
from Entities import Base


@Base.Registry.mapped
@dataclass
class Gear:
    __tablename__ = "gear"
    __sa_dataclass_metadata_key__ = "sa"

    id: str = field(metadata={"sa": Column(String(25), ForeignKey("activities.gear_id"), primary_key=True)})
    athlete_id: int = field(init=False, metadata={"sa": Column(Integer, ForeignKey("athletes.id"))})
    primary: bool = field(metadata={"sa": Column(Boolean)})
    gear_type: str = field(metadata={"sa": Column(String(4))})
    name: str = field(metadata={"sa": Column(String(50))})
    nickname: str = field(metadata={"sa": Column(String(50))})
    retired: bool = field(metadata={"sa": Column(Boolean)})
    distance: int = field(metadata={"sa": Column(Integer)})
    converted_distance: float = field(metadata={"sa": Column(Float)})

    @staticmethod
    def from_activity_dict(obj: Any) -> 'Gear':
        if obj is None or obj.get("id") is None:
            return

        _id = str(obj.get("id"))
        _primary = bool(obj.get("primary"))
        _name = str(obj.get("name"))
        _distance = int(obj.get("distance"))
        return Gear(_id, _primary, None, _name, None, None, _distance, None)

    @staticmethod
    def from_athlete_dict(obj: Any, gear_type: str) -> 'Gear':
        _id = str(obj.get("id"))
        _primary = bool(obj.get("primary"))
        _name = str(obj.get("name"))
        _nickname = str(obj.get("nickname"))
        _retired = bool(obj.get("retired"))
        _distance = int(obj.get("distance"))
        _converted_distance = float(obj.get("converted_distance"))
        return Gear(_id, _primary, gear_type, _name, _nickname, _retired, _distance, _converted_distance)
