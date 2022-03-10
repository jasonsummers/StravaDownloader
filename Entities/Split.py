from typing import Any
from dataclasses import dataclass, field
from sqlalchemy import Column, Integer, Float, Boolean, ForeignKey, String
from Entities import Base


@Base.Registry.mapped
@dataclass
class Split:
    __tablename__ = "splits"
    __sa_dataclass_metadata_key__ = "sa"

    activity_id: int = field(metadata={"sa": Column(Integer, ForeignKey("activities.id"), primary_key=True)})
    distance: float = field(metadata={"sa": Column(Float)})
    elapsed_time: int = field(metadata={"sa": Column(Integer)})
    elevation_difference: float
    moving_time: int = field(metadata={"sa": Column(Integer)})
    split: int = field(metadata={"sa": Column(Integer, primary_key=True)})
    average_speed: float = field(metadata={"sa": Column(Float)})
    pace_zone: int = field(metadata={"sa": Column(Integer)})
    average_heartrate: float = field(metadata={"sa": Column(Float)})
    is_metric: bool = field(metadata={"sa": Column(Boolean, primary_key=True)})

    @staticmethod
    def from_dict(obj: Any, activity_id: int, is_metric: bool) -> 'Split':
        _distance = float(obj.get("distance"))
        _elapsed_time = int(obj.get("elapsed_time"))
        _elevation_difference = float(obj.get("elevation_difference")) if not obj.get("elevation_difference") is None else None
        _moving_time = int(obj.get("moving_time"))
        _split = int(obj.get("split"))
        _average_speed = float(obj.get("average_speed"))
        _pace_zone = int(obj.get("pace_zone"))
        _average_heartrate = float(obj.get("average_heartrate")) if not obj.get("average_heartrate") is None else None

        return Split(activity_id, _distance, _elapsed_time, _elevation_difference, _moving_time, _split,
                     _average_speed, _pace_zone, _average_heartrate, is_metric)
