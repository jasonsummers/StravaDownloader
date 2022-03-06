from typing import Any
from dataclasses import dataclass
from Entities import Segment


@dataclass
class SegmentEffort:
    id: float
    resource_state: int
    name: str
    activity_id: int
    athlete_id: int
    elapsed_time: int
    moving_time: int
    start_date: str
    start_date_local: str
    distance: float
    start_index: int
    end_index: int
    average_cadence: float
    device_watts: bool
    average_watts: float
    segment: Segment.Segment
    kom_rank: int
    pr_rank: int
    hidden: bool
    average_heartrate: float
    max_heartrate: float
    segment_id: int

    @staticmethod
    def from_dict(obj: Any) -> 'SegmentEffort':
        _id = float(obj.get("id"))
        _resource_state = int(obj.get("resource_state"))
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
        _average_heartrate = float(obj.get("average_heartrate"))
        _max_heartrate = float(obj.get("max_heartrate"))
        _segment_id = _segment.id
        return SegmentEffort(_id, _resource_state, _name, _activity_id, _athlete_id, _elapsed_time, _moving_time, _start_date,
                             _start_date_local, _distance, _start_index, _end_index, _average_cadence, _device_watts,
                             _average_watts, _segment, _kom_rank, _pr_rank, _hidden, _average_heartrate, _max_heartrate,
                             _segment_id)
