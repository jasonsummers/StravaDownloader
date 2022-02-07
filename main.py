import csv
import json
import requests
import urllib3
from os.path import exists
import polylinetoimg
import ActivityProcessor
import StravaDataDownloader
import os
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


def process_activities(activity_ids, settings):

    mappy = polylinetoimg.PolylineToImg(settings['azure_maps_key'])

    source_dir = settings["data_location"]

    for a in activity_ids:

        activity_json_file = source_dir + a + "_activityDetail.json"

        if exists(activity_json_file):
            activity_json = open(activity_json_file, "r")
            activity_details = json.loads(activity_json.read())
            if activity_details["distance"] < 0.1:
                continue
        else:
            # We have no details for the activity ID so skip it
            continue

        activity_kudos_file = source_dir + a + "_activityKudos.json"

        if exists(activity_kudos_file) and activity_details["kudos_count"] > 0:
            kudos_json = open(activity_kudos_file, "r")
            kudos = json.loads(kudos_json.read())
        else:
            kudos = ""

        activity_comments_file = source_dir + a + "_activityComments.json"

        if exists(activity_comments_file) and activity_details["comment_count"] > 0:
            comments_json = open(activity_comments_file, "r")
            comments = json.loads(comments_json.read())
        else:
            comments = ""

        activity_processor = ActivityProcessor.ActivityProcessor(activity_details, kudos, comments)

        entry_datetime = activity_details["start_date_local"]
        entry_timezone = activity_details["timezone"][activity_details["timezone"].index(") ") + 2:]
        entry_coords = "{0} {1}".format(activity_details["start_latlng"][0], activity_details["start_latlng"][1]) if activity_details["start_latlng"] else ""
        entry_tags = activity_details["type"]
        entry_body = activity_processor.process_activity(True, True, "detailed", "both", True)

        shell_command_format = "dayone2 -j Strava --isoDate {0} --time-zone {1} --tags {2}"
        shell_command = shell_command_format.format(entry_datetime, entry_timezone, entry_tags)

        if entry_coords:
            shell_command += " --coordinate {0}".format(entry_coords)

        if activity_details["map"]["polyline"]:
            entry_image = mappy.get_image_url(activity_details["map"]["polyline"])
            downloaded_image = download_activity_image(a, entry_image, source_dir)
            shell_command += " --attachments \"{0}\"".format(downloaded_image)

        shell_command += " -- new \"{0}\"".format(entry_body)

        print(shell_command)
        #os.system(shell_command)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    with open('settings.json') as settings_file:
        settings = json.load(settings_file)

    activity_ids = get_activity_ids(settings["strava_activities_file"])

    #get_data(activity_ids, "all", settings["data_location"])
    process_activities(activity_ids, settings["data_location"])
