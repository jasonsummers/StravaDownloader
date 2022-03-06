from typing import List
from typing import Any
from dataclasses import dataclass
from Entities import Club, Gear


@dataclass
class Athlete:
    id: int
    username: str
    resource_state: int
    firstname: str
    lastname: str
    bio: str
    city: str
    state: str
    country: str
    sex: str
    premium: bool
    summit: bool
    created_at: str
    updated_at: str
    badge_type_id: int
    weight: float
    profile_medium: str
    profile: str
    friend: bool
    follower: bool
    blocked: bool
    can_follow: bool
    follower_count: int
    friend_count: int
    mutual_friend_count: int
    athlete_type: int
    date_preference: str
    measurement_preference: str
    clubs: List[Club.Club]
    ftp: str
    bikes: List[Bike.Bike]
    shoes: List[Shoe.Shoe]

    @staticmethod
    def from_dict(obj: Any) -> 'Athlete':
        _id = int(obj.get("id"))
        _username = str(obj.get("username"))
        _resource_state = int(obj.get("resource_state"))
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
        _clubs = [Club.Club.from_dict(y) for y in obj.get("clubs")]
        _ftp = str(obj.get("ftp"))
        _bikes = [Gear.Gear.from_athlete_dict(y) for y in obj.get("bikes")]
        _shoes = [Gear.Gear.from_athlete_dict(y) for y in obj.get("shoes")]
        return Athlete(_id, _username, _resource_state, _firstname, _lastname, _bio, _city, _state, _country, _sex,
                       _premium, _summit, _created_at, _updated_at, _badge_type_id, _weight, _profile_medium, _profile,
                       _friend, _follower, _blocked, _can_follow, _follower_count, _friend_count, _mutual_friend_count,
                       _athlete_type, _date_preference, _measurement_preference, _clubs, _ftp, _bikes, _shoes)