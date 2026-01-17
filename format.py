#formatting file

import requests
import json
id=int(input("enter the game id:"))
alldat=[]
res=requests.get("https://store.steampowered.com/api/appdetails/?appids="+str(id)+"&lag=en")
out=res.json()
name=out[str(id)]["data"]["name"]
price=out[str(id)]["data"]["price_overview"]['final_formatted']
alldat.append(out)

with open("data.json","w") as f:
    json.dump(alldat,f)

