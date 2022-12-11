
from flask import Flask, session, render_template, request, redirect
import sqlite3, auth, os

app = Flask(__name__)
app.secret_key = os.urandom(32)  #set up the session with a secret key
app.config['s'] = app.secret_key

@app.route("/", methods = ["GET", "POST"])
def landing():
    if "username" in session:
        return redirect("/homepage")
    if request.method == "POST":
      if request.form.get("register") == "Create an account":
        return render_template("register.html")
      if request.form.get("login") == "login":
        truth = auth.get_accounts(request.form["username"], request.form["password"])
        if truth == True:
          return render_template("homepage.html")
        else:
          return "Incorrect Username and/or Password"
    return render_template("login.html")

@app.route("/register", methods = ["GET", "POST"])
def register():
    if request.method == ["GET", "POST"]:
      if request.form.get("register") == "register":
        auth.add_accounts(request.form["username"], request.form["password"])
        return render_template("login.html")
    return render_template("register.html")

@app.route("/homepage", methods = ["GET", "POST"])
def homepage():
  return render_template("homepage.html")

if __name__ == "__main__":
    app.debug = True
    auth.verify_accounts()
    app.run()
