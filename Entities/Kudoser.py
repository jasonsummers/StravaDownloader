from itertools import islice
from typing import Any
from dataclasses import dataclass, field
from sqlalchemy import Column, Integer, String, ForeignKey
from Entities import Base


@Base.Registry.mapped
@dataclass
class Kudoser:
    __tablename__ = "kudosers"
    __sa_dataclass_metadata_key__ = "sa"

    activity_id: int = field(metadata={"sa": Column(Integer, ForeignKey("activities.id"), primary_key=True)})
    firstname: str = field(metadata={"sa": Column(String(50), primary_key=True)})
    lastname: str = field(metadata={"sa": Column(String(50), primary_key=True)})

    @staticmethod
    def from_dict(obj: Any, activity_id: int) -> 'Kudoser':
        _firstname = str(obj.get("firstname"))
        _lastname = str(obj.get("lastname"))
        return Kudoser(activity_id, _firstname, _lastname)

    @staticmethod
    def list_from_dict_array(array, activity_id: int):
        kudosers = []
        for k in array:

            duplicated_kudosers = [x for x in array if x.get("firstname") == k.get("firstname") and
                                   x.get("lastname") == k.get("lastname")]
            kudosers_to_amend = islice(duplicated_kudosers, 1, None)

            duplicate_count = 2
            for d in kudosers_to_amend:
                d["lastname"] += " ({0})".format(duplicate_count)
                duplicate_count += 1

            kudosers.append(Kudoser.from_dict(k, activity_id))

        return kudosers