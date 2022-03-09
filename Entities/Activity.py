from typing import List
from typing import Any
from dataclasses import dataclass, field
from sqlalchemy import Column, Integer, Float, String, Boolean
from sqlalchemy.orm import relationship
from Entities import Gear, HighlightedKudoser, Lap, Map, Photos, SegmentEffort, Split, Base, Kudoser, Comment


@Base.Registry.mapped
@dataclass
class Activity:
    __tablename__ = "activities"
    __sa_dataclass_metadata_key__ = "sa"

    id: int = field(metadata={"sa": Column(Integer, primary_key=True)})
    external_id: str = field(metadata={"sa": Column(String(50))})
    upload_id: int = field(metadata={"sa": Column(Integer)})
    athlete_id: int = field(metadata={"sa": Column(Integer)})
    name: str = field(metadata={"sa": Column(String(100))})
    distance: int = field(metadata={"sa": Column(Integer)})
    moving_time: int = field(metadata={"sa": Column(Integer)})
    elapsed_time: int = field(metadata={"sa": Column(Integer)})
    total_elevation_gain: int = field(metadata={"sa": Column(Integer)})
    type: str = field(metadata={"sa": Column(String(25))})
    start_date: str = field(metadata={"sa": Column(String(50))})
    start_date_local: str = field(metadata={"sa": Column(String(50))})
    timezone: str = field(metadata={"sa": Column(String(25))})
    utc_offset: float = field(metadata={"sa": Column(Float)})
    start_lat: float = field(metadata={"sa": Column(Float)})
    start_lng: float = field(metadata={"sa": Column(Float)})
    end_lat: float = field(metadata={"sa": Column(Float)})
    end_lng: float = field(metadata={"sa": Column(Float)})
    achievement_count: int = field(metadata={"sa": Column(Integer)})
    kudos_count: int = field(metadata={"sa": Column(Integer)})
    comment_count: int = field(metadata={"sa": Column(Integer)})
    athlete_count: int = field(metadata={"sa": Column(Integer)})
    photo_count: int = field(metadata={"sa": Column(Integer)})
    map: Map = field(metadata={"sa": relationship("Map", uselist=False)})
    trainer: bool = field(metadata={"sa": Column(Boolean)})
    commute: bool = field(metadata={"sa": Column(Boolean)})
    manual: bool = field(metadata={"sa": Column(Boolean)})
    private: bool = field(metadata={"sa": Column(Boolean)})
    flagged: bool = field(metadata={"sa": Column(Boolean)})
    gear_id: str = field(metadata={"sa": Column(String(25))})
    from_accepted_tag: bool = field(metadata={"sa": Column(Boolean)})
    average_speed: float = field(metadata={"sa": Column(Float)})
    max_speed: float = field(metadata={"sa": Column(Float)})
    average_cadence: float = field(metadata={"sa": Column(Float)})
    average_temp: int = field(metadata={"sa": Column(Integer)})
    average_watts: float = field(metadata={"sa": Column(Float)})
    weighted_average_watts: int = field(metadata={"sa": Column(Integer)})
    kilojoules: float = field(metadata={"sa": Column(Float)})
    device_watts: bool = field(metadata={"sa": Column(Boolean)})
    has_heartrate: bool = field(metadata={"sa": Column(Boolean)})
    max_watts: int = field(metadata={"sa": Column(Integer)})
    elev_high: float = field(metadata={"sa": Column(Float)})
    elev_low: float = field(metadata={"sa": Column(Float)})
    pr_count: int = field(metadata={"sa": Column(Integer)})
    total_photo_count: int = field(metadata={"sa": Column(Integer)})
    has_kudoed: bool = field(metadata={"sa": Column(Boolean)})
    workout_type: int = field(metadata={"sa": Column(Integer)})
    suffer_score: str = field(metadata={"sa": Column(String(25))})
    description: str = field(metadata={"sa": Column(String(25))})
    calories: float = field(metadata={"sa": Column(Float)})
    gear: Gear = field(metadata={"sa": relationship("Gear", primaryjoin="and_(Activity.gear_id==Gear.id)",
                                                    uselist=False)})
    partner_brand_tag: str = field(metadata={"sa": Column(String(50))})
    photos: Photos = field(metadata={"sa": relationship("Photos", uselist=False)})
    hide_from_home: bool = field(metadata={"sa": Column(Boolean)})
    device_name: str = field(metadata={"sa": Column(String(50))})
    embed_token: str = field(metadata={"sa": Column(String(50))})
    segment_leaderboard_opt_out: bool = field(metadata={"sa": Column(Boolean)})
    leaderboard_opt_out: bool = field(metadata={"sa": Column(Boolean)})
    average_heartrate: float = field(metadata={"sa": Column(Float)})
    max_heartrate: float = field(metadata={"sa": Column(Float)})

    segment_efforts: List[SegmentEffort.SegmentEffort] = field(default_factory=list,
                                                               metadata={"sa": relationship("SegmentEffort")})

    splits_metric: List[Split.Split] = field(default_factory=list, metadata={
        "sa": relationship("Split", primaryjoin="and_(Activity.id==Split.activity_id, Split.is_metric==True)")})

    splits_standard: List[Split.Split] = field(default_factory=list, metadata={
        "sa": relationship("Split", primaryjoin="and_(Activity.id==Split.activity_id, Split.is_metric==False)",
                           overlaps="splits_metric")})

    laps: List[Lap.Lap] = field(default_factory=list, metadata={"sa": relationship("Lap")})
    highlighted_kudosers: List[HighlightedKudoser.HighlightedKudoser] = field(default_factory=list,
                                                           metadata={"sa": relationship("HighlightedKudoser")})

    kudos: List[Kudoser.Kudoser] = field(default_factory=list, metadata={"sa": relationship("Kudoser")})
    comments: List[Comment.Comment] = field(default_factory=list, metadata={"sa": relationship("Comment")})

    @staticmethod
    def from_dict(obj: Any) -> 'Activity':
        _id = int(obj.get("id"))
        _external_id = str(obj.get("external_id"))
        _upload_id = int(obj.get("upload_id"))
        _athlete_id = int(obj.get("athlete")["id"])
        _name = str(obj.get("name"))
        _distance = int(obj.get("distance"))
        _moving_time = int(obj.get("moving_time"))
        _elapsed_time = int(obj.get("elapsed_time"))
        _total_elevation_gain = int(obj.get("total_elevation_gain"))
        _type = str(obj.get("type"))
        _start_date = str(obj.get("start_date"))
        _start_date_local = str(obj.get("start_date_local"))
        _timezone = str(obj.get("timezone"))
        _utc_offset = int(obj.get("utc_offset"))
        _start_lat = float(obj.get("start_latlng")[0]) if len(obj.get("start_latlng")) > 0 else 0.0
        _start_lng = float(obj.get("start_latlng")[1]) if len(obj.get("start_latlng")) > 0 else 0.0
        _end_lat = float(obj.get("end_latlng")[0]) if len(obj.get("end_latlng")) > 0 else 0.0
        _end_lng = float(obj.get("end_latlng")[1]) if len(obj.get("end_latlng")) > 0 else 0.0
        _achievement_count = int(obj.get("achievement_count"))
        _kudos_count = int(obj.get("kudos_count"))
        _comment_count = int(obj.get("comment_count"))
        _athlete_count = int(obj.get("athlete_count"))
        _photo_count = int(obj.get("photo_count"))
        _map = Map.Map.from_dict(obj.get("map"))
        _trainer = bool(obj.get("trainer"))
        _commute = bool(obj.get("commute"))
        _manual = bool(obj.get("manual"))
        _private = bool(obj.get("private"))
        _flagged = bool(obj.get("flagged"))
        _gear_id = str(obj.get("gear_id"))
        _from_accepted_tag = bool(obj.get("from_accepted_tag"))
        _average_speed = float(obj.get("average_speed"))
        _max_speed = float(obj.get("max_speed"))
        _average_cadence = float(obj.get("average_cadence")) if not obj.get("average_cadence") is None else 0.0
        _average_temp = int(obj.get("average_temp")) if not obj.get("average_temp") is None else 0
        _average_watts = float(obj.get("average_watts")) if not obj.get("average_watts") is None else 0.0
        _weighted_average_watts = int(obj.get("weighted_average_watts")) if not obj.get("weighted_average_watts") is None else 0
        _kilojoules = float(obj.get("kilojoules")) if not obj.get("kilojoules") is None else 0.0
        _device_watts = bool(obj.get("device_watts"))
        _has_heartrate = bool(obj.get("has_heartrate"))
        _max_watts = int(obj.get("max_watts")) if not obj.get("max_watts") is None else 0
        _elev_high = float(obj.get("elev_high")) if not obj.get("elev_high") is None else 0.0
        _elev_low = float(obj.get("elev_low")) if not obj.get("elev_low") is None else 0.0
        _pr_count = int(obj.get("pr_count"))
        _total_photo_count = int(obj.get("total_photo_count"))
        _has_kudoed = bool(obj.get("has_kudoed"))
        _workout_type = int(obj.get("workout_type")) if not obj.get("workout_type") is None else 0
        _suffer_score = str(obj.get("suffer_score"))
        _description = str(obj.get("description"))
        _calories = float(obj.get("calories"))
        _segment_efforts = [SegmentEffort.SegmentEffort.from_dict(y) for y in obj.get("segment_efforts")]
        _splits_metric = [Split.Split.from_dict(y, _id, True) for y in obj.get("splits_metric")]
        _splits_standard = [Split.Split.from_dict(y, _id, False) for y in obj.get("splits_standard")]
        _laps = [Lap.Lap.from_dict(y) for y in obj.get("laps")]
        _gear = Gear.Gear.from_activity_dict(obj.get("gear"))
        _partner_brand_tag = str(obj.get("partner_brand_tag"))
        _photos = Photos.Photos.from_dict(obj.get("photos"), _id)
        _highlighted_kudosers = [HighlightedKudoser.HighlightedKudoser.from_dict(y) for y in obj.get("highlighted_kudosers")] if not obj.get("highlighted_kudosers") is None else []
        _hide_from_home = bool(obj.get("hide_from_home"))
        _device_name = str(obj.get("device_name"))
        _embed_token = str(obj.get("embed_token"))
        _segment_leaderboard_opt_out = bool(obj.get("segment_leaderboard_opt_out"))
        _leaderboard_opt_out = bool(obj.get("leaderboard_opt_out"))
        _average_heartrate = float(obj.get("average_heartrate"))
        _max_heartrate = float(obj.get("max_heartrate"))

        return Activity(_id, _external_id, _upload_id, _athlete_id, _name, _distance, _moving_time, _elapsed_time,
                        _total_elevation_gain, _type, _start_date, _start_date_local, _timezone, _utc_offset,
                        _start_lat, _start_lng, _end_lat, _end_lng, _achievement_count, _kudos_count, _comment_count,
                        _athlete_count, _photo_count, _map, _trainer, _commute, _manual, _private, _flagged, _gear_id,
                        _from_accepted_tag, _average_speed, _max_speed, _average_cadence, _average_temp, _average_watts,
                        _weighted_average_watts, _kilojoules, _device_watts, _has_heartrate, _max_watts, _elev_high,
                        _elev_low, _pr_count, _total_photo_count, _has_kudoed, _workout_type, _suffer_score,
                        _description, _calories, _gear, _partner_brand_tag, _photos, _hide_from_home, _device_name,
                        _embed_token, _segment_leaderboard_opt_out, _leaderboard_opt_out, _average_heartrate,
                        _max_heartrate, _segment_efforts, _splits_metric, _splits_standard, _laps,
                        _highlighted_kudosers)
