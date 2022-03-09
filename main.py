import csv
import datetime
import json
import requests
import urllib3
from os.path import exists

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


def get_activity_ids(strava_activities_file):
    from dateutil import parser

    activities = []
    with open(strava_activities_file) as activities_csv:
        csv_reader = csv.reader(activities_csv, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                line_count = line_count + 1
            else:
                if parser.parse(row[1]).year != 2021 or row[3] != "Run":
                    continue

                activities.append(row[0])

    return activities


def get_data(activities, data_type, output_dir):
    strava = StravaDataDownloader.StravaDataDownloader()
    strava.get_data(activities, data_type, output_dir)


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

    mappy = polylinetoimg.PolylineToImg(settings["azure_maps_key"])

    source_dir = settings["data_location"]

    for a in activity_ids:

        activity_json_file = source_dir + a + "_activityDetail.json"

        if exists(activity_json_file):
            with open(activity_json_file, "r") as activity_json:
                activity_details_json = json.loads(activity_json.read())
                activity_details = Activity.Activity.from_dict(activity_details_json)
            if activity_details.distance < 0.1:
                continue
        else:
            # We have no details for the activity ID so skip it
            continue

        activity_kudos_file = source_dir + a + "_activityKudos.json"

        if settings["include_strava_kudos"] and exists(activity_kudos_file) and activity_details.kudos_count > 0:
            with open(activity_kudos_file, "r") as kudos_json:
                kudos_dict = json.loads(kudos_json.read())
                kudos = Kudoser.Kudoser.list_from_dict_array(kudos_dict)
        else:
            kudos = None

        activity_comments_file = source_dir + a + "_activityComments.json"

        if settings["include_strava_comments"] and exists(activity_comments_file)\
                and activity_details.comment_count > 0:
            with open(activity_comments_file, "r") as comments_json:
                comments_dict = json.loads(comments_json.read())
                comments = Comment.Comment.list_from_dict_array(comments_dict)
        else:
            comments = None

        activity_processor = ActivityProcessor.ActivityProcessor(activity_details, kudos, comments)
        entry_body = activity_processor.process_activity(settings["include_strava_kudos"],
                                                         settings["include_strava_comments"],
                                                         settings["include_segments"], settings["which_splits"],
                                                         settings["include_laps"])

        if output_format == "markdown_terminal":
            print(entry_body)
            continue

        entry_datetime = activity_details.start_date_local
        entry_timezone = activity_details.timezone[activity_details.timezone.index(") ") + 2:]
        entry_coords = "{0} {1}".format(activity_details.start_latlng[0], activity_details.start_latlng[1])\
            if activity_details.start_latlng else ""
        entry_tags = activity_details.type

        shell_command_format = "dayone2 -j {0} --isoDate {1} --time-zone {2} --tags {3}"
        shell_command = shell_command_format.format(journal_name, entry_datetime, entry_timezone, entry_tags)

        if entry_coords:
            shell_command += " --coordinate {0}".format(entry_coords)

        if activity_details.map.polyline:
            entry_image = mappy.get_image_url(activity_details.map.polyline)
            downloaded_image = download_activity_image(a, entry_image, source_dir)
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
    with open("/Users/Jason/Desktop/athlete.json") as athlete_file:
        athlete_json = json.load(athlete_file)

    new_athlete = Athlete.from_dict(athlete_json)

    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker

    engine = create_engine('sqlite:///strava.sqlite')
    Session = sessionmaker(engine)

    with Session() as session:
        session.add(new_athlete)
        session.commit()

def load_activities():
    with open('settings.json') as settings_file:
        settings = json.load(settings_file)
    activity_ids = get_activity_ids(settings["strava_activities_file"])
    source_dir = settings["data_location"]

    activities_to_add = []

    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker

    for a in activity_ids:
        activity_json_file = source_dir + a + "_activityDetail.json"

        if exists(activity_json_file):
            with open(activity_json_file, "r") as activity_json:
                activity_details_json = json.loads(activity_json.read())
                activity_details = Activity.from_dict(activity_details_json)
            if activity_details.distance < 0.1:
                continue
        else:
            # We have no details for the activity ID so skip it
            continue

        activity_kudos_file = source_dir + a + "_activityKudos.json"

        if settings["include_strava_kudos"] and exists(activity_kudos_file) and activity_details.kudos_count > 0:
            with open(activity_kudos_file, "r") as kudos_json:
                kudos_dict = json.loads(kudos_json.read())
                kudos = Kudoser.list_from_dict_array(kudos_dict)
        else:
            kudos = []

        activity_comments_file = source_dir + a + "_activityComments.json"

        if settings["include_strava_comments"] and exists(activity_comments_file) \
                and activity_details.comment_count > 0:
            with open(activity_comments_file, "r") as comments_json:
                comments_dict = json.loads(comments_json.read())
                comments = Comment.list_from_dict_array(comments_dict)
        else:
            comments = []

        activity_details.kudos = kudos
        activity_details.comments = comments

        activities_to_add.append(activity_details)

    DataUtilities.save_activities(activities_to_add)


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
            start_date = arg


    activity_ids = get_activity_ids(settings["strava_activities_file"])

    if settings["include_strava_comments"] and settings["include_strava_kudos"]:
        data_types = "all"
    else:
        data_types = "detail"
        if settings["include_strava_comments"]:
            data_types += ",comments"
        if settings["include_strava_kudos"]:
            data_types += ",kudos"

    if not no_downloads:
        get_data(activity_ids, data_types, settings["data_location"])

    process_activities(activity_ids, settings, output_format, journal_name)


if __name__ == '__main__':

    #update()
    #load_athlete()
    load_activities()
    #main(sys.argv[1:])
    #setup()

    #strava = StravaDataDownloader.StravaDataDownloader()
    #before = None
    #after = datetime.datetime(2022, 1, 1)
    #activities = strava.get_activities(before, after)
    #print(activities)

