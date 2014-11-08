#!/usr/bin/python
from flask import Flask, render_template, request, redirect, \
    url_for, flash
import json, urllib2

app = Flask(__name__)

@app.route("/")
def index():
    query = request.args.get("query",None)
    if query == None:
        #have it flash "You didn't give us a thing! Try again please."
        return render_template("home.html")
    else:
        return redirect(url_for("query", query=query))

@app.route("/<query>")
def query(query):
    url = "http://8tracks.com/mix_sets/tags:%s.json?include=mixes&api_key=b72f8beba38aa9fb230d52bf6f45e2baf9fbf322"
    #add tags w/ +
    #spaces to underscores
    #alternately keyword:<SEARCH TERM>
    url = url%(query)
    request = urllib2.urlopen(url)
    resultstring = request.read()
    #result = json.loads(resultstring)
    #s = ""
    return resultstring

if __name__ == "__main__":
    app.debug = True
    app.run()
