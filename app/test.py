import users
import requests

#users.verify_accounts()
#users.add_accounts("Avinda", ["Your Name", "A Silent Voice", "Demon Slayer"])
#users.remove_accounts("Avinda", ["Your Name", "Demon Slayer", "A Silent Voice"])
#print(users.get_accounts("Avinda"))

#key = open("../app/keys/key_omdapi.txt", "r").read()
#print(key)
#response = requests.get(f"https://api.myanimelist.net/v2/anime/season/2017/summer?limit=4")
#print(response)
#print(response.text)

key = 'YaI3KDpNull6LCiQp3skU1ybBUQCEUD0bC6daLAW'
#response1 = requests.get(f'https://api.watchmode.com/v1/genres/?apiKey={key}')
response1 = requests.get(f'https://api.watchmode.com/v1/list-titles/?apiKey={key}&sort_by=popularity_asc&limit=5&genres=33')
response = requests.get(f'https://api.watchmode.com/v1/list-titles/?apiKey={key}&sort_by=popularity_desc&limit=5&genres=33')
#print(response)
print(response.text)
print("\n\n")
print(response1.text)
