from typing import Any
from dataclasses import dataclass


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
