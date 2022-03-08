from typing import Any
from dataclasses import dataclass, field
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from Entities import Base

@Base.Registry.mapped
@dataclass
class HighlightedKudoser:
    __tablename__ = "highlighted_kudoser"
    __sa_dataclass_metadata_key__ = "sa"

    id: int = field(init=False, metadata={"sa": Column(Integer, primary_key=True)})
    activity_id: int = field(metadata={"sa": Column(Integer, ForeignKey("activities.id"))})
    destination_url: str = field(metadata={"sa": Column(String(250))})
    display_name: str = field(metadata={"sa": Column(String(250))})
    avatar_url: str = field(metadata={"sa": Column(String(250))})
    show_name: bool = field(metadata={"sa": Column(Boolean)})

    @staticmethod
    def from_dict(obj: Any) -> 'HighlightedKudoser':
        _destination_url = str(obj.get("destination_url"))
        _display_name = str(obj.get("display_name"))
        _avatar_url = str(obj.get("avatar_url"))
        _show_name = bool(obj.get("show_name"))
        return HighlightedKudoser(None, _destination_url, _display_name, _avatar_url, _show_name)