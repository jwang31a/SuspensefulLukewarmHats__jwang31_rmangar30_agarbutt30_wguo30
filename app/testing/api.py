import json, os, urllib.request
from flask import Flask, render_template

#opens key for omdbapi, turns it into string
omdb = open("../keys/key_omdapi.txt").read()
#print(omdb)

app = Flask(__name__)

@app.route("/")
def req():
    #spaces in urls are represented by "+"
    url = f"http://www.omdbapi.com/?apikey={omdb}&t=Infinity+War"
    #print(url)
    info = json.load(urllib.request.urlopen(url))
    i = info["Poster"]
    print(i)
    #make sure in jinja templating the brackets are {{ }}
    return render_template("testing.html", imageurl=i)

if __name__ == "__main__":
    app.debug = True
    app.run()