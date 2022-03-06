from typing import Any
from dataclasses import dataclass


@dataclass
class Split:
    activity_id: int
    distance: float
    elapsed_time: int
    elevation_difference: float
    moving_time: int
    split: int
    average_speed: float
    pace_zone: int
    average_heartrate: float

    @staticmethod
    def from_dict(obj: Any) -> 'Split':
        _distance = float(obj.get("distance"))
        _elapsed_time = int(obj.get("elapsed_time"))
        _elevation_difference = float(obj.get("elevation_difference")) if not obj.get("elevation_difference") is None else None
        _moving_time = int(obj.get("moving_time"))
        _split = int(obj.get("split"))
        _average_speed = float(obj.get("average_speed"))
        _pace_zone = int(obj.get("pace_zone"))
        _average_heartrate = float(obj.get("average_heartrate"))
        return Split(None, _distance, _elapsed_time, _elevation_difference, _moving_time, _split, _average_speed,
                     _pace_zone, _average_heartrate)