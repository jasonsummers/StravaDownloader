from typing import Any
from dataclasses import dataclass


@dataclass
class Lap:
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
    total_elevation_gain: int
    average_speed: float
    max_speed: float
    average_cadence: float
    device_watts: bool
    average_watts: float
    lap_index: int
    split: int
    average_heartrate: float
    max_heartrate: float

    @staticmethod
    def from_dict(obj: Any) -> 'Lap':
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
        return Lap(_id, _resource_state, _name, _activity_id, _athlete_id, _elapsed_time, _moving_time, _start_date,
                   _start_date_local, _distance, _start_index, _end_index, _total_elevation_gain, _average_speed,
                   _max_speed, _average_cadence, _device_watts, _average_watts, _lap_index, _split, _average_heartrate,
                   _max_heartrate)
