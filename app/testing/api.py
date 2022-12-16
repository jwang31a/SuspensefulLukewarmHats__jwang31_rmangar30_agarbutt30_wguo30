import json, os, urllib.request
from flask import Flask, render_template

#opens key for omdbapi, turns it into string
omdb = open("../keys/key_omdapi.txt").read()
#print(omdb)
watchmode = open("../keys/key_watchmode.txt").read()

app = Flask(__name__)

@app.route("/")
def req():
    #spaces in urls are represented by "+"
    url = f"http://www.omdbapi.com/?apikey={omdb}&t=Infinity+War"
    #print(url)
    info = json.load(urllib.request.urlopen(url))
    #print(info)
    i = info["Poster"]
    print(i)
    with urllib.request.urlopen(f"https://api.watchmode.com/v1/search/?apiKey={watchmode}&search_field=name&search_value=Breaking+Bad") as url:
        data = json.loads(url.read().decode())
        print(data)
    #make sure in jinja templating the brackets are {{ }}
    return render_template("testing.html", imageurl=i)

"""
from serpapi import GoogleSearch

params = {
  "q": "McDonald's",
  "location": "austin, texas, united states",
  "tbm": "lcl",
  "api_key": "secret_api_key"
}

search = GoogleSearch(params)
results = search.get_dict()
local_results = results["local_results"]
"""

if __name__ == "__main__":
    app.debug = True
    app.run()