import users

users.verify_accounts()
users.add_accounts("What", ["Bruh","Bruh2","Bruh3", "Bruh4"])
print(users.get_accounts("What"))
users.add_accounts("What", ["Bruh5"])
print(users.get_accounts("What"))
users.remove_accounts("What", ["Bruh5"])
print(users.get_accounts("What"))
