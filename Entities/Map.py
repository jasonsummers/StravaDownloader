from typing import List
from typing import Any
from dataclasses import dataclass


@dataclass
class Map:
    id: str
    polyline: str
    summary_polyline: str

    @staticmethod
    def from_dict(obj: Any) -> 'Map':
        _id = str(obj.get("id"))
        _polyline = str(obj.get("polyline"))
        _summary_polyline = str(obj.get("summary_polyline"))
        return Map(_id, _polyline, _summary_polyline)