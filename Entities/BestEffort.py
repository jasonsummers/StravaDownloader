from dataclasses import dataclass, field
from typing import Any
from sqlalchemy import Column, Integer, String, ForeignKey
from Entities import Base


@Base.Registry.mapped
@dataclass
class BestEffort:
    __tablename__ = "best_efforts"
    __sa_dataclass_metadata_key__ = "sa"

    id: int = field(metadata={"sa": Column(Integer, primary_key=True)})
    name: str = field(metadata={"sa": Column(String(50))})
    activity_id: int = field(metadata={"sa": Column(Integer, ForeignKey("activities.id"))})
    athlete_id: int = field(metadata={"sa": Column(Integer, ForeignKey("athletes.id"))})
    elapsed_time: int = field(metadata={"sa": Column(Integer)})
    moving_time: int = field(metadata={"sa": Column(Integer)})
    start_date: str = field(metadata={"sa": Column(String(50))})
    start_date_local: str = field(metadata={"sa": Column(String(50))})
    distance: int = field(metadata={"sa": Column(Integer)})
    start_index: int = field(metadata={"sa": Column(Integer)})
    end_index: int = field(metadata={"sa": Column(Integer)})
    pr_rank: int = field(metadata={"sa": Column(Integer)})

    @staticmethod
    def from_dict(obj: Any) -> 'BestEffort':
        _id = int(obj.get("id"))
        _name = str(obj.get("name"))
        _activity_id = int(obj.get("activity")["id"])
        _athlete_id = int(obj.get("athlete")["id"])
        _elapsed_time = int(obj.get("elapsed_time"))
        _moving_time = int(obj.get("moving_time"))
        _start_date = str(obj.get("start_date"))
        _start_date_local = str(obj.get("start_date_local"))
        _distance = int(obj.get("distance"))
        _start_index = int(obj.get("start_index"))
        _end_index = int(obj.get("end_index"))
        _pr_rank = int(obj.get("pr_rank")) if not obj.get("pr_rank") is None else 0
        return BestEffort(_id, _name, _activity_id, _athlete_id, _elapsed_time, _moving_time, _start_date,
                          _start_date_local, _distance, _start_index, _end_index, _pr_rank)

