#Reading from json

import json
import os
f=open("games.json",'r',encoding='utf-8')
data=json.load(f)

for n in range(0,20):
    print(data[n]['appid'])
