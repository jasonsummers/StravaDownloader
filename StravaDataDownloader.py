import datetime
import requests
import json
import time
import csv
from os.path import exists

class StravaDataDownloader:

    def __init__(self):
        self.activity_base_url = "https://www.strava.com/api/v3/activities"
        self.athlete_base_url = "https://www.strava.com/api/v3/athlete"
        with open('settings.json') as settings_file:
            self.settings = json.load(settings_file)

        # Get the tokens from file to connect to Strava
        with open('strava_tokens.json') as json_file:
            self.strava_tokens = json.load(json_file)
        # If access_token has expired then
        # use the refresh_token to get the new access_token
        if self.strava_tokens['expires_at'] < time.time():
            # Make Strava auth API call with current refresh token
            response = requests.post(
                url='https://www.strava.com/oauth/token',
                data={
                    'client_id': self.settings['strava_client_id'],
                    'client_secret': self.settings['strava_client_secret'],
                    'grant_type': 'refresh_token',
                    'refresh_token': self.strava_tokens['refresh_token']
                }
            )
            # Save response as json in new variable
            new_strava_tokens = response.json()
            # Save new tokens to file
            with open('strava_tokens.json', 'w') as outfile:
                json.dump(new_strava_tokens, outfile)
            # Use new Strava tokens from now
            self.strava_tokens = new_strava_tokens

    def get_token(self):
        return self.strava_tokens['access_token']

    def fetch_from_strava(self, url, header, param=""):
        if param:
            response = requests.get(url, params=param, headers=header).json()
        else:
            response = requests.get(url, headers=header).json()

        if "errors" not in response:
            return response

        print("Error Downloading from Strava...")
        print("Message: {0}".format(response["message"]))
        print("Errors:")
        for e in response["errors"]:
            print("    resource: {0}, field: {1}, code: {2}".format(e["resource"], e["field"], e["code"]))

        exit(1)

    def update_activities_list(self):
        activities_file_path = "/activities.csv".format(self.settings["data_location"])

        if exists(activities_file_path):
            lines = open(activities_file_path).readlines()[-1:]  # Assumes the file can fit into memory
            last_line = [line.split()[0] for line in lines]

        with open(activities_file_path, "w") as activites_file:
            csv_reader = csv.reader(activites_file, delimiter=',')

    def get_activities(self, before: datetime.date, after: datetime.date):
        url_format = "{0}/activities?per_page=200".format(self.athlete_base_url)

        if before is not None:
            url_format += "&before={0}".format(before.strftime('%s'))

        if after is not None:
            url_format += "&after={0}".format(after.strftime('%s'))

        activities = []

        header = {'Authorization': 'Bearer ' + self.strava_tokens['access_token']}

        page = 1
        while True:
            the_url = "{0}&page={1}".format(url_format, page)
            print(the_url)
            fetched_activites = self.fetch_from_strava(the_url, header)

            if len(fetched_activites) == 0:
                break

            activities.append(fetched_activites)

            page = page + 1

        return activities

    def get_activity_detail(self, header, activity_id, output_directory):
        the_url = "{0}/{1}".format(self.activity_base_url, activity_id)
        file_path = "{0}{1}_activityDetail.json".format(output_directory, activity_id)

        if exists(file_path) and output_directory:
            with open(file_path, "r") as file:
                data = json.loads(file.read())
            return data

        param = {'include_all_efforts': 'true'}
        response = self.fetch_from_strava(the_url, header, param)

        if output_directory:
            with open(file_path, "w") as file:
                json.dump(response, file, indent=4)

        return response

    def get_activity_comments(self, header, activity_id, output_directory):
        the_url = "{0}/{1}/comments".format(self.activity_base_url, activity_id)
        file_path = "{0}{1}_activityComments.json".format(output_directory, activity_id)

        if exists(file_path) and output_directory:
            with open(file_path, "r") as file:
                data = json.loads(file.read())
            return data

        response = self.fetch_from_strava(the_url, header)

        if output_directory:
            with open(file_path, "w") as file:
                json.dump(response, file, indent=4)

        return response

    def get_activity_kudos(self, header, activity_id, output_directory):
        the_url = "{0}/{1}/kudos".format(self.activity_base_url, activity_id)
        file_path = "{0}{1}_activityKudos.json".format(output_directory, activity_id)

        if exists(file_path) and output_directory:
            with open(file_path, "r") as file:
                data = json.loads(file.read())
            return data

        response = self.fetch_from_strava(the_url, header)

        if output_directory:
            with open(file_path, "w") as file:
                json.dump(response, file, indent=4)

        return response

    def get_data(self, activities, data_type, output_dir):

        header = {'Authorization': 'Bearer ' + self.strava_tokens['access_token']}

        for a in activities:
            if data_type == "all":
                detail = self.get_activity_detail(header, a, output_dir)
                if detail["comment_count"] > 0:
                    self.get_activity_comments(header, a, output_dir)
                if detail["kudos_count"] > 0:
                    self.get_activity_kudos(header, a, output_dir)
                return
            if "detail" in data_type:
                self.get_activity_detail(header, a, output_dir)
            if "comments" in data_type:
                self.get_activity_comments(header, a, output_dir)
            if "kudos" in data_type:
                self.get_activity_kudos(header, a, output_dir)

