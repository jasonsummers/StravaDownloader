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

        if not exists('strava_tokens.json'):
            tokenUrl = "http://www.strava.com/oauth/authorize?client_id=" + str(self.settings["strava_client_id"]) + \
                       "&response_type=code&redirect_uri=http://localhost/exchange_token&approval_prompt=force&" + \
                       "scope=read,activity:read_all,activity:write,profile:read_all"
            print(tokenUrl)
            self.get_strava_tokens(False)
            return

        with open('strava_tokens.json') as json_file:
            self.strava_tokens = json.load(json_file)

        if self.strava_tokens['expires_at'] < time.time():
            self.get_strava_tokens(True)

    def get_strava_tokens(self, refresh: bool):
        post_data = {
            'client_id': self.settings['strava_client_id'],
            'client_secret': self.settings['strava_client_secret']
        }

        if refresh:
            post_data['grant_type'] = 'refresh_token'
            post_data['refresh_token'] = self.strava_tokens['refresh_token']
        else:
            code = input("Paste Code Here:")
            post_data['grant_type'] = 'authorization_code'
            post_data['code'] = code

        response = requests.post(
            url='https://www.strava.com/oauth/token',
            data=post_data
        )

        new_strava_tokens = response.json()
        with open('strava_tokens.json', 'w') as outfile:
            json.dump(new_strava_tokens, outfile)

        self.strava_tokens = new_strava_tokens

    def get_token(self):
        return self.strava_tokens['access_token']

    def fetch_from_strava(self, url, header, param=""):
        max_retries = 3
        retry_count = 0

        while retry_count < max_retries:
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
                if e["field"] == "rate limit":
                    print("Rate Limit Error detected. Waiting 16 minutes before continuing.")
                    time.sleep(16 * 60)

            retry_count += 1

        return None

    def get_activities(self, before: datetime.date, after: datetime.date):
        url_format = "{0}/activities?per_page=200".format(self.athlete_base_url)

        if before is not None:
            url_format += "&before={0}".format(before.strftime('%s'))

        if after is not None:
            url_format += "&after={0}".format(after.strftime('%s'))

        activities = []
        header = self.generate_header()

        page = 1
        while True:
            the_url = "{0}&page={1}".format(url_format, page)

            fetched_activites = self.fetch_from_strava(the_url, header)

            if len(fetched_activites) == 0:
                break

            for a in fetched_activites:
                activities.append(a)

            page = page + 1

        return activities

    def get_activity_detail(self, activity_id, output_directory):
        header = self.generate_header()
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

    def get_activity_comments(self, activity_id, output_directory):
        header = self.generate_header()
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

    def get_activity_kudos(self, activity_id, output_directory):
        header = self.generate_header()
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

        for a in activities:
            if data_type == "all":
                detail = self.get_activity_detail(a, output_dir)
                if detail["comment_count"] > 0:
                    self.get_activity_comments(a, output_dir)
                if detail["kudos_count"] > 0:
                    self.get_activity_kudos(a, output_dir)
                return
            if "detail" in data_type:
                self.get_activity_detail(a, output_dir)
            if "comments" in data_type:
                self.get_activity_comments(a, output_dir)
            if "kudos" in data_type:
                self.get_activity_kudos(a, output_dir)

    def get_athlete(self):
        header = self.generate_header()
        response = self.fetch_from_strava(self.athlete_base_url, header)
        return response

    def generate_header(self):
        header = {'Authorization': 'Bearer ' + self.strava_tokens['access_token']}
        return header
