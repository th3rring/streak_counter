#!flask/bin/python
import logging
import time
import datetime

from flask import Flask, render_template, redirect, url_for, request, jsonify
from stravalib import Client

class Tracker:

    # Strava client to hold information for tracker.
    client = Client()

    # Time token expires at
    token_expires_at = None

    # Time in seconds between refreshes.
    sleep_time_ = 300

    # Number of target activities per week.
    target_ = 4

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

            time.sleep(self.sleep_time_)

app = Flask(__name__)
app.config.from_envvar('APP_SETTINGS')

tracker = Tracker()

@app.route("/")
def login():
    c = Client()
    url = c.authorization_url(client_id=app.config['STRAVA_CLIENT_ID'],
                              redirect_uri=url_for('.logged_in', _external=True),
                              approval_prompt='auto')
    return render_template('login.html', authorize_url=url)


@app.route("/strava-oauth")
def logged_in():
    """
    Method called by Strava (redirect) that includes parameters.
    - state
    - code
    - error
    """
    error = request.args.get('error')
    state = request.args.get('state')
    if error:
        return render_template('login_error.html', error=error)
    else:
        code = request.args.get('code')
        access_token = tracker.client.exchange_code_for_token(client_id=app.config['STRAVA_CLIENT_ID'],
                                                      client_secret=app.config['STRAVA_CLIENT_SECRET'],
                                                      code=code)
        tracker.set_expiration(access_token['expires_at'])
        strava_athlete = tracker.client.get_athlete()


        return render_template('login_results.html', athlete=strava_athlete, access_token=access_token)

@app.route('/button_callback')
def button_callback():
    tracker.run()

    return 'nothing'


if __name__ == '__main__':
    app.run(debug=True)
