
import requests
from pprint import pprint as pp
import json

user = 'oksanatsuverkalova'
url = requests.get(f'https://api.github.com/users/{user}/repos')
repos = []

if url.ok:
    data = url.json()

if url.ok:
    path = "repositories_list.json"
    with open(path,'w') as f:
        json.dump(data, f)

for n in data:
    print(n['name'])