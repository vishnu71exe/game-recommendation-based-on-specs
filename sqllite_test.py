#Steam API pull
import requests
import json
import sqlite3
from bs4 import BeautifulSoup

connection=sqlite3.connect("data1.db")
cur=connection.cursor()

command1="CREATE TABLE IF NOT EXISTS game_details(appid INTEGER PRIMARY KEY,name TEXT,price TEXT,img TEXT,dev TEXT,pub TEXT,pl_pc INTEGER,pl_mac INTEGER,pl_lin INTEGER,m_rate INTEGER,genre TEXT,relese TEXT,desc TEXT) "
command2="CREATE TABLE IF NOT EXISTS sreq_min(appid INTEGER PRIMARY KEY, process TEXT,graphics TEXT,storage TEXT,ram TEXT)"
command3="CREATE TABLE IF NOT EXISTS sreq_rec(appid INTEGER PRIMARY KEY, process TEXT,graphics TEXT,storage TEXT,ram TEXT)"

cur.execute(command1)
cur.execute(command2)
cur.execute(command3)


id=int(input("enter the game id:"))

def parse(html,t):
    pro=None

    soup=BeautifulSoup(html,'lxml')

    for li in soup.find_all("li"):
        lable=li.find("strong")
        if lable and t in lable.get_text():
            pro=li.get_text(strip=True)
            pro=pro.replace(t,"")
            pro=pro.strip()
            break
    return pro


res=requests.get("https://store.steampowered.com/api/appdetails/?appids="+str(id)+"&lag=en")
out=res.json()

#12 game details fields

name=out[str(id)]["data"]["name"]
price=out[str(id)]["data"]["price_overview"]['final_formatted']
img=out[str(id)]["data"]["header_image"]
developers=out[str(id)]["data"]["developers"][0]
publishers=out[str(id)]["data"]["publishers"][0]
genre1=out[str(id)]["data"]["genres"][0]["description"]
relese=out[str(id)]["data"]["release_date"]["date"]
desc=out[str(id)]["data"]["short_description"]



# 4 specs fields

process_m=out[str(id)]["data"]["pc_requirements"]['minimum']
graphics_m=out[str(id)]["data"]["pc_requirements"]['minimum']
storage_m=out[str(id)]["data"]["pc_requirements"]['minimum']
ram_m=out[str(id)]["data"]["pc_requirements"]['minimum']

try:
    process_r=out[str(id)]["data"]["pc_requirements"]['recommended']
    graphics_r=out[str(id)]["data"]["pc_requirements"]['recommended']
    storage_r=out[str(id)]["data"]["pc_requirements"]['recommended']
    ram_r=out[str(id)]["data"]["pc_requirements"]['recommended']

    cur.execute("INSERT INTO sreq_rec VALUES(?,?,?,?,?)",(id,str(parse(process_r,"Processor:")),str(parse(graphics_r,"Graphics:")),str(parse(storage_r,"Storage:")),str(parse(ram_r,"Memory:"))))


except KeyError:
    print("no recommended")




cur.execute("INSERT INTO game_details VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)",(id,name,price,img,developers,publishers,plat_pc,plat_mac,plat_linux,m_rate,genre1,relese,desc))
cur.execute("INSERT INTO sreq_min VALUES(?,?,?,?,?)",(id,str(parse(process_m,"Processor:")),str(parse(graphics_m,"Graphics:")),str(parse(storage_m,"Storage:")),str(parse(ram_m,"Memory:"))))



cur.execute("SELECT * FROM sreq_min")

results=cur.fetchall()
#print(results)

connection.commit()

print(name)
print(price)
print(img)
print(developers)
print(publishers)
print(plat_pc)
print(plat_mac)
print(plat_linux)
print(genre1)
print(m_rate)
print(relese)
print(desc)
print(parse(process_m,"Processor:"))
print(parse(graphics_m,"Graphics:"))
print(parse(storage_m,"Storage:"))
print(parse(ram_m,"Memory:"))

try:
    print(parse(storage_r,"Storage:"))
    print(parse(ram_r,"Memory:"))
    print(parse(graphics_r,"Graphics:"))
    print(parse(process_r,"Processor:"))
except NameError:
    print(" ")


