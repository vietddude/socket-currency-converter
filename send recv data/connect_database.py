import json

username = input()
password = input()
data = {
    'username': username,
    'password': password
}

with open('data.json', 'a') as outfile:
    json.dump(data, outfile)
    print('Completed!')
