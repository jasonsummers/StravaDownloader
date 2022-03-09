from typing import Any
from dataclasses import dataclass, field
from sqlalchemy import Column, Integer, Float, String, Boolean, ForeignKey
from Entities import Base

@Base.Registry.mapped
@dataclass
class Comment:
    __tablename__ = "comments"
    __sa_dataclass_metadata_key__ = "sa"

    id: int = field(metadata={"sa": Column(Integer, primary_key=True)})
    activity_id: int = field(metadata={"sa": Column(Integer, ForeignKey("activities.id"), primary_key=True)})
    commenter_firstname: str = field(metadata={"sa": Column(String(50))})
    commenter_lastname: str = field(metadata={"sa": Column(String(50))})
    text: str = field(metadata={"sa": Column(String(250))})
    created_at: str = field(metadata={"sa": Column(String(50))})

    @staticmethod
    def from_dict(obj: Any) -> 'Comment':
        _id = int(obj.get("id"))
        _activity_id = int(obj.get("activity_id"))
        _commenter_firstname = str(obj.get("athlete")["firstname"])
        _commenter_lastname = str(obj.get("athlete")["lastname"])
        _text = str(obj.get("text"))
        _created_at = str(obj.get("created_at"))
        return Comment(_id, _activity_id, _commenter_firstname, _commenter_lastname, _text, _created_at)

    @staticmethod
    def list_from_dict_array(array):
        comments = []
        for c in array:
            comments.append(Comment.from_dict(c))

        return comments
