#Steam API pull

import requests
import json
id=int(input("enter the game id:"))
alldat=[]
res=requests.get("https://store.steampowered.com/api/appdetails/?appids="+str(id)+"&lag=en")
out=res.json()
#m_rate=int(out[str(id)]["data"]["metacritic"]["score"]) #int
print(out)
#print("name=",name)
#print("price=",price)

    






