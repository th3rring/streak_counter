import time
import datetime
import pickle

from stravalib import Client
from display import Display

class Tracker:

    def __init__(self):
        # Strava client to hold information for tracker.
        self.client = Client()

        # Time token expires at.
        self.token_expires_at_ = None

        # Client information.
        self.client_id = None
        self.client_secret = None

        # Time in seconds between refreshes.
        self.sleep_time_ = 300

        # Number of target activities per week.
        self.target_ = 4

        # Private display object.
        self.display_ = Display()

        # Activity tracking variables.
        self.start_date = datetime.datetime.utcnow().date()
        self.next_week  = self.start_date + datetime.timedelta(weeks=1)
        self.week_streak = 0
        self.num_activities = 0

        # Filename of save file.
        self.save_file_ = 'streak.yaml'


    def set_expiration(self, token_expires_at):
        self.token_expires_at_ = token_expires_at

    def set_client_info(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret

    def save_status(self):
        save_obj = {'start_date' : self.start_date, 'next_week' : self.next_week, 
                'week_streak' : self.week_streak, 'num_activities' : self.num_activities}
        with open(self.save_file_, 'wb') as save_file:
            pickle.dump(save_obj, save_file)

    def load_status(self):
        save_obj = None
        try:
            with open(self.save_file_, 'rb') as save_file:
                save_obj = pickle.load(save_file)
            self.start_date = save_obj['start_date']
            self.next_week = save_obj['next_week']
            self.week_streak = save_obj['week_streak']
            self.num_activities = save_obj['num_activities']
        except (OSError, IOError, EOFError) as e:
            print('Nothing in this save file, going to save defaults.')
            self.save_status()

    def update(self):
        self.save_status()
        self.display_.show(self.week_streak, self.target_ - self.num_activities, self.target_)



    def run(self):
        # Save start date/time
        # Ask Strava for activities since 1 week ago
        # If len(activities) >= goal increment streak
        # Check that token won't expire in 12 hours
        # If token needs refreshing, refresh it
        # Sleep for sleep_time
        self.load_status()
        self.update()
        while(True):
            # Refresh token if necessary.
            if time.time() > self.token_expires_at_:
                refresh_response = self.client.refresh_access_token(client_id=self.client_id,
                                                      client_secret=self.client_secret,
                                                      refresh_token=self.client.refresh_token)
                self.token_expires_at_ = refresh_response['expires_at']
                print('Refreshing token, new one expires at {}'
                        .format(str(refresh_response['expires_at'])))

            new_activities = len(list(self.client.get_activities(after = self.start_date.isoformat())))

            # Handle null return from Strava servers.
            if not new_activities:
                new_activities = 0
            print(new_activities)

            if new_activities != self.num_activities:
                print("New activities detected!")
                self.num_activities = new_activities
                self.update()

            for activity in self.client.get_activities(after = self.start_date.isoformat()):
                print("{0.name} {0.moving_time}".format(activity))


            # Check if we've hit the target for this week.
            if self.num_activities >= self.target_:
                self.week_streak += 1
                self.update()

            cur_date = datetime.datetime.utcnow().date()

            # Check if it's next week.
            if cur_date == self.next_week:

                # Check if we haven't hit our target and reset.
                if self.num_activities < self.target_:
                    self.week_streak = 0

                # Advance the date to a week from now.
                self.start_date = cur_date
                self.next_week = cur_date + datetime.timedelta(weeks=1)
                self.update()

            time.sleep(self.sleep_time_)
