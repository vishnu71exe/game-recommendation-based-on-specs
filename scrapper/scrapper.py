
import requests
import json
import sqlite3
import time
import csv
from bs4 import BeautifulSoup


connection=sqlite3.connect("data6.db")
cur=connection.cursor()

command1="CREATE TABLE IF NOT EXISTS game_details(appid INTEGER PRIMARY KEY,name TEXT,price TEXT,img TEXT,dev TEXT,pub TEXT,pl_pc INTEGER,pl_mac INTEGER,pl_lin INTEGER,m_rate INTEGER,genre TEXT,relese TEXT,desc TEXT,free INTEGER) "
command2="CREATE TABLE IF NOT EXISTS sreq_min(appid INTEGER PRIMARY KEY, process TEXT,graphics TEXT,storage TEXT,ram TEXT)"
command3="CREATE TABLE IF NOT EXISTS sreq_rec(appid INTEGER PRIMARY KEY, process TEXT,graphics TEXT,storage TEXT,ram TEXT)"

cur.execute(command1)
cur.execute(command2)
cur.execute(command3)


#id=int(input("enter the game id:"))

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


#get list of all games
f=open("games.json",'r',encoding='utf-8')
data=json.load(f)
count=0
n=1
app_list=[]
try:
    while(1):

        dat=data[n]['appid']
        app_list.append(dat)
        if dat!=0:
            count+=1
        n+=1
except:
    print("finished")


m=0
with open("till_scrapped.txt","r") as f:
    m=int(f.read())
    print("m=",m)
f.close()

c1=1

t=len(app_list)

while m<t:


    print("**************")
    id=app_list[m]
    print("m=",m)
    print("id=",id)
    ignore=0

    try:
        res=requests.get("https://store.steampowered.com/api/appdetails/?appids="+str(id)+"&lag=en")
        out=json.loads(res.content.decode("utf-8-sig"))
    except:
        with open("redo_apps.csv","a",newline="",encoding='utf-8') as f2:
            writer=csv.writer(f2)
            writer.writerow([m,id])
            #f2.write(str(m))
        f2.close()
        print("api pull failed")


    if res.status_code==200:
        print("STATUS:",res.status_code)
    elif res.status_code==429:
        print("too many requests - loop sleep")
        time.sleep(3*60)
        
        with open("redo_apps.csv","a",newline="",encoding='utf-8') as f2:
            writer=csv.writer(f2)
            writer.writerow([m,id])
            #f2.write(str(m))
        f2.close()
        time.sleep(10)

    elif res.status_code==403:
        print("forbidden access")
        with open("redo_apps.csv","a",newline="",encoding='utf-8') as f2:
            writer=csv.writer(f2)
            writer.writerow([m,id])
            #f2.write(str(m))
        f2.close()
        time.sleep(3*60)   
    
    

    #12 game details fields
    try:
        name=out[str(id)]["data"]["name"]
        img=out[str(id)]["data"]["header_image"]
        plat_pc=int(out[str(id)]["data"]["platforms"]["windows"]) #int 
        plat_mac=int(out[str(id)]["data"]["platforms"]["mac"]) #int
        plat_linux=int(out[str(id)]["data"]["platforms"]["linux"]) #int 
    except:
        ignore=1
        print(" tier 1 skip major")

    try: 
        genre1=out[str(id)]["data"]["genres"][0]["description"]
        relese=out[str(id)]["data"]["release_date"]["date"]
        desc=out[str(id)]["data"]["short_description"]
    except:
        genre1=relese=desc=None
        print(" tier 1 skip extras")

    try:
        price=out[str(id)]["data"]["price_overview"]['final_formatted']
    except:
        price=None
    
    try:
        free=out[str(id)]["data"]["is_free"]
        if free==True:
            free_out=1
        elif free==False:
            free_out=0
    except:
        free=None
    
    try:
        developers=out[str(id)]["data"]["developers"][0]
        publishers=out[str(id)]["data"]["publishers"][0]
        m_rate=int(out[str(id)]["data"]["metacritic"]["score"]) #int
    except:
        m_rate=plat_pc=plat_mac=plat_linux=developers=publishers=None
        print("tier 2 skipped")

    if ignore!=1:
        cur.execute("INSERT INTO game_details VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?)",(id,name,price,img,developers,publishers,plat_pc,plat_mac,plat_linux,m_rate,genre1,relese,desc,free_out))
        print("Details entered")

    try:
        process_m=out[str(id)]["data"]["pc_requirements"]['minimum']
        graphics_m=out[str(id)]["data"]["pc_requirements"]['minimum']
        storage_m=out[str(id)]["data"]["pc_requirements"]['minimum']
        ram_m=out[str(id)]["data"]["pc_requirements"]['minimum']

        cur.execute("INSERT INTO sreq_min VALUES(?,?,?,?,?)",(id,str(parse(process_m,"Processor:")),str(parse(graphics_m,"Graphics:")),str(parse(storage_m,"Storage:")),str(parse(ram_m,"Memory:"))))

    except:
        print("no min")


    # 4 specs fields

    
    
    
    try:
        process_r=out[str(id)]["data"]["pc_requirements"]['recommended']
        graphics_r=out[str(id)]["data"]["pc_requirements"]['recommended']
        storage_r=out[str(id)]["data"]["pc_requirements"]['recommended']
        ram_r=out[str(id)]["data"]["pc_requirements"]['recommended']

       
        



        cur.execute("INSERT INTO sreq_rec VALUES(?,?,?,?,?)",(id,str(parse(process_r,"Processor:")),str(parse(graphics_r,"Graphics:")),str(parse(storage_r,"Storage:")),str(parse(ram_r,"Memory:"))))


    except:
        print("no recommended")

    

    connection.commit()

    

    with open("till_scrapped.txt","w") as f1:
        f1.write(str(m+1))
    m+=1
    f1.close()
    print("loop complete")
    print("**************")
    
    






