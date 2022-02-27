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


@dataclass
class SegmentEffort:
    id: float
    resource_state: int
    name: str
    activity_id: int
    athlete_id: int
    elapsed_time: int
    moving_time: int
    start_date: str
    start_date_local: str
    distance: float
    start_index: int
    end_index: int
    average_cadence: float
    device_watts: bool
    average_watts: float
    segment: Segment
    kom_rank: int
    pr_rank: int
    hidden: bool
    average_heartrate: float
    max_heartrate: float
    segment_id: int

    @staticmethod
    def from_dict(obj: Any) -> 'SegmentEffort':
        _id = float(obj.get("id"))
        _resource_state = int(obj.get("resource_state"))
        _name = str(obj.get("name"))
        _activity_id = int(obj.get("activity")["id"])
        _athlete_id = int(obj.get("athlete")["id"])
        _elapsed_time = int(obj.get("elapsed_time"))
        _moving_time = int(obj.get("moving_time"))
        _start_date = str(obj.get("start_date"))
        _start_date_local = str(obj.get("start_date_local"))
        _distance = float(obj.get("distance"))
        _start_index = int(obj.get("start_index"))
        _end_index = int(obj.get("end_index"))
        _average_cadence = float(obj.get("average_cadence")) if not obj.get("average_cadence") is None else None
        _device_watts = bool(obj.get("device_watts"))
        _average_watts = float(obj.get("average_watts")) if not obj.get("average_watts") is None else None
        _segment = Segment.from_dict(obj.get("segment"))
        _kom_rank = int(obj.get("kom_rank")) if not obj.get("kom_rank") is None else None
        _pr_rank = int(obj.get("pr_rank")) if not obj.get("pr_rank") is None else None
        _hidden = bool(obj.get("hidden"))
        _average_heartrate = float(obj.get("average_heartrate"))
        _max_heartrate = float(obj.get("max_heartrate"))
        _segment_id = _segment.id
        return SegmentEffort(_id, _resource_state, _name, _activity_id, _athlete_id, _elapsed_time, _moving_time, _start_date,
                             _start_date_local, _distance, _start_index, _end_index, _average_cadence, _device_watts,
                             _average_watts, _segment, _kom_rank, _pr_rank, _hidden, _average_heartrate, _max_heartrate,
                             _segment_id)


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


@dataclass
class Lap:
    id: float
    resource_state: int
    name: str
    activity_id: int
    athlete_: int
    elapsed_time: int
    moving_time: int
    start_date: str
    start_date_local: str
    distance: float
    start_index: int
    end_index: int
    total_elevation_gain: int
    average_speed: float
    max_speed: float
    average_cadence: float
    device_watts: bool
    average_watts: float
    lap_index: int
    split: int
    average_heartrate: float
    max_heartrate: float

    @staticmethod
    def from_dict(obj: Any) -> 'Lap':
        _id = float(obj.get("id"))
        _resource_state = int(obj.get("resource_state"))
        _name = str(obj.get("name"))
        _activity_id = int(obj.get("activity")["id"])
        _athlete_id = int(obj.get("athlete")["id"])
        _elapsed_time = int(obj.get("elapsed_time"))
        _moving_time = int(obj.get("moving_time"))
        _start_date = str(obj.get("start_date"))
        _start_date_local = str(obj.get("start_date_local"))
        _distance = float(obj.get("distance"))
        _start_index = int(obj.get("start_index"))
        _end_index = int(obj.get("end_index"))
        _total_elevation_gain = int(obj.get("total_elevation_gain"))
        _average_speed = float(obj.get("average_speed"))
        _max_speed = float(obj.get("max_speed"))
        _average_cadence = float(obj.get("average_cadence")) if not obj.get("average_cadence") is None else None
        _device_watts = bool(obj.get("device_watts"))
        _average_watts = float(obj.get("average_watts")) if not obj.get("average_watts") is None else None
        _lap_index = int(obj.get("lap_index"))
        _split = int(obj.get("split"))
        _average_heartrate = float(obj.get("average_heartrate"))
        _max_heartrate = float(obj.get("max_heartrate"))
        return Lap(_id, _resource_state, _name, _activity_id, _athlete_id, _elapsed_time, _moving_time, _start_date,
                   _start_date_local, _distance, _start_index, _end_index, _total_elevation_gain, _average_speed,
                   _max_speed, _average_cadence, _device_watts, _average_watts, _lap_index, _split, _average_heartrate,
                   _max_heartrate)


@dataclass
class Gear:
    id: str
    activity_id: int
    primary: bool
    name: str
    resource_state: int
    distance: int

    @staticmethod
    def from_dict(obj: Any) -> 'Gear':
        if obj is None or obj.get("id") is None:
            return

        _id = str(obj.get("id"))
        _primary = bool(obj.get("primary"))
        _name = str(obj.get("name"))
        _resource_state = int(obj.get("resource_state"))
        _distance = int(obj.get("distance"))
        return Gear(_id, None, _primary, _name, _resource_state, _distance)


@dataclass
class Urls:
    photo_id: int
    small_image: str
    large_image: str

    @staticmethod
    def from_dict(obj: Any) -> 'Urls':
        small_image = str(obj.get("100"))
        large_image = str(obj.get("600"))
        return Urls(None, small_image, large_image)


@dataclass
class PrimaryPhoto:
    id: str
    activity_id: int
    unique_id: str
    urls: Urls
    source: int

    @staticmethod
    def from_dict(obj: Any) -> 'PrimaryPhoto':
        if obj is None or obj.get("id") is None:
            return

        _id = str(obj.get("id"))
        _unique_id = str(obj.get("unique_id"))
        _urls = Urls.from_dict(obj.get("urls"))
        _source = int(obj.get("source"))
        return PrimaryPhoto(_id, None, _unique_id, _urls, _source)


@dataclass
class Photos:
    activity_id: int
    primary: PrimaryPhoto
    use_primary_photo: bool
    count: int

    @staticmethod
    def from_dict(obj: Any) -> 'Photos':
        _primary = PrimaryPhoto.from_dict(obj.get("primary"))
        _use_primary_photo = bool(obj.get("use_primary_photo"))
        _count = int(obj.get("count"))
        return Photos(None, _primary, _use_primary_photo, _count)


@dataclass
class HighlightedKudoser:
    activity_id: int
    destination_url: str
    display_name: str
    avatar_url: str
    show_name: bool

    @staticmethod
    def from_dict(obj: Any) -> 'HighlightedKudoser':
        _destination_url = str(obj.get("destination_url"))
        _display_name = str(obj.get("display_name"))
        _avatar_url = str(obj.get("avatar_url"))
        _show_name = bool(obj.get("show_name"))
        return HighlightedKudoser(None, _destination_url, _display_name, _avatar_url, _show_name)


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
    segment_efforts: List[SegmentEffort]
    splits_metric: List[Split]
    splits_standard: List[Split]
    laps: List[Lap]
    gear: Gear
    partner_brand_tag: str
    photos: Photos
    highlighted_kudosers: List[HighlightedKudoser]
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
        _map = Map.from_dict(obj.get("map"))
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
        _segment_efforts = [SegmentEffort.from_dict(y) for y in obj.get("segment_efforts")]
        _splits_metric = [Split.from_dict(y) for y in obj.get("splits_metric")]
        _splits_standard = [Split.from_dict(y) for y in obj.get("splits_standard")]
        _laps = [Lap.from_dict(y) for y in obj.get("laps")]
        _gear = Gear.from_dict(obj.get("gear"))
        _partner_brand_tag = str(obj.get("partner_brand_tag"))
        _photos = Photos.from_dict(obj.get("photos"))
        _highlighted_kudosers = [HighlightedKudoser.from_dict(y) for y in obj.get("highlighted_kudosers")] if not obj.get("highlighted_kudosers") is None else None
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


@dataclass
class Kudoser:
    activity_id: int
    firstname: str
    lastname: str

    @staticmethod
    def from_dict(obj: Any) -> 'Kudoser':
        _firstname = str(obj.get("firstname"))
        _lastname = str(obj.get("lastname"))
        return Kudoser(None, _firstname, _lastname)

    @staticmethod
    def list_from_dict_array(array):
        kudosers = []
        for k in array:
            kudosers.append(Kudoser.from_dict(k))

        return kudosers


@dataclass
class Comment:
    activity_id: int
    commenter_firstname: str
    commenter_lastname: str
    text: str
    created_at: str

    @staticmethod
    def from_dict(obj: Any) -> 'Comment':
        _activity_id = int(obj.get("activity_id"))
        _commenter_firstname = str(obj.get("athlete")["firstname"])
        _commenter_lastname = str(obj.get("athlete")["lastname"])
        _text = str(obj.get("text"))
        _created_at = str(obj.get("created_at"))
        return Comment(_activity_id, _commenter_firstname, _commenter_lastname, _text, _created_at)

    @staticmethod
    def list_from_dict_array(array):
        comments = []
        for c in array:
            comments.append(Comment.from_dict(c))

        return comments