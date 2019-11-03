This is an example Flask application showing how you can use stravalib to help
with getting access tokens.
To run the streak counter, you first have to sign into the web and authenticate this application with Strava. That means that it's necessarily to launch the Flask web application and use their OAuth2 portal first. Follow these instructions to do so!

Installing
====================

Clone this repo to your computer and install the necessary tools by executing 'install.sh':

```
$ ./install.sh
```

Create a Config File
====================

Create a file -- for example `settings.cfg`:

```
$ vim settings.cfg
```
Paste in your Strava client ID and secret:

```python
STRAVA_CLIENT_ID=123
STRAVA_CLIENT_SECRET='deadbeefdeadbeefdeadbeef'
```

Run Server
==========

Run the Flask server, specifying the path to this file in your `APP_SETTINGS`
environment var:

```
$ APP_SETTINGS=settings.cfg python3 server.py
```
