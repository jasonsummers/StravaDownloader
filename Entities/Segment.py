from typing import List
from typing import Any
from dataclasses import dataclass


@dataclass
class Segment:
    id: int
    resource_state: int
    name: str
    activity_type: str
    distance: float
    average_grade: float
    maximum_grade: float
    elevation_high: float
    elevation_low: float
    start_latlng: List[float]
    end_latlng: List[float]
    climb_category: int
    city: str
    state: str
    country: str
    private: bool
    hazardous: bool
    starred: bool

    @staticmethod
    def from_dict(obj: Any) -> 'Segment':
        _id = int(obj.get("id"))
        _resource_state = int(obj.get("resource_state"))
        _name = str(obj.get("name"))
        _activity_type = str(obj.get("activity_type"))
        _distance = float(obj.get("distance"))
        _average_grade = float(obj.get("average_grade"))
        _maximum_grade = float(obj.get("maximum_grade"))
        _elevation_high = float(obj.get("elevation_high"))
        _elevation_low = float(obj.get("elevation_low"))
        _start_latlng = [float(y) for y in obj.get("start_latlng")]
        _end_latlng = [float(y) for y in obj.get("end_latlng")]
        _climb_category = int(obj.get("climb_category"))
        _city = str(obj.get("city"))
        _state = str(obj.get("state"))
        _country = str(obj.get("country"))
        _private = bool(obj.get("private"))
        _hazardous = bool(obj.get("hazardous"))
        _starred = bool(obj.get("starred"))
        return Segment(_id, _resource_state, _name, _activity_type, _distance, _average_grade, _maximum_grade,
                       _elevation_high, _elevation_low, _start_latlng, _end_latlng, _climb_category, _city, _state,
                       _country, _private, _hazardous, _starred)
