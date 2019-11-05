#!flask/bin/python
from flask import Flask, render_template, redirect, url_for, request, jsonify
from tracker import Tracker
from stravalib import Client

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
        tracker.set_client_info(app.config['STRAVA_CLIENT_ID'], app.config['STRAVA_CLIENT_SECRET'])
        strava_athlete = tracker.client.get_athlete()


        return render_template('login_results.html', athlete=strava_athlete, access_token=access_token)

@app.route('/button_callback')
def button_callback():
    tracker.run()

    return 'nothing'


if __name__ == '__main__':
    app.run(debug=True)
