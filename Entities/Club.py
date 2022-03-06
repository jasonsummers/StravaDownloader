from typing import List
from typing import Any
from dataclasses import dataclass


@dataclass
class Club:
    id: int
    resource_state: int
    name: str
    profile_medium: str
    profile: str
    cover_photo: str
    cover_photo_small: str
    activity_types: List[str]
    activity_types_icon: str
    dimensions: List[str]
    sport_type: str
    city: str
    state: str
    country: str
    private: bool
    member_count: int
    featured: bool
    verified: bool
    url: str
    membership: str
    admin: bool
    owner: bool

    @staticmethod
    def from_dict(obj: Any) -> 'Club':
        _id = int(obj.get("id"))
        _resource_state = int(obj.get("resource_state"))
        _name = str(obj.get("name"))
        _profile_medium = str(obj.get("profile_medium"))
        _profile = str(obj.get("profile"))
        _cover_photo = str(obj.get("cover_photo"))
        _cover_photo_small = str(obj.get("cover_photo_small"))
        _activity_types = [str(y) for y in obj.get("activity_types")]
        _activity_types_icon = str(obj.get("activity_types_icon"))
        _dimensions = [str(y) for y in obj.get("dimensions")]
        _sport_type = str(obj.get("sport_type"))
        _city = str(obj.get("city"))
        _state = str(obj.get("state"))
        _country = str(obj.get("country"))
        _private = bool(obj.get("private"))
        _member_count = int(obj.get("member_count"))
        _featured = bool(obj.get("featured"))
        _verified = bool(obj.get("verified"))
        _url = str(obj.get("url"))
        _membership = str(obj.get("membership"))
        _admin = bool(obj.get("admin"))
        _owner = bool(obj.get("owner"))
        return Club(_id, _resource_state, _name, _profile_medium, _profile, _cover_photo, _cover_photo_small,
                    _activity_types, _activity_types_icon, _dimensions, _sport_type, _city, _state, _country, _private,
                    _member_count, _featured, _verified, _url, _membership, _admin, _owner)