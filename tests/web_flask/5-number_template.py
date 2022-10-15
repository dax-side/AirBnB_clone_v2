#!/usr/bin/python3
""" Starts a flask web application
    host=0.0.0.0 port= 5000
    Routes: 6
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
    """ C route that takes in a text varible
        displays "C" followed by the value of the text
    """
    return "C {}".format(escape(text.replace("_", " ")))


@app.route("/python", defaults={"text": "is cool"}, strict_slashes=False)
@app.route("/python/<text>", strict_slashes=False)
def python(text):
    """ Python route that displays "Python" followed by the value of the text
            variable (replaces the underscore _ symbols with a space )
            The default value of text is "is cool"
    """
    return "Python {}".format(escape(text.replace("_", " ")))


@app.route("/number/<int:n>", strict_slashes=False)
def route_number(n):
    """ Number route that takes n variable and display:
            n is a number only if n is an integer
    """
    return "{} is a number".format(n)


@app.route("/number_template/<int:n>", strict_slashes=False)
def number_template(n):
    """ Number template route"""
    from flask import render_template
    return render_template("5-number.html", number=n)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
