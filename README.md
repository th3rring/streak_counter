This is an example Flask application showing how you can use stravalib to help
with getting access tokens.
To run the streak counter, you first have to sign into the web and authenticate this application with Strava. That means that it's necessarily to launch the Flask web application and use their OAuth2 portal first. Follow these instructions to do so!

This is meant to run on a [Raspberry Pi Zero W](https://www.raspberrypi.org/products/raspberry-pi-zero-w/) with a [2.7 inch e-Paper HAT](https://www.amazon.com/gp/product/B07DH48M7N/ref=ppx_yo_dt_b_asin_title_o00_s00?ie=UTF8&psc=1).

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
