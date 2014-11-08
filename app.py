#!/usr/bin/python
from flask import Flask, render_template, request, redirect, \
    url_for, session, flash
import json, urllib2

app = Flask(__name__)

@app.route("/")
def index():
    query = request.args.get("query",None)
    if query == None:
        #flash("You didn't give us a thing! Try again please.")
        #"RuntimeError: the session is unavailable because no secret key was set.
        #Set the secret_key on the application to something unique and secret."
        #(no idea what this is about)
        return render_template("home.html")
    else:
        return redirect(url_for("query", query=query))


def createJSON(url):
    request = urllib2.urlopen(url+"&api_key=b72f8beba38aa9fb230d52bf6f45e2baf9fbf322")
    resultstring = request.read()
    return json.loads(resultstring)
    
    

@app.route("/<query>")
def query(query):
    url = "http://8tracks.com/mix_sets/tags:%s.json?include=mixes"
    #add tags w/ +
    #spaces to underscores
    #alternately keyword:<SEARCH TERM>
    url = url%(query)
    results = createJSON(url)
    mixID = results["mixes"][0]["id"]
    mixTitle = results["mixes"][0]["name"]
    mixDJ = results["mixes"][0]["user"]["login"]
    
    return render_template("results.html", query=query, mixID=mixID, mixTitle=mixTitle, mixDJ=mixDJ)




if __name__ == "__main__":
    app.debug = True
    app.run()
