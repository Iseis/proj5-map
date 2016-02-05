"""
simple flask program for opening up a file setting some locations
and sending it to the client.
"""

import flask
from flask import render_template
from flask import request
from flask import url_for


import json
import logging
import process_places

###
# Globals
###
app = flask.Flask(__name__)
places = "data/places.txt"  # This should be configurable
import CONFIG

import uuid
app.secret_key = str(uuid.uuid4())
app.debug=CONFIG.DEBUG
app.logger.setLevel(logging.DEBUG)


@app.route("/")
@app.route("/index")
def interested():
    app.logger.debug("Main page entry")
    if 'places' not in flask.session:
      app.logger.debug("Processing raw schedule file")
      raw = open('data/places.txt')
      flask.session['places'] = process_places.process(raw)

    return flask.render_template('leaflet_example.html')



@app.errorhandler(404)
def page_not_found(error):
    app.logger.debug("Page not found")
    flask.session['linkback'] =  flask.url_for("index")
    return flask.render_template('page_not_found.html'), 404

#############
#
# Set up to run from cgi-bin script, from
# gunicorn, or stand-alone.
#


if __name__ == "__main__":
    # Standalone, with a dynamically generated
    # secret key, accessible outside only if debugging is not on
    import uuid
    app.secret_key = str(uuid.uuid4())
    app.debug=CONFIG.DEBUG
    app.logger.setLevel(logging.DEBUG)
    if app.debug:
        print("Accessible only on localhost")
        app.run(port=CONFIG.PORT)  # Accessible only on localhost
    else:
        print("Opening for global access on port {}".format(CONFIG.PORT))
        app.run(port=CONFIG.PORT, host="0.0.0.0")
else:
    # Running from cgi-bin or from gunicorn WSGI server,
    # which makes the call to app.run.  Gunicorn may invoke more than
    # one instance for concurrent service.
    app.secret_key = CONFIG.secret_key
    app.debug=False

