from typing import List
from typing import Any
from dataclasses import dataclass
from Entities import Gear, HighlightedKudoser, Lap, Map, Photos, SegmentEffort, Split


@dataclass
class Activity:
    id: float
    external_id: str
    upload_id: float
    athlete_id: int
    name: str
    distance: int
    moving_time: int
    elapsed_time: int
    total_elevation_gain: int
    type: str
    start_date: str
    start_date_local: str
    timezone: str
    utc_offset: float
    start_latlng: List[float]
    end_latlng: List[float]
    achievement_count: int
    kudos_count: int
    comment_count: int
    athlete_count: int
    photo_count: int
    map: Map
    trainer: bool
    commute: bool
    manual: bool
    private: bool
    flagged: bool
    gear_id: str
    from_accepted_tag: bool
    average_speed: float
    max_speed: float
    average_cadence: float
    average_temp: int
    average_watts: float
    weighted_average_watts: int
    kilojoules: float
    device_watts: bool
    has_heartrate: bool
    max_watts: int
    elev_high: float
    elev_low: float
    pr_count: int
    total_photo_count: int
    has_kudoed: bool
    workout_type: int
    suffer_score: str
    description: str
    calories: float
    segment_efforts: List[SegmentEffort.SegmentEffort]
    splits_metric: List[Split.Split]
    splits_standard: List[Split.Split]
    laps: List[Lap.Lap]
    gear: Gear
    partner_brand_tag: str
    photos: Photos
    highlighted_kudosers: List[HighlightedKudoser.HighlightedKudoser]
    hide_from_home: bool
    device_name: str
    embed_token: str
    segment_leaderboard_opt_out: bool
    leaderboard_opt_out: bool
    average_heartrate: float
    max_heartrate: float

    @staticmethod
    def from_dict(obj: Any) -> 'Activity':
        _id = float(obj.get("id"))
        _external_id = str(obj.get("external_id"))
        _upload_id = float(obj.get("upload_id"))
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
        _start_latlng = [float(y) for y in obj.get("start_latlng")]
        _end_latlng = [float(y) for y in obj.get("end_latlng")]
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
        _average_cadence = float(obj.get("average_cadence")) if not obj.get("average_cadence") is None else None
        _average_temp = int(obj.get("average_temp")) if not obj.get("average_temp") is None else None
        _average_watts = float(obj.get("average_watts")) if not obj.get("average_watts") is None else None
        _weighted_average_watts = int(obj.get("weighted_average_watts")) if not obj.get("weighted_average_watts") is None else None
        _kilojoules = float(obj.get("kilojoules")) if not obj.get("kilojoules") is None else None
        _device_watts = bool(obj.get("device_watts"))
        _has_heartrate = bool(obj.get("has_heartrate"))
        _max_watts = int(obj.get("max_watts")) if not obj.get("max_watts") is None else None
        _elev_high = float(obj.get("elev_high")) if not obj.get("elev_high") is None else None
        _elev_low = float(obj.get("elev_low")) if not obj.get("elev_low") is None else None
        _pr_count = int(obj.get("pr_count"))
        _total_photo_count = int(obj.get("total_photo_count"))
        _has_kudoed = bool(obj.get("has_kudoed"))
        _workout_type = int(obj.get("workout_type")) if not obj.get("workout_type") is None else None
        _suffer_score = str(obj.get("suffer_score"))
        _description = str(obj.get("description"))
        _calories = float(obj.get("calories"))
        _segment_efforts = [SegmentEffort.SegmentEffort.from_dict(y) for y in obj.get("segment_efforts")]
        _splits_metric = [Split.Split.from_dict(y) for y in obj.get("splits_metric")]
        _splits_standard = [Split.Split.from_dict(y) for y in obj.get("splits_standard")]
        _laps = [Lap.Lap.from_dict(y) for y in obj.get("laps")]
        _gear = Gear.Gear.from_activity_dict(obj.get("gear"))
        _partner_brand_tag = str(obj.get("partner_brand_tag"))
        _photos = Photos.Photos.from_dict(obj.get("photos"))
        _highlighted_kudosers = [HighlightedKudoser.HighlightedKudoser.from_dict(y) for y in obj.get("highlighted_kudosers")] if not obj.get("highlighted_kudosers") is None else None
        _hide_from_home = bool(obj.get("hide_from_home"))
        _device_name = str(obj.get("device_name"))
        _embed_token = str(obj.get("embed_token"))
        _segment_leaderboard_opt_out = bool(obj.get("segment_leaderboard_opt_out"))
        _leaderboard_opt_out = bool(obj.get("leaderboard_opt_out"))
        _average_heartrate = float(obj.get("average_heartrate"))
        _max_heartrate = float(obj.get("max_heartrate"))
        return Activity(_id, _external_id, _upload_id, _athlete_id, _name, _distance, _moving_time,
                        _elapsed_time, _total_elevation_gain, _type, _start_date, _start_date_local, _timezone,
                        _utc_offset, _start_latlng, _end_latlng, _achievement_count, _kudos_count, _comment_count,
                        _athlete_count, _photo_count, _map, _trainer, _commute, _manual, _private, _flagged, _gear_id,
                        _from_accepted_tag, _average_speed, _max_speed, _average_cadence, _average_temp, _average_watts,
                        _weighted_average_watts, _kilojoules, _device_watts, _has_heartrate, _max_watts, _elev_high,
                        _elev_low, _pr_count, _total_photo_count, _has_kudoed, _workout_type, _suffer_score,
                        _description, _calories, _segment_efforts, _splits_metric, _splits_standard, _laps, _gear,
                        _partner_brand_tag, _photos, _highlighted_kudosers, _hide_from_home, _device_name, _embed_token,
                        _segment_leaderboard_opt_out, _leaderboard_opt_out, _average_heartrate, _max_heartrate)