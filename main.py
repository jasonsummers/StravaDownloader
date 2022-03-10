import datetime
import json
from typing import List
import dateutil.parser
import requests
import urllib3
from os.path import exists

from sqlalchemy import create_engine, select, desc, or_, and_
from sqlalchemy.orm import sessionmaker, joinedload

import DataUtilities
from Entities import Activity, Comment, Kudoser, Athlete
import polylinetoimg
import ActivityProcessor
import StravaDataDownloader
import os
import sys
import getopt
import shutil
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def get_activity_ids(before: datetime, after: datetime, activity_types: List[str]):
    engine = create_engine('sqlite:///strava.sqlite')
    session = sessionmaker(engine)

    activity_ids = []
    with session() as my_session:
        activity_query = select(Activity.id, Activity.type)

        if before:
            activity_query = activity_query.filter(Activity.start_date < before)

        if after:
            activity_query = activity_query.filter(Activity.start_date > after)

        activity_result = my_session.execute(activity_query).all()
        for a in activity_result:
            if a["type"] in activity_types:
                activity_ids.append(a["id"])

    return activity_ids


def download_activity_image(activity_id, url, output_dir):
    filepath = "{0}/map_images/{1}.png".format(output_dir, activity_id)

    if exists(filepath):
        return filepath

    if not url:
        return ""

    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(filepath, 'wb') as f:
            shutil.copyfileobj(response.raw, f)
        return filepath

    return ""


def process_activities(activity_ids, settings, output_format, journal_name):

    engine = create_engine('sqlite:///strava.sqlite')
    session = sessionmaker(engine)

    mappy = polylinetoimg.PolylineToImg(settings["azure_maps_key"])

    for a in activity_ids:
        print("Processing Activity ID {0}".format(a))

        with session() as my_session:
            activity_query = select(Activity).options(
                joinedload(Activity.map),
                joinedload(Activity.gear),
                joinedload(Activity.segment_efforts),
                joinedload(Activity.splits_metric),
                joinedload(Activity.splits_standard),
                joinedload(Activity.laps),
                joinedload(Activity.kudos),
                joinedload(Activity.comments)
            ).filter_by(id=a)
            activity_result = my_session.execute(activity_query).first()

            if activity_result is None:
                continue

            activity = activity_result[0]

        activity_processor = ActivityProcessor.ActivityProcessor(activity)
        entry_body = activity_processor.process_activity(settings["include_strava_kudos"],
                                                         settings["include_strava_comments"],
                                                         settings["include_segments"], settings["which_splits"],
                                                         settings["include_laps"])

        if output_format == "markdown_terminal":
            print(entry_body)
            continue

        entry_datetime = activity.start_date_local
        entry_timezone = activity.timezone[activity.timezone.index(") ") + 2:]
        entry_coords = "{0} {1}".format(activity.start_lat, activity.start_lng) if activity.start_lat else ""
        entry_tags = activity.type

        shell_command_format = "dayone2 -j {0} --isoDate {1} --time-zone {2} --tags {3}"
        shell_command = shell_command_format.format(journal_name, entry_datetime, entry_timezone, entry_tags)

        if entry_coords:
            shell_command += " --coordinate {0}".format(entry_coords)

        if activity.map.polyline:
            entry_image = mappy.get_image_url(activity.map.polyline)
            downloaded_image = download_activity_image(a, entry_image, os.getcwd())
            shell_command += " --attachments \"{0}\"".format(downloaded_image)

        shell_command += " -- new \"{0}\"".format(entry_body)

        if output_format == "dayone_terminal":
            print(shell_command)
            continue

        if output_format == "dayone":
            os.system(shell_command)
            continue


def update():
    with open('settings.json') as settings_file:
        settings = json.load(settings_file)
    activity_ids = get_activity_ids(settings["strava_activities_file"])

    import requests
    header = {'Authorization': 'Bearer '}
    for aid in activity_ids:
        print('ActivityId: ' + aid)
        response = requests.put(
            url='https://www.strava.com/api/v3/activities/' + aid,
            headers=header,
            data={
                'gear_id': 'g10247939'
            }
        )
        print(response.json())


def load_athlete():
    strava = StravaDataDownloader.StravaDataDownloader()
    athlete_json = strava.get_athlete()
    athlete = Athlete.from_dict(athlete_json)

    DataUtilities.save_athlete(athlete)


def main(arg):
    with open('settings.json') as settings_file:
        settings = json.load(settings_file)

    journal_name = ''
    output_format = ''
    start_date = ''
    activity_types = ''
    no_downloads = False

    try:
        opts, args = getopt.getopt(arg, "hj:o:xd:t:",
                                   ["journal=", "outputformat=", "nodownloads", "startdate=", "activitytypes="])
    except getopt.GetoptError:
        print('main.py -j <journal> -o <outputformat>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('main.py -i <inputfile> -o <outputfile>')
            sys.exit()
        elif opt in ("-j", "--journal"):
            journal_name = arg
        elif opt in ("-o", "--outputformat"):
            output_format = arg
        elif opt in ("-x", "--nodownloads"):
            no_downloads = True
        elif opt in ("-d", "--startdate"):
            start_date = arg
        elif opt in ("-t", "--activitytypes"):
            activity_types = arg

    activity_types_list = activity_types.split(",")

    after = dateutil.parser.parse(start_date)
    activity_ids = get_activity_ids(None, after, activity_types_list)

    process_activities(activity_ids, settings, output_format, journal_name)


def load_activity_summaries():

    engine = create_engine('sqlite:///strava.sqlite')
    session = sessionmaker(engine)

    with session() as my_session:
        latest_activity_query = select(Activity).order_by(Activity.start_date.desc())
        latest_activity_result = my_session.execute(latest_activity_query).first()

    strava = StravaDataDownloader.StravaDataDownloader()
    before = None
    after = dateutil.parser.isoparse(latest_activity_result[0].start_date)
    activities = strava.get_activities(before, after)

    new_activities = []
    for a in activities:
        new_activity = Activity.from_dict(a)
        new_activities.append(new_activity)

    DataUtilities.save_activities(new_activities)


def download_activity_data(past_days_to_process: int, latest_first: bool, types_to_process: List[str]):
    with open('settings.json') as settings_file:
        settings = json.load(settings_file)

    engine = create_engine('sqlite:///strava.sqlite')
    session = sessionmaker(engine)
    strava = StravaDataDownloader.StravaDataDownloader()

    with session() as my_session:
        latest_activity_query = select(Activity).order_by(Activity.start_date.desc())
        latest_activity_result = my_session.execute(latest_activity_query).first()

        latest_start_date = dateutil.parser.isoparse(latest_activity_result[0].start_date)
        start_date = latest_start_date - datetime.timedelta(past_days_to_process)

        activities_to_process_query = select(Activity).filter(
            or_(
                Activity.start_date > start_date,
                and_(
                    Activity.device_name == "None",
                    Activity.embed_token == "None"
                )
            )
        )

        if latest_first:
            activities_to_process_query = activities_to_process_query.order_by(Activity.start_date.desc())
        else:
            activities_to_process_query = activities_to_process_query.order_by(Activity.start_date)

        activities_to_process = my_session.execute(activities_to_process_query).all()

        for a in activities_to_process:
            if types_to_process is not None:
                if a[0].type not in types_to_process:
                    continue

            print("Downloading detail for Activity ID: {0}".format(a[0].id))

            activity_json = strava.get_activity_detail(a[0].id, None)
            activity = Activity.from_dict(activity_json)

            if activity.kudos_count > 0 and settings["include_strava_kudos"]:
                kudos_json = strava.get_activity_kudos(a[0].id, None)
                kudos = Kudoser.list_from_dict_array(kudos_json, a[0].id)
                activity.kudos = kudos

            if activity.comment_count > 0 and settings["include_strava_comments"]:
                comments_json = strava.get_activity_comments(a[0].id, None)
                comments = Comment.list_from_dict_array(comments_json)
                activity.comments = comments

            initial_detail_load = a[0].device_name == "None" and a[0].embed_token == "None"

            DataUtilities.save_activity(activity, initial_detail_load)


if __name__ == '__main__':

    #update()
    #load_athlete()
    #load_activities()
    #main(sys.argv[1:])
    #setup()
    #load_activity_summaries()
    download_activity_data(7, False)

