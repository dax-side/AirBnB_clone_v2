#!/usr/bin/python3
""" Starts a flask web application
    host=0.0.0.0 port= 5000
    Number of Routes: 7
"""

from flask import Flask, escape, render_template


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
    return render_template("5-number.html", number=n)


@app.route("/number_odd_or_even/<int:n>", strict_slashes=False)
def number_odd_even(n):
    """display a HTML page only if n is an integer"""
    num_t = ""
    if n % 2 == 0:
        num_t = "even"
    else:
        num_t = "odd"
    return render_template("6-number_odd_or_even.html", number=n, num_t=num_t)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
