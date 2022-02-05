import csv
import json
import requests
import urllib3
from os.path import exists
import polylinetoimg
import time
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def get_activity_ids():
    from dateutil import parser
    strava_activities_file = "/Users/Jason/Downloads/export_2111200/activities.csv"

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


def get_activity_detail(base_url, header, activity_id, output_directory):
    the_url = base_url + "/" + activity_id

    param = {'include_all_efforts': 'true'}
    response = requests.get(the_url, params=param, headers=header).json()

    file = open(output_directory + activity_id + "_activityDetail.json", "w")
    json.dump(response, file, indent=4)
    file.close()


def get_activity_comments(base_url, header, activity_id, output_directory):
    the_url = base_url + "/" + activity_id + "/comments"

    response = requests.get(the_url, headers=header).json()

    file = open(output_directory + activity_id + "_activityComments.json", "w")
    json.dump(response, file, indent=4)
    file.close()


def get_activity_kudos(base_url, header, activity_id, output_directory):
    the_url = base_url + "/" + activity_id + "/kudos"

    response = requests.get(the_url, headers=header).json()

    file = open(output_directory + activity_id + "_activityKudos.json", "w")
    json.dump(response, file, indent=4)
    file.close()


def get_data(activities, data_type):

    output_dir = "/Users/Jason/Desktop/strava_output/"
    activites_url = "https://www.strava.com/api/v3/activities"
    access_token = 'strava-access-token-goes-here'
    print("Access Token = {}\n".format(access_token))

    header = {'Authorization': 'Bearer ' + access_token}

    for a in activities:
        if data_type == "detail":
            get_activity_detail(activites_url, header, a, output_dir)
        elif data_type == "comments":
            get_activity_comments(activites_url, header, a, output_dir)
        elif data_type == "kudos":
            get_activity_kudos(activites_url, header, a, output_dir)
        elif data_type == "all":
            get_activity_detail(activites_url, header, a, output_dir)
            get_activity_comments(activites_url, header, a, output_dir)
            get_activity_kudos(activites_url, header, a, output_dir)


def process_segment(segment, detailed):
    if segment["pr_rank"] == 1:
        pr_suffix = "\U0001F947"
    elif segment["pr_rank"] == 2:
        pr_suffix = "\U0001F948"
    elif segment["pr_rank"] == 3:
        pr_suffix = "\U0001F949"
    else:
        pr_suffix = ""

    segment_pr = " {0}".format(pr_suffix) if segment["pr_rank"] is not None else ""
    segment_distance_km = round(segment["distance"] / 1000, 2)
    segment_distance_mi = round((segment["distance"] / 1000) * 0.6213712, 2)
    segment_time = time.gmtime(segment["moving_time"])

    if segment["moving_time"] > 3599:
        segment_time_output = time.strftime("%H:%M:%S", segment_time)
    else:
        segment_time_output = time.strftime("%M:%S", segment_time)

    segment_pace_km_seconds = float(segment["moving_time"]) / float(segment_distance_km)
    segment_pace_km_time = time.gmtime(segment_pace_km_seconds)
    segment_pace_km_time_output = time.strftime("%M:%S", segment_pace_km_time)

    segment_pace_mi_seconds = float(segment["moving_time"]) / float(segment_distance_mi)
    segment_pace_mi_time = time.gmtime(segment_pace_mi_seconds)
    segment_pace_mi_time_output = time.strftime("%M:%S", segment_pace_mi_time)

    if detailed is False:
        return "{0} {1}  \n".format(segment["name"], segment_pr)

    string_format = "| {0}{1} | {2} | {3}km / {4}mi | {5}min/km / {6}min/mi | {7} bpm | {8} bpm |  \n"

    return string_format.format(segment["name"], segment_pr, segment_time_output,
                                segment_distance_km, segment_distance_mi, segment_pace_km_time_output,
                                segment_pace_mi_time_output, round(segment["average_heartrate"]),
                                round(segment["max_heartrate"]))


def process_segments(activity, detailed):
    segments_string = "### Segments  \n"

    if detailed is True:
        segments_string += "| Segment | Time | Distance | Pace | Avg. Heart Rate | Max Heart Rate |  \n"
        segments_string += "| ----- | ----- | ----- | ----- | ----- | ----- |  \n"

    for s in activity["segment_efforts"]:
        segments_string += process_segment(s, detailed)

    return segments_string


def process_split(split, metric):
    moving_time = time.gmtime(split["moving_time"])
    elapsed_time = time.gmtime(split["elapsed_time"])

    if split["moving_time"] > 3599:
        moving_time_output = time.strftime("%H:%M:%S", moving_time)
    else:
        moving_time_output = time.strftime("%M:%S", moving_time)

    if split["elapsed_time"] > 3599:
        elapsed_time_output = time.strftime("%H:%M:%S", elapsed_time)
    else:
        elapsed_time_output = time.strftime("%M:%S", elapsed_time)

    speed = round(split["average_speed"] * 3.6, 2)
    if metric is False:
        speed = round(speed * 0.6213712, 2)

    if metric:
        speed_suffix = "kph"
    else:
        speed_suffix = "mph"

    return "| {0} | {1} | {2} {3} | {4} bpm |  \n".format(split["split"], moving_time_output, speed,
                                                   speed_suffix, round(split["average_heartrate"]))


def process_splits(activity):
    splits_string = "### Splits  \n"

    table_header = "| Split | Time | Speed | Heart Rate |  \n"
    table_header += "| ----- | ----- | ----- | ----- |  \n"

    splits_string += "#### Kilometres  \n"
    splits_string += table_header

    for s in activity["splits_metric"]:
        splits_string += process_split(s, True)

    splits_string += "  \n"
    splits_string += "#### Miles  \n"
    splits_string += table_header

    for s in activity["splits_standard"]:
        splits_string += process_split(s, False)

    return splits_string

def process_activity_details(activity):
    description = "{0}  \n".format(activity["description"]) if activity["description"] is not None else ""
    distance_km = round(activity["distance"] / 1000, 2)
    distance_mi = round((activity["distance"] / 1000) * 0.6213712, 2)
    moving_time = time.gmtime(activity["moving_time"])
    elapsed_time = time.gmtime(activity["elapsed_time"])

    if activity["moving_time"] > 3599:
        moving_time_output = time.strftime("%H:%M:%S", moving_time)
    else:
        moving_time_output = time.strftime("%M:%S", moving_time)

    if activity["elapsed_time"] > 3599:
        elapsed_time_output = time.strftime("%H:%M:%S", elapsed_time)
    else:
        elapsed_time_output = time.strftime("%M:%S", elapsed_time)

    pace_km_seconds = float(activity["moving_time"]) / float(distance_km)
    pace_km_time = time.gmtime(pace_km_seconds)
    pace_km_time_output = time.strftime("%M:%S", pace_km_time)

    segment_pace_mi_seconds = float(activity["moving_time"]) / float(distance_mi)
    segment_pace_mi_time = time.gmtime(segment_pace_mi_seconds)
    pace_mi_time_output = time.strftime("%M:%S", segment_pace_mi_time)

    avg_speed_kmh = round(activity["average_speed"] * 3.6, 2)
    avg_speed_mph = round(avg_speed_kmh * 0.6213712, 2)
    max_speed_kmh = round(activity["max_speed"] * 3.6, 2)
    max_speed_mph = round(max_speed_kmh * 0.6213712, 2)

    activity_details_string = "# {0}  \n".format(activity["name"])
    activity_details_string += description
    activity_details_string += "|       |       |       |  \n"
    activity_details_string += "| ----- | ----- | ----- |  \n"
    activity_details_string += "| **Time:** | {0} moving | {1} total |  \n".format(moving_time_output, elapsed_time_output)
    activity_details_string += "| **Distance:** | {0}km | {1}mi |  \n".format(distance_km, distance_mi)
    activity_details_string += "| **Pace:** | {0} min/km | {1} min/mi |  \n".format(pace_km_time_output, pace_mi_time_output)
    activity_details_string += "| **Avg. Speed:** | {0} kph | {1} mph |  \n".format(avg_speed_kmh, avg_speed_mph)
    activity_details_string += "| **Max Speed:** | {0} kph | {1} mph |  \n".format(max_speed_kmh, max_speed_mph)

    if activity["has_heartrate"]:
        activity_details_string += "| **Heart Rate:** | {0} bpm avg | {1} bpm max  \n".format(round(activity["average_heartrate"]), round(activity["max_heartrate"]))

    activity_details_string += "  \n[{attachment}]  \n"

    return activity_details_string


def process_comments(comments):
    comment_string = '### Comments\n'
    for c in comments:
        comment_string += "**{0} {1}** {2}  \n".format(c["athlete"]["firstname"], c["athlete"]["lastname"], c["text"])

    return comment_string[:len(comment_string)-2]


def process_kudos(kudos):
    kudos_string = '### Got Kudos From\n'
    for k in kudos:
        kudos_string += "{0} {1} ".format(k["firstname"], k["lastname"])

    return kudos_string


def process_activities(activity_ids, source_dir):

    mappy = polylinetoimg.PolylineToImg("subscription_key_goes_here")

    for a in activity_ids:

        activity_json_file = source_dir + a + "_activityDetail.json"

        if exists(activity_json_file):
            activity_json = open(activity_json_file, "r")
            activity_details = json.loads(activity_json.read())
            if activity_details["distance"] < 0.1:
                continue

            entry_body = process_activity_details(activity_details)
            entry_image = mappy.get_image_url(activity_details["map"]["polyline"])

        activity_kudos_file = source_dir + a + "_activityKudos.json"

        if exists(activity_kudos_file) and activity_details["kudos_count"] > 0:
            kudos_json = open(activity_kudos_file, "r")
            kudos = json.loads(kudos_json.read())
            entry_body += '\n'
            entry_body += process_kudos(kudos)

        activity_comments_file = source_dir + a + "_activityComments.json"

        if exists(activity_comments_file) and activity_details["comment_count"] > 0:
            comments_json = open(activity_comments_file, "r")
            comments = json.loads(comments_json.read())
            entry_body += '\n'
            entry_body += process_comments(comments)

        entry_body += '\n'
        entry_body += process_segments(activity_details, True)

        entry_body += '\n'
        entry_body += process_splits(activity_details)

        entry_datetime = activity_details["start_date_local"]
        entry_timezone = activity_details["timezone"][activity_details["timezone"].index(") ") + 2:]
        entry_coords = "{0} {1}".format(activity_details["start_latlng"][0], activity_details["start_latlng"][1]) if activity_details["start_latlng"] else ""

        """
        print(entry_datetime)
        print(entry_timezone)
        print(entry_coords)
        print(entry_image)
        print(entry_body)
        """

        shell_command_format = "dayone2 -j Strava --isoDate {0} --time-zone {1} --attachments {2}"
        shell_command = shell_command_format.format(entry_datetime, entry_timezone, entry_image)

        if entry_coords:
            shell_command += " --coordinate {0}".format(entry_coords)

        shell_command += " {0}".format(entry_body)
        print(shell_command)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    activity_ids = get_activity_ids()
    #get_data(activity_ids, "kudos")
    process_activities(activity_ids, "/Users/Jason/Desktop/strava_output/")
