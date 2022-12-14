
from flask import Flask, session, render_template, request, redirect
import sqlite3, auth, os

#creates flask app
app = Flask(__name__)
app.secret_key = "hello" #os.urandom(32)  #set up the session with a secret key
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
        if request.form.get("login") == "login":
            truth = auth.get_accounts(request.form["username_login"], request.form["password_login"])
            if truth:
                session['username'] = request.form["username_login"]
                return redirect("/homepage", code=307)
            else:
                return "Incorrect Username and/or Password"

    return render_template("login.html")


@app.route("/homepage", methods = ["GET", "POST"])
def homepage():
    return render_template("homepage.html")

@app.route("/anime", methods = ["GET", "POST"])
def anime():
    return render_template("anime.html")

#can be changed and added to /homepage as form button
#also no way to access this yet
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

if __name__ == "__main__":
    app.debug = True
    app.run()
