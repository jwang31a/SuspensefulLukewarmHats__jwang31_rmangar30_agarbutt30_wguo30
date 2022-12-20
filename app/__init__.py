from flask import Flask, session, render_template, request, redirect
import sqlite3, auth, os
import json, urllib.request

#creates flask app
app = Flask(__name__)
app.secret_key = os.urandom(32)  # set up the session with a secret key
app.config['s'] = app.secret_key

#calls function from auth.py that sets up acc database
DB_FILE="accounts.db"
db = sqlite3.connect(DB_FILE, check_same_thread=False)
c = db.cursor()

auth.verify_accounts()

#landing page (first page user sees when loading link)
@app.route("/", methods = ["GET", "POST"])
def landing():
    #if user is already logged in
    if "username" in session:
        return redirect("/homepage", code=307)
    if request.method == "POST":
        # deals with login and register buttons being clicked
        if request.form.get("register") == "register":
            auth.add_accounts(request.form["username_register"], request.form["password_register"])
            return render_template("login.html", color = "success", message = "Successfully registered")
        if request.form.get("login") == "login":

            truth = auth.get_accounts(request.form["username_login"], request.form["password_login"])

            #verifies login info
            if truth:
                session['username'] = request.form["username_login"]
                return redirect("/homepage", code=307)
            else:
                return render_template('login.html', color = "danger", message = "Incorrect Username and/or Password")

    return render_template("login.html")



@app.route("/homepage", methods = ["GET", "POST"])
def homepage():
    return render_template("homepage.html")



@app.route("/theatres", methods = ["GET", "POST"])
def theatres():
    return render_template("theatres.html")



@app.route("/anime", methods = ["GET", "POST"])
def anime():

    key = 'YaI3KDpNull6LCiQp3skU1ybBUQCEUD0bC6daLAW'
    response = requests.get(f'https://api.watchmode.com/v1/list-titles/?apiKey={key}&sort_by=popularity_asc&limit=5')
    response = requests.get(f'https://api.watchmode.com/v1/list-titles/?apiKey={key}&release_date_start=20220101&limit=5')

    return render_template("anime.html")



@app.route("/homepage/search", methods = ["GET", "POST"])
def homepage_search():
    q =  request.form.get("query")

    #read apikey from key_nasa.txt
    key = open("../app/keys/key_omdapi.txt", "r").read()
    url = f"https://www.omdbapi.com/?apikey={key}&t={q}"
    url = url.replace(" ", "+")

    longplot = f"https://www.omdbapi.com/?apikey={key}&t={q}&plot=full"
    longplot = longplot.replace(" ", "+")

    # opens url as a string or Request object
    data = urllib.request.urlopen(url)
    dict = json.load(data)
    print(dict)

    #need to handle if no search results are returned from api call
    return(render_template('homepage.html',title = dict['Title'],image=dict['Poster'], descriptionshort=dict['Plot'],descriptionlong=json.load(urllib.request.urlopen(longplot))['Plot']))



@app.route("/theatres/search", methods = ["GET", "POST"])
def theatres_search():
    q = request.form.get("query")

    #read apikey from key_serpapi.txt
    key = open("keys/key_serpapi.txt", "r").read()
    url = f"https://serpapi.com/search?engine=google&location=New+York,+United+States&api_key={key}&q={q}+showtimes"
    url = url.replace(" ", "+")

    # opens url as a string or Request object
    data = urllib.request.urlopen(url)
    dict = json.load(data)

    # be weary, not all movies return showtimes data! if a dict["showtimes"]
    # returns a KeyError that means no showtimes results were found for that
    # movie, so just say "no upcoming showtimes" or something like that
    data = dict['showtimes']

    return data



@app.route("/homepage/randomize", methods = ["GET", "POST"])
def homepage_randomize():
    #read apikey from key_nasa.txt
    key = open("../app/keys/key_omdapi.txt", "r").read()
    url = f"https://www.omdbapi.com/?apikey={key}&t={q}"
    url = url.replace(" ", "+")

    longplot = f"https://www.omdbapi.com/?apikey={key}&t={q}&plot=full"
    longplot = longplot.replace(" ", "+")

    # opens url as a string or Request object
    data = urllib.request.urlopen(url)
    dict = json.load(data)
    print(dict)

    #need to handle if no search results are returned from api call
    return(render_template('homepage.html',title = dict['Title'],image=dict['Poster'], descriptionshort=dict['Plot'],descriptionlong=json.load(urllib.request.urlopen(longplot))['Plot']))



@app.route("/logout", methods = ['POST'])
def logout():
    if "username" in session:
        try:
            session.pop('username') #gets rid of session
        except:
            return redirect("/")
    #db.close()
    #dbstory.close()
    return redirect("/")#goes home


#if user tries to search for a movie that doesn't exist, there won't be any information, so we can't access the dictionary
#this handles the nonexistent key
@app.errorhandler(KeyError)
def handle_key(e):
    return redirect("/homepage", code=307)

@app.errorhandler(404)
def not_found(e):
    return redirect("/homepage", code=307)

if __name__ == "__main__":
    app.debug = True
    app.run()
