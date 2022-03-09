from itertools import islice
from typing import List

from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker, Session

from Entities import Activity, SegmentEffort, Segment


def save_activities(activities: List[Activity]):
    engine = create_engine('sqlite:///strava.sqlite')
    session = sessionmaker(engine)

    for a in activities:
        add_new_segments(a.segment_efforts)

        with session() as my_session:
            existing_activity_query = select(Activity).filter_by(id=a.id)
            existing_activity_result = my_session.execute(existing_activity_query).all()

            if len(existing_activity_result) > 0:
                my_session.merge(a)
            else:
                my_session.add(a)

            my_session.commit()


def add_new_segments(efforts: List[SegmentEffort]):
    engine = create_engine('sqlite:///strava.sqlite')
    session = Session(engine, future=True)

    for e in efforts:
        if e.segment is None:
            continue

        duplicated_segments = [x for x in efforts if x.segment_id == e.segment_id]
        duplicates_to_remove = islice(duplicated_segments, 1, None)

        for d in duplicates_to_remove:
            d.segment = None

        existing_segment_query = select(Segment).filter_by(id=e.segment_id)
        existing_segment_result = session.execute(existing_segment_query).all()

        if len(existing_segment_result) > 0:
            e.segment = None
