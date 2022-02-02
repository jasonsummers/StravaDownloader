import csv
import json
import requests
import urllib3
from os.path import exists
import polylinetoimg
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


def process_activity_details(activity):
    activity_details_string = "" #"{0}"activity["description"] + '\n'
    activity_details_string += activity["name"] + '\n'
    activity_details_string += "Distance (km) {0}, Distance (mi) {1}\n".format(round(activity["distance"] / 1000, 2), round((activity["distance"] / 1000) * 0.6213712, 2))

    activity_details_string += "Segments...\n"
    for s in activity["segment_efforts"]:
        activity_details_string += "{0} {1}\n".format(s["name"], s["pr_rank"])

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
            print(process_activity_details(activity_details))
            print(mappy.get_image_url(activity_details["map"]["polyline"]))

        activity_comments_file = source_dir + a + "_activityComments.json"

        if exists(activity_comments_file) and activity_details["comment_count"] > 0:
            comments_json = open(activity_comments_file, "r")
            comments = json.loads(comments_json.read())
            print(process_comments(comments))

        activity_kudos_file = source_dir + a + "_activityKudos.json"

        if exists(activity_kudos_file) and activity_details["kudos_count"] > 0:
            kudos_json = open(activity_kudos_file, "r")
            kudos = json.loads(kudos_json.read())
            print(process_kudos(kudos))


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    activity_ids = get_activity_ids()
    #get_data(activity_ids, "kudos")
    process_activities(activity_ids, "/Users/Jason/Desktop/strava_output/")
