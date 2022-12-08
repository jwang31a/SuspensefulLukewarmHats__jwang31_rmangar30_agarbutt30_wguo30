from flask import Flask, session, render_template, request
import sqlite3

app = Flask(__name__)

@app.route("/")
def landing():
    return render_template("login.html")

@app.route("/register")
def register():
    return render_template("register.html")

if __name__ == "__main__": 
    app.debug = True
    app.run()    