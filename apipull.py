import requests
import json

f=open("games.json",'r',encoding='utf-8')
data=json.load(f)
for n in range(500,550):
    id=data[n]['appid']
    print("id=",id)
    res=requests.get("https://store.steampowered.com/api/appdetails/?appids="+str(id)+"&lag=en")
    out=res.json()
    name=out[str(id)]["data"]["name"]
    req=out[str(id)]["data"]["pc_requirements"]
    print(name)
 
