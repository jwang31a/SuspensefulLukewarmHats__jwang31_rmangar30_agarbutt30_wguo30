'''
SuspensefulLukewarmHuts - Ravindra Mangar
SoftDev
p01: ArRESTed Development
08-12-22
'''

import os, sqlite3

DB_FILE="users.db"
db = sqlite3.connect(DB_FILE, check_same_thread=False)
c = db.cursor()

def verify_accounts():
  #DB_FILE="accounts.db"
  #db = sqlite3.connect(DB_FILE, check_same_thread=False)
  #c = db.cursor()
  try:
    c.execute("CREATE TABLE accounts(username TEXT_UNIQUE, movies TEXT);")
  except:
    pass

def add_accounts(username, movies):
  #DB_FILE="accounts.db"
  #db = sqlite3.connect(DB_FILE, check_same_thread=False)
  #c = db.cursor()
  current = get_accounts(username)
  for item in movies:
    current.append(item)
  print(f"INSERT: {current}")
  #try:
  c.execute("UPDATE accounts WHERE username(?) SET movies(?);")
  #except:
  #  c.execute("INSERT INTO accounts VALUES(?, ?);", [username, "_".join(current)])

def get_accounts(username):
    #DB_FILE="accounts.db"
    #db = sqlite3.connect(DB_FILE, check_same_thread=False)
    #c = db.cursor()
    c.execute("SELECT * FROM accounts;")
    response = c.fetchall()
    #print(response)
    for account in response:
        if account[0] == username:
            print(f"GET {account[1]}")
            return account[1].split("_")
    return []

#testing if these functions work
'''
add_accounts("dudu", "dudu")
add_accounts("111", "111")
add_accounts("222", "222")
print(get_accounts("dudu", "dudu"))
'''
