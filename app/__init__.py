from flask import Flask, session, render_template, request, redirect
import sqlite3, auth, os, requests
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
    return render_template("homepage.html", status = 'start')



@app.route("/theatres", methods = ["GET", "POST"])
def theatres():
    return render_template("theatres.html", status = 'start')



@app.route("/anime", methods = ["GET", "POST"])
def anime():
    key = open("../app/keys/key_anime.txt", "r").read()

    #ANIME
    response = requests.get(f'https://api.watchmode.com/v1/list-titles/?apiKey={key}&sort_by=popularity_asc&limit=5&genres=33')
    response = requests.get(f'https://api.watchmode.com/v1/list-titles/?apiKey={key}&release_date_start=20220101&limit=5&genres=33')
    data = urllib.request.urlopen(f"https://api.watchmode.com/v1/list-titles/?apiKey={key}&sort_by=popularity_dsc&limit=12&genres=33")
    data2 = urllib.request.urlopen(f'https://api.watchmode.com/v1/list-titles/?apiKey={key}&release_date_start=20220101&limit=12&genres=33')
    anime = json.load(data)
    anime2 = json.load(data2)
    titleid = []
    titleid2 = []
    cardinfo = {}
    cardinfo2 = {}
    for items in anime['titles']:
        titleid.append(items['id'])
    for ids in titleid:
        info = json.load(urllib.request.urlopen(f'https://api.watchmode.com/v1/title/{ids}/details/?apiKey={key}'))
        cardinfo[info['title']] = [info['poster'],info['plot_overview']]
    for items in anime2['titles']:
        titleid2.append(items['id'])
    for ids in titleid2:
        info = json.load(urllib.request.urlopen(f'https://api.watchmode.com/v1/title/{ids}/details/?apiKey={key}'))
        cardinfo2[info['title']] = [info['poster'],info['plot_overview']]
    #print(anime)
    #print(cardinfo)
    
    #COMEDY
    response = requests.get(f'https://api.watchmode.com/v1/list-titles/?apiKey={key}&sort_by=popularity_asc&limit=5&genres=4')
    response = requests.get(f'https://api.watchmode.com/v1/list-titles/?apiKey={key}&release_date_start=20220101&limit=5&genres=4')
    data2 = urllib.request.urlopen(f"https://api.watchmode.com/v1/list-titles/?apiKey={key}&sort_by=popularity_dsc&limit=5&genres=4")
    comedy = json.load(data2)
    ##print(comedy)
    
    return render_template("anime.html", anime = cardinfo, anime2 = cardinfo2)


@app.route("/comedy", methods = ["GET", "POST"])
def comedy():
    key = open("../app/keys/key_watchmode.txt", "r").read()

    #COMEDY
    response = requests.get(f'https://api.watchmode.com/v1/list-titles/?apiKey={key}&sort_by=popularity_asc&limit=12&genres=4')
    response = requests.get(f'https://api.watchmode.com/v1/list-titles/?apiKey={key}&release_date_start=20220101&limit=12&genres=4')
    data = urllib.request.urlopen(f"https://api.watchmode.com/v1/list-titles/?apiKey={key}&sort_by=popularity_dsc&limit=12&genres=4")
    data2 = urllib.request.urlopen(f'https://api.watchmode.com/v1/list-titles/?apiKey={key}&release_date_start=20220101&limit=12&genres=4')
    comedy = json.load(data)
    comedy2 = json.load(data2)
    titleid = []
    titleid2 = []
    cardinfo = {}
    cardinfo2 = {}
    for items in comedy['titles']:
        titleid.append(items['id'])
    for ids in titleid:
        info = json.load(urllib.request.urlopen(f'https://api.watchmode.com/v1/title/{ids}/details/?apiKey={key}'))
        cardinfo[info['title']] = [info['poster'],info['plot_overview']]
    for items in comedy2['titles']:
        titleid2.append(items['id'])
    for ids in titleid2:
        info = json.load(urllib.request.urlopen(f'https://api.watchmode.com/v1/title/{ids}/details/?apiKey={key}'))
        cardinfo2[info['title']] = [info['poster'],info['plot_overview']]
    #print(comedy)
    #print(cardinfo)
    
    return render_template("comedy.html", comedy = cardinfo, comedy2 = cardinfo2)



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
    return(render_template('homepage.html',title = dict['Title'],image=dict['Poster'], descriptionshort=dict['Plot'],descriptionlong=json.load(urllib.request.urlopen(longplot))['Plot'], status = 'using'))



@app.route("/theatres/search", methods = ["GET", "POST"])
def theatres_search():
    q = request.form.get("query")

    #read apikey from key_serpapi.txt
    key = open("keys/key_serpapi.txt", "r").read()
    url = f"https://serpapi.com/search?engine=google&location=New+York,+United+States&api_key={key}&q={q}+english+showtimes"
    url = url.replace(" ", "+")

    # opens url as a string or Request object
    data = urllib.request.urlopen(url)
    dict = json.load(data)

    # be weary, not all movies return showtimes data! if a dict["showtimes"]
    # returns a KeyError that means no showtimes results were found for that
    # movie, so just say "no upcoming showtimes" or something like that
    data = dict['showtimes'] #data is list of dictionary
    cinemas = {}
    address= {}
    time = {}
    test = {}

    #print(data)
    for item in data: #goes through all the dictionary within list separated by date
        #print(item)
        #print("\n")
        dictkey = item['day']
        #print(dictkey)
        cinemas.update({dictkey : []})
        for info in item['theaters']: # list of dictionary separated by theatre name
            #print(info)
            #print("\n")
            namekey = info['name']
            address.update({namekey : []})
            time.update({namekey: []})
            cinemas[dictkey].append(namekey)
            address[namekey].append(info['address'])
            #print(cinemas)
            #print("\n")
            for i in info['showing']: #list of dictionary with different type
                time[namekey].append(i['time'])

    #print(cinemas)
    #print(address)
    #print(time)
    
    return render_template('theatres.html',data = data, status = 'ok', theatre = cinemas, location = address, showtime = time)



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

#if user trying to access route that doesn't exist
@app.errorhandler(404)
def not_found(e):
    return redirect("/homepage", code=307)

#if user trying to search for no title (also to make sure the random button doesn't break everything)
@app.errorhandler(NameError)
def name_error(e):
    return redirect("/homepage", code=307)

if __name__ == "__main__":
    app.debug = True
    app.run()
