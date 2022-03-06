from typing import Any
from dataclasses import dataclass


@dataclass
class Gear:
    id: str
    activity_id: int
    primary: bool
    name: str
    nickname: str
    resource_state: int
    retired: bool
    distance: int
    converted_distance: float

    @staticmethod
    def from_activity_dict(obj: Any) -> 'Gear':
        if obj is None or obj.get("id") is None:
            return

        _id = str(obj.get("id"))
        _primary = bool(obj.get("primary"))
        _name = str(obj.get("name"))
        _resource_state = int(obj.get("resource_state"))
        _distance = int(obj.get("distance"))
        return Gear(_id, None, _primary, _name, None, _resource_state, None, _distance, None)

    @staticmethod
    def from_athlete_dict(obj: Any) -> 'Bike':
        _id = str(obj.get("id"))
        _primary = bool(obj.get("primary"))
        _name = str(obj.get("name"))
        _nickname = str(obj.get("nickname"))
        _resource_state = int(obj.get("resource_state"))
        _retired = bool(obj.get("retired"))
        _distance = int(obj.get("distance"))
        _converted_distance = float(obj.get("converted_distance"))
        return Gear(_id, None, _primary, _name, _nickname, _resource_state, _retired, _distance, _converted_distance)
