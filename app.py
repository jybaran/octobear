from flask import Flask, request, url_for, redirect, render_template
import json, urllib2

app = Flask(__name__)

@app.route("/")
def index():
    return "hello"

@app.route("/t/<tag>")
def tag(tag="manatee"):
    url = "http://8tracks.com/mix_sets/tags:%s.json?include=mixes&api_key=b72f8beba38aa9fb230d52bf6f45e2baf9fbf322"
    #add tags w/ +
    #spaces to underscores
    #alternately keyword:<SEARCH TERM>
    url = url%(tag)
    request = urllib2.urlopen(url)
    resultstring = request.read()
    #result = json.loads(resultstring)
    #s = ""
    return resultstring

if __name__ == "__main__":
    app.debug = True
    app.run()
