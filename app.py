#!/usr/bin/python
from flask import Flask, render_template, request, redirect, \
    url_for, session, flash
import json, urllib2

app = Flask(__name__)

@app.route("/")
def main():
    return redirect(url_for("index", error = "search"))

@app.route("/<error>", methods = ["GET", "POST"])
def index(error = None):
    session["count"] = 0
    if request.method == "POST":
        query = request.form["query"]
        if query == "":
            message = "You didn't give us a thing! Try again please."
            return render_template("home.html", error = True, message = message)
        else:
            return redirect(url_for("query", query=query))
    if error == "NoMore":
        message = "Sorry, there are no more playlists with this tag. Try another?"
        return render_template("home.html", error = True, message = message)
    if error == "TagError":
        message = "Sorry, but this tag does not exist. Try another?"
        return render_template("home.html", error = True, message = message)
    return render_template("home.html", error = False)


def createJSON(url):
    request = urllib2.urlopen(url+"&api_key=b72f8beba38aa9fb230d52bf6f45e2baf9fbf322")
    resultstring = request.read()
    return json.loads(resultstring)
    
    

@app.route("/search/<query>", methods = ["GET", "POST"])
def query(query=None):
    if request.method == "POST":
        session["count"] = session["count"] + 1
        return redirect(url_for("query", query = query))
    message = "I am sorry, but this tag does not exist. Try another?"
    url = "http://8tracks.com/mix_sets/tags:%s.json?include=mixes"
    #add tags w/ +
    #spaces to underscores
    #alternately keyword:<SEARCH TERM>
    url = url%(query)
    try:
        results = createJSON(url)
        if session["count"] == len(results["mixes"]):
            return redirect(url_for("index", error = "NoMore"))
        mixID = results["mixes"][session["count"]]["id"]
        mixTitle = results["mixes"][session["count"]]["name"]
        mixDJ = results["mixes"][session["count"]]["user"]["login"]
    except ValueError:
        return redirect(url_for("index", error="TagError"))
    except IndexError:
        return redirect(url_for("index", error="TagError"))
    return render_template("results.html", query=query, mixID=mixID, mixTitle=mixTitle, mixDJ=mixDJ)



if __name__ == "__main__":
    app.debug = True
    app.secret_key = "key_thing"
    app.run()
