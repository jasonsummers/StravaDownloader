from typing import Any
from dataclasses import dataclass


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