
from flask import Flask, session, render_template, request, redirect
import sqlite3, auth, os

#creates flask app
app = Flask(__name__)
app.secret_key = os.urandom(32)  #set up the session with a secret key
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
        #deals with user pressing register or login buttons
        if request.form.get("register") == "Create an account":
            return render_template("register.html")
        elif request.form.get("login") == "login":
            truth = auth.get_accounts(request.form["username"], request.form["password"])
            if truth:
                print(request.form['username'] + "username")
                session['username'] = request.form['username']
                print(session['username'] + "landing")
                return redirect("/homepage", code=307)
            else:
                print(request.form['username'] + "username landing")
                return "Incorrect Username and/or Password"
    return render_template("login.html")

#register page
@app.route("/register", methods = ["GET", "POST"])
def register():
    if request.method == ["GET", "POST"]:
        if request.form.get("register") == "register":
            auth.add_accounts(request.form["username"], request.form["password"])
            return redirect("/", code=307)
    return render_template("register.html")

@app.route("/homepage", methods = ["GET", "POST"])
def homepage():
    print(session['username'] + "session username homepage")
    return render_template("homepage.html")

#can be changed and added to /homepage as form button
#also no way to access this yet
@app.route("/logout")
def logout():
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
