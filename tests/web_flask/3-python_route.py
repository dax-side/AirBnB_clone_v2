#!/usr/bin/python3
""" Starts a flask web application
    host=0.0.0.0 port= 5000
    Routes:
        hello route (/)
        hbnb route (/hbnb)
        c route (/c/<text>): display "C" followed by the value of the text
        python route (/python/<text>): displays "Python" followed by
        the value of the text
            variable (replace underscore _ symbols with a space )
            The default value of text is "is cool"
"""

from flask import Flask, escape


app = Flask(__name__)


@app.route("/", strict_slashes=False)
def index():
    """ Home page"""
    return "Hello HBNB!"


@app.route("/hbnb", strict_slashes=False)
def hbnb():
    """hbnb route """
    return "HBNB"


@app.route("/c/<text>", strict_slashes=False)
def c_route(text):
    """  c route that takes in a text varible"""
    return "C {}".format(escape(text.replace("_", " ")))


@app.route("/python", defaults={"text": "is cool"}, strict_slashes=False)
@app.route("/python/<text>", strict_slashes=False)
def python(text):
    """ python route, takes text argument with default value 'is cool'"""
    return "Python {}".format(text.replace("_", " "))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
