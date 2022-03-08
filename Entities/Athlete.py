from typing import List
from typing import Any
from dataclasses import dataclass, field
from sqlalchemy import Column, Integer, Float, String, Boolean
from sqlalchemy.orm import relationship
from Entities import Gear, Base


@Base.Registry.mapped
@dataclass
class Athlete:
    __tablename__ = "athletes"
    __sa_dataclass_metadata_key__ = "sa"

    id: int = field(metadata={"sa": Column(Integer, primary_key=True)})
    username: str = field(metadata={"sa": Column(String(50))})
    firstname: str = field(metadata={"sa": Column(String(50))})
    lastname: str = field(metadata={"sa": Column(String(50))})
    bio: str = field(metadata={"sa": Column(String(500))})
    city: str = field(metadata={"sa": Column(String(50))})
    state: str = field(metadata={"sa": Column(String(50))})
    country: str = field(metadata={"sa": Column(String(50))})
    sex: str = field(metadata={"sa": Column(String(10))})
    premium: bool = field(metadata={"sa": Column(Boolean)})
    summit: bool = field(metadata={"sa": Column(Boolean)})
    created_at: str = field(metadata={"sa": Column(String(50))})
    updated_at: str = field(metadata={"sa": Column(String(50))})
    badge_type_id: int = field(metadata={"sa": Column(Integer)})
    weight: float = field(metadata={"sa": Column(Float)})
    profile_medium: str = field(metadata={"sa": Column(String(50))})
    profile: str = field(metadata={"sa": Column(String(500))})
    friend: bool = field(metadata={"sa": Column(Boolean)})
    follower: bool = field(metadata={"sa": Column(Boolean)})
    blocked: bool = field(metadata={"sa": Column(Boolean)})
    can_follow: bool = field(metadata={"sa": Column(Boolean)})
    follower_count: int = field(metadata={"sa": Column(Integer)})
    friend_count: int = field(metadata={"sa": Column(Integer)})
    mutual_friend_count: int = field(metadata={"sa": Column(Integer)})
    athlete_type: int = field(metadata={"sa": Column(Integer)})
    date_preference: str = field(metadata={"sa": Column(String(50))})
    measurement_preference: str = field(metadata={"sa": Column(String(50))})
    ftp: str = field(metadata={"sa": Column(String(50))})
    bikes: List[Gear.Gear] = field(default_factory=list, metadata={
        "sa": relationship("Gear", primaryjoin="and_(Athlete.id==Gear.athlete_id, Gear.gear_type=='bike'")})
    shoes: List[Gear.Gear] = field(default_factory=list, metadata={
        "sa": relationship("Gear", primaryjoin="and_(Athlete.id==Gear.athlete_id, Gear.gear_type=='shoe'")})

    @staticmethod
    def from_dict(obj: Any) -> 'Athlete':
        _id = int(obj.get("id"))
        _username = str(obj.get("username"))
        _firstname = str(obj.get("firstname"))
        _lastname = str(obj.get("lastname"))
        _bio = str(obj.get("bio"))
        _city = str(obj.get("city"))
        _state = str(obj.get("state"))
        _country = str(obj.get("country"))
        _sex = str(obj.get("sex"))
        _premium = bool(obj.get("premium"))
        _summit = bool(obj.get("summit"))
        _created_at = str(obj.get("created_at"))
        _updated_at = str(obj.get("updated_at"))
        _badge_type_id = int(obj.get("badge_type_id"))
        _weight = float(obj.get("weight"))
        _profile_medium = str(obj.get("profile_medium"))
        _profile = str(obj.get("profile"))
        _friend = bool(obj.get("friend"))
        _follower = bool(obj.get("follower"))
        _blocked = bool(obj.get("blocked"))
        _can_follow = bool(obj.get("can_follow"))
        _follower_count = int(obj.get("follower_count"))
        _friend_count = int(obj.get("friend_count"))
        _mutual_friend_count = int(obj.get("mutual_friend_count"))
        _athlete_type = int(obj.get("athlete_type"))
        _date_preference = str(obj.get("date_preference"))
        _measurement_preference = str(obj.get("measurement_preference"))
        _ftp = str(obj.get("ftp"))
        _bikes = [Gear.from_athlete_dict(y, "bike") for y in obj.get("bikes")]
        _shoes = [Gear.from_athlete_dict(y, "shoe") for y in obj.get("shoes")]
        return Athlete(_id, _username, _firstname, _lastname, _bio, _city, _state, _country, _sex,
                       _premium, _summit, _created_at, _updated_at, _badge_type_id, _weight, _profile_medium, _profile,
                       _friend, _follower, _blocked, _can_follow, _follower_count, _friend_count, _mutual_friend_count,
                       _athlete_type, _date_preference, _measurement_preference, _ftp, _bikes, _shoes)
