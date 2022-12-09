'''
SuspensefulLukewarmHuts - Ravindra Mangar
SoftDev
p01: ArRESTed Development
08-12-22
'''

import os, sqlite3

def verify_accounts():
  DB_FILE="accounts.db"
  db = sqlite3.connect(DB_FILE, check_same_thread=False)
  c = db.cursor()
  try:
    c.execute("CREATE TABLE accounts(username TEXT, password TEXT);")
  except:
    pass

def add_accounts(username, password):
  DB_FILE="accounts.db"
  db = sqlite3.connect(DB_FILE, check_same_thread=False)
  c = db.cursor()
  c.execute("INSERT INTO accounts VALUES(?, ?);", [username, password])

def get_accounts(username, password):
  DB_FILE="accounts.db"
  db = sqlite3.connect(DB_FILE, check_same_thread=False)
  c = db.cursor()
  c.execute("SELECT * FROM accounts;")
  response = c.fetchall()
  print(response)
  for account in response:
    if account[0] == username and account[1] == password:
      return True
  return False

print(get_accounts("dudu", "dudu"))