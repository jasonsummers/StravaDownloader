from typing import Any
from dataclasses import dataclass, field
from sqlalchemy import Column, Integer, String, ForeignKey
from Entities import Base


@Base.Registry.mapped
@dataclass
class Kudoser:
    __tablename__ = "kudosers"
    __sa_dataclass_metadata_key__ = "sa"

    id: int = field(init=False, metadata={"sa": Column(Integer, primary_key=True)})
    activity_id: int = field(metadata={"sa": Column(Integer, ForeignKey("activities.id"))})
    firstname: str = field(metadata={"sa": Column(String(50))})
    lastname: str = field(metadata={"sa": Column(String(50))})

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