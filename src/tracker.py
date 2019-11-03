import time
import datetime

from stravalib import Client
from display import Display

class Tracker:

    def __init__(self):
        # Strava client to hold information for tracker.
        self.client = Client()

        # Time token expires at
        self.token_expires_at = None

        # Time in seconds between refreshes.
        self.sleep_time_ = 300

        # Number of target activities per week.
        self.target_ = 4

        self.display = Display()


    def set_expiration(self, token_expires_at):
        self.token_expires_at = token_expires_at

    def run(self):
        # Save start date/time
        # Ask Strava for activities since 1 week ago
        # If len(activities) >= goal increment streak
        # Check that token won't expire in 12 hours
        # If token needs refreshing, refresh it
        # Sleep for sleep_time
        start_date = datetime.datetime.utcnow().date()
        next_week  = start_date + datetime.timedelta(weeks=1)
        week_streak = 0
        while(True):
            # Refresh token if necessary.
            if time.time() > self.token_expires_at:
                refresh_response = self.client.refresh_access_token(client_id=app.config['STRAVA_CLIENT_ID'],
                                                      client_secret=app.config['STRAVA_CLIENT_SECRET'],
                                                      refresh_token=self.client.refresh_token)
                self.token_expires_at = refresh_response['expires_at']
                print('Refreshing token, new one expires at {}'
                        .format(str(refresh_response['expires_at'])))

            num_activities = len(list(self.client.get_activities(after = start_date.isoformat())))

            for activity in self.client.get_activities(after = start_date.isoformat()):
                print("{0.name} {0.moving_time}".format(activity))

            # Handle null return from Strava servers.
            if not num_activities:
                num_activities = 0
            print(num_activities)

            # Check if we've hit the target for this week.
            if num_activities >= self.target_:
                week_streak += 1

            cur_date = datetime.datetime.utcnow().date()

            # Check if it's next week.
            if cur_date == next_week:

                # Check if we haven't hit our target and reset.
                if num_activities < self.target_:
                    week_streak = 0

                # Advance the date to a week from now.
                start_date = cur_date
                next_week = cur_date + datetime.timedelta(weeks=1)

            # Display num_activities, week streak, etc
            self.display.show(week_streak, self.target_ - num_activities, self.target_)

            time.sleep(self.sleep_time_)
