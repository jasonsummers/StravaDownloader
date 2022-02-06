import requests
import json
import time

class StravaDataDownloader:

    def __init__(self):
        self.base_url = "https://www.strava.com/api/v3/activities"
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

    def get_activity_detail(self, header, activity_id, output_directory):
        the_url = "{0}/{1}".format(self.base_url, activity_id)

        param = {'include_all_efforts': 'true'}
        response = requests.get(the_url, params=param, headers=header).json()

        if not output_directory:
            return response

        file = open("{0}{1}_activityDetail.json".format(output_directory, activity_id), "w")
        json.dump(response, file, indent=4)
        file.close()

    def get_activity_comments(self, header, activity_id, output_directory):
        the_url = "{0}/{1}/comments".format(self.base_url, activity_id)
        response = requests.get(the_url, headers=header).json()

        if not output_directory:
            return response

        file = open("{0}{1}_activityComments.json".format(output_directory, activity_id), "w")
        json.dump(response, file, indent=4)
        file.close()

    def get_activity_kudos(self, header, activity_id, output_directory):
        the_url = "{0}/{1}/kudos".format(self.base_url, activity_id)
        response = requests.get(the_url, headers=header).json()

        if not output_directory:
            return response

        file = open("{0}{1}_activityKudos.json".format(output_directory, activity_id), "w")
        json.dump(response, file, indent=4)
        file.close()

    def get_data(self, activities, data_type, output_dir):

        header = {'Authorization': 'Bearer ' + self.strava_tokens['access_token']}

        for a in activities:
            if data_type == "detail":
                self.get_activity_detail(header, a, output_dir)
            elif data_type == "comments":
                self.get_activity_comments(header, a, output_dir)
            elif data_type == "kudos":
                self.get_activity_kudos(header, a, output_dir)
            elif data_type == "all":
                self.get_activity_detail(header, a, output_dir)
                self.get_activity_comments(header, a, output_dir)
                self.get_activity_kudos(header, a, output_dir)

