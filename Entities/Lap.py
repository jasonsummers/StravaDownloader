from typing import Any
from dataclasses import dataclass, field
from sqlalchemy import Column, Integer, Float, String, Boolean, ForeignKey
from Entities import Base


@Base.Registry.mapped
@dataclass
class Lap:
    __tablename__ = "laps"
    __sa_dataclass_metadata_key__ = "sa"

    id: int = field(metadata={"sa": Column(Integer, primary_key=True)})
    name: str = field(metadata={"sa": Column(String(50))})
    activity_id: int = field(metadata={"sa": Column(Integer, ForeignKey("activities.id"))})
    athlete_id: int = field(metadata={"sa": Column(Integer)})
    elapsed_time: int = field(metadata={"sa": Column(Integer)})
    moving_time: int = field(metadata={"sa": Column(Integer)})
    start_date: str = field(metadata={"sa": Column(String(50))})
    start_date_local: str = field(metadata={"sa": Column(String(50))})
    distance: float = field(metadata={"sa": Column(Float)})
    start_index: int = field(metadata={"sa": Column(Integer)})
    end_index: int = field(metadata={"sa": Column(Integer)})
    total_elevation_gain: int = field(metadata={"sa": Column(Integer)})
    average_speed: float = field(metadata={"sa": Column(Float)})
    max_speed: float = field(metadata={"sa": Column(Float)})
    average_cadence: float = field(metadata={"sa": Column(Float)})
    device_watts: bool = field(metadata={"sa": Column(Boolean)})
    average_watts: float = field(metadata={"sa": Column(Float)})
    lap_index: int = field(metadata={"sa": Column(Integer)})
    split: int = field(metadata={"sa": Column(Integer)})
    average_heartrate: float = field(metadata={"sa": Column(Float)})
    max_heartrate: float = field(metadata={"sa": Column(Float)})

    @staticmethod
    def from_dict(obj: Any) -> 'Lap':
        _id = int(obj.get("id"))
        _name = str(obj.get("name"))
        _activity_id = int(obj.get("activity")["id"])
        _athlete_id = int(obj.get("athlete")["id"])
        _elapsed_time = int(obj.get("elapsed_time"))
        _moving_time = int(obj.get("moving_time"))
        _start_date = str(obj.get("start_date"))
        _start_date_local = str(obj.get("start_date_local"))
        _distance = float(obj.get("distance"))
        _start_index = int(obj.get("start_index"))
        _end_index = int(obj.get("end_index"))
        _total_elevation_gain = int(obj.get("total_elevation_gain"))
        _average_speed = float(obj.get("average_speed"))
        _max_speed = float(obj.get("max_speed"))
        _average_cadence = float(obj.get("average_cadence")) if not obj.get("average_cadence") is None else None
        _device_watts = bool(obj.get("device_watts"))
        _average_watts = float(obj.get("average_watts")) if not obj.get("average_watts") is None else None
        _lap_index = int(obj.get("lap_index"))
        _split = int(obj.get("split"))
        _average_heartrate = float(obj.get("average_heartrate"))
        _max_heartrate = float(obj.get("max_heartrate"))
        return Lap(_id, _name, _activity_id, _athlete_id, _elapsed_time, _moving_time, _start_date,
                   _start_date_local, _distance, _start_index, _end_index, _total_elevation_gain, _average_speed,
                   _max_speed, _average_cadence, _device_watts, _average_watts, _lap_index, _split, _average_heartrate,
                   _max_heartrate)
