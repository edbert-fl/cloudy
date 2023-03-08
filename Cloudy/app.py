from calendar import c
import json
import os

from flask import Flask, jsonify, flash, redirect, render_template, request
from flask_session import Session
from pip._vendor import requests

from functions import locate, lookup, find, local_time

# Configure application
template_dir = os.path.abspath('templates')
app = Flask(__name__, template_folder=template_dir)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"

Session(app)

@app.route("/", methods = ['POST', 'GET'])
def index():
    if request.method == "GET":
        return render_template("index.html")
    
    if request.method == "POST":
        city = request.form.get("city")

        if not city:
            return render_template("error.html", status="404", reason="No input detected", time=None)
        elif city.isdigit():
            return render_template("error.html", status="404", reason="Format error", time=None)

        try:
            location = locate(city)
            weather = lookup(location["lat"], location["lon"])
            time = local_time(weather["dt"], weather["tz"])
            return render_template("results.html", weather=weather, location=location, time=time)
        except:
            return render_template("error.html", status=404, reason="Location not found", time=None)

@app.route("/search")
def search(): 
    c = request.args.get("c")
    if c:
        city = find(c)
    else:
        city = {"error": "No search term provided"}
    return jsonify(city)