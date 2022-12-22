'''
SuspensefulLukewarmHuts - Ravindra Mangar
SoftDev
p01: ArRESTed Development
08-12-22
'''

import os, sqlite3

DB_FILE="accounts.db"
db = sqlite3.connect(DB_FILE, check_same_thread=False)
c = db.cursor()

def verify_accounts():
  #DB_FILE="accounts.db"
  #db = sqlite3.connect(DB_FILE, check_same_thread=False)
  #c = db.cursor()
  try:
    c.execute("CREATE TABLE accounts(username TEXT, password TEXT);")
  except:
    pass

def add_accounts(username, password):
  #DB_FILE="accounts.db"
  #db = sqlite3.connect(DB_FILE, check_same_thread=False)
  #c = db.cursor()
  c.execute("INSERT INTO accounts VALUES(?, ?);", [username, password])

def get_accounts(username, password):
    #DB_FILE="accounts.db"
    #db = sqlite3.connect(DB_FILE, check_same_thread=False)
    #c = db.cursor()
    c.execute("SELECT * FROM accounts;")
    response = c.fetchall()
    #print(response)
    for account in response:
        if account[0] == username and account[1] == password:
            return True
    return False

#testing if these functions work
'''
add_accounts("dudu", "dudu")
add_accounts("111", "111")
add_accounts("222", "222")
print(get_accounts("dudu", "dudu"))
'''
