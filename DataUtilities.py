from itertools import islice
from typing import List

from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker, Session, joinedload

from Entities import Activity, SegmentEffort, Segment, Athlete


def save_activities(activities: List[Activity]):
    engine = create_engine('sqlite:///strava.sqlite')
    session = sessionmaker(engine)

    for a in activities:

        with session() as my_session:
            existing_activity_query = select(Activity).options(joinedload(Activity.segment_efforts)).filter_by(id=a.id)
            existing_activity_result = my_session.execute(existing_activity_query).first()

            if existing_activity_result is not None:
                my_session.merge(a)
            else:
                add_new_segments(a.segment_efforts)
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
        existing_segment_result = session.execute(existing_segment_query).first()

        if existing_segment_result is not None:
            e.segment = None


def save_athlete(athlete: Athlete):
    engine = create_engine('sqlite:///strava.sqlite')
    session = sessionmaker(engine)

    with session() as my_session:
        existing_athlete_query = select(Athlete).filter_by(id=athlete.id)
        existing_athlete_result = my_session.execute(existing_athlete_query).first()

        if existing_athlete_result is not None:
            my_session.merge(athlete)
        else:
            my_session.add(athlete)

        my_session.commit()
