from typing import Any
from dataclasses import dataclass, field
from sqlalchemy import Column, Integer, Float, String, Boolean
from Entities import Base


@Base.Registry.mapped
@dataclass
class Segment:
    __tablename__ = "segments"
    __sa_dataclass_metadata_key__ = "sa"

    id: int = field(metadata={"sa": Column(Integer, primary_key=True)})
    name: str = field(metadata={"sa": Column(String(50))})
    activity_type: str = field(metadata={"sa": Column(String(10))})
    distance: float = field(metadata={"sa": Column(Float)})
    average_grade: float = field(metadata={"sa": Column(Float)})
    maximum_grade: float = field(metadata={"sa": Column(Float)})
    elevation_high: float = field(metadata={"sa": Column(Float)})
    elevation_low: float = field(metadata={"sa": Column(Float)})
    start_lat: float = field(metadata={"sa": Column(Float)})
    start_lng: float = field(metadata={"sa": Column(Float)})
    end_lat: float = field(metadata={"sa": Column(Float)})
    end_lng: float = field(metadata={"sa": Column(Float)})
    climb_category: int = field(metadata={"sa": Column(Integer)})
    city: str = field(metadata={"sa": Column(String(50))})
    state: str = field(metadata={"sa": Column(String(50))})
    country: str = field(metadata={"sa": Column(String(50))})
    private: bool = field(metadata={"sa": Column(Boolean)})
    hazardous: bool = field(metadata={"sa": Column(Boolean)})
    starred: bool = field(metadata={"sa": Column(Boolean)})

    @staticmethod
    def from_dict(obj: Any) -> 'Segment':
        _id = int(obj.get("id"))
        _name = str(obj.get("name"))
        _activity_type = str(obj.get("activity_type"))
        _distance = float(obj.get("distance"))
        _average_grade = float(obj.get("average_grade"))
        _maximum_grade = float(obj.get("maximum_grade"))
        _elevation_high = float(obj.get("elevation_high"))
        _elevation_low = float(obj.get("elevation_low"))
        _start_lat = float(obj.get("start_latlng")[0])
        _start_lng = float(obj.get("start_latlng")[1])
        _end_lat = float(obj.get("end_latlng")[0])
        _end_lng = float(obj.get("end_latlng")[1])
        _climb_category = int(obj.get("climb_category"))
        _city = str(obj.get("city"))
        _state = str(obj.get("state"))
        _country = str(obj.get("country"))
        _private = bool(obj.get("private"))
        _hazardous = bool(obj.get("hazardous"))
        _starred = bool(obj.get("starred"))

        return Segment(_id, _name, _activity_type, _distance, _average_grade, _maximum_grade, _elevation_high,
                       _elevation_low, _start_lat, _start_lng, _end_lat, _end_lng, _climb_category, _city, _state,
                       _country, _private, _hazardous, _starred)
