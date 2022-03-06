from typing import Any
from dataclasses import dataclass


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