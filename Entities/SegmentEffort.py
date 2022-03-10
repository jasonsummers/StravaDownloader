from typing import Any
from dataclasses import dataclass, field
from sqlalchemy import Column, Integer, Float, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from Entities import Segment, Base


@Base.Registry.mapped
@dataclass
class SegmentEffort:
    __tablename__ = "segment_efforts"
    __sa_dataclass_metadata_key__ = "sa"

    id: int = field(metadata={"sa": Column(Integer, primary_key=True)})
    name: str = field(metadata={"sa": Column(String(50))})
    activity_id: int = field(metadata={"sa": Column(Integer, ForeignKey("activities.id"))})
    athlete_id: int = field(metadata={"sa": Column(Integer, ForeignKey("athletes.id"))})
    elapsed_time: int = field(metadata={"sa": Column(Integer)})
    moving_time: int = field(metadata={"sa": Column(Integer)})
    start_date: str = field(metadata={"sa": Column(String(50))})
    start_date_local: str = field(metadata={"sa": Column(String(50))})
    distance: float = field(metadata={"sa": Column(Float)})
    start_index: int = field(metadata={"sa": Column(Integer)})
    end_index: int = field(metadata={"sa": Column(Integer)})
    average_cadence: float = field(metadata={"sa": Column(Float)})
    device_watts: bool = field(metadata={"sa": Column(Boolean)})
    average_watts: float = field(metadata={"sa": Column(Float)})
    segment: Segment = field(metadata={"sa": relationship("Segment",
                                                          primaryjoin="and_(SegmentEffort.segment_id==Segment.id)",
                                                          uselist=False)})
    kom_rank: int = field(metadata={"sa": Column(Integer)})
    pr_rank: int = field(metadata={"sa": Column(Integer)})
    hidden: bool = field(metadata={"sa": Column(Boolean)})
    average_heartrate: float = field(metadata={"sa": Column(Float)})
    max_heartrate: float = field(metadata={"sa": Column(Float)})
    segment_id: int = field(metadata={"sa": Column(Integer)})

    @staticmethod
    def from_dict(obj: Any) -> 'SegmentEffort':
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
        _average_cadence = float(obj.get("average_cadence")) if not obj.get("average_cadence") is None else None
        _device_watts = bool(obj.get("device_watts"))
        _average_watts = float(obj.get("average_watts")) if not obj.get("average_watts") is None else None
        _segment = Segment.Segment.from_dict(obj.get("segment"))
        _kom_rank = int(obj.get("kom_rank")) if not obj.get("kom_rank") is None else None
        _pr_rank = int(obj.get("pr_rank")) if not obj.get("pr_rank") is None else None
        _hidden = bool(obj.get("hidden"))
        _average_heartrate = float(obj.get("average_heartrate")) if not obj.get("average_heartrate") is None else None
        _max_heartrate = float(obj.get("max_heartrate")) if not obj.get("max_heartrate") is None else None
        _segment_id = _segment.id
        return SegmentEffort(_id, _name, _activity_id, _athlete_id, _elapsed_time, _moving_time, _start_date,
                             _start_date_local, _distance, _start_index, _end_index, _average_cadence, _device_watts,
                             _average_watts, _segment, _kom_rank, _pr_rank, _hidden, _average_heartrate, _max_heartrate,
                             _segment_id)
