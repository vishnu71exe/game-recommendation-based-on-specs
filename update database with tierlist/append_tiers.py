import sqlite3
import csv
import re

connection=sqlite3.connect("data6_partial.db")
cur=connection.cursor()

try:
    cur.execute("ALTER TABLE sreq_rec ADD tier INTEGER")
    connection.commit()
    print("added")
except:
    print("")
#cur.execute("SELECT * FROM game_details where appid=73010")
#cur.execute("SELECT COUNT(appid) from game_details")
cur.execute("SELECT appid,process FROM sreq_rec")
results=cur.fetchall()

m=0
count=0

def normalise(text):
    text=text.lower()
    text=text.replace("/"," ")
    text=text.replace("-"," ")
    
    
    text=text.split("@")[0]
    text = re.sub(r"[^a-z0-9 ]", " ", text)
    words=text.split()

    remove={"intel","core","amd","or","higher","greater","better","eight","equivalent","quad","embedded","ghz"}
    
    final_words=[]
    for w in words:
        if w not in remove:
            final_words.append(w)

    phrase=" ".join(final_words)

    return phrase


def append(score,id):

    if score<=100:
        print("junk values")

    if score<=1000:
        tier=1
    elif score<=5000:
        tier=2
    elif score<=11000:
        tier=3
    elif score<=35000:
        tier=4
    else:
        tier=5
    cur.execute("UPDATE sreq_rec SET tier=? where appid=?",(tier,id))
    connection.commit()
    print("data appended")


cpu={} #full data from reference sheet
with open("cpu_data_tagged.csv","r",encoding="utf-8") as f:
    reader=csv.reader(f)
    
    for lines in reader:
        #gpu.append(lines[0])
        cpu[lines[0]]=lines[1]
        count+=1

d_cpu={} # data from steam database
m=0
for appid,process in results:
    #d_cpu.append(results[m][1])
    d_cpu[process]=appid
#print(d_cpu)

count=0

baseline={"i3":2000,"i5":3000,"i7":4000,"i9":5000,"ryzen 3":2000,"ryzen 5":4000,"ryzen 7":5000,"ryzen 9":6000,"1.7 ghz":1100,"dual":700}



for i in d_cpu:
    match=False
    for j in cpu:
        if normalise(j) in normalise(i):
            match=True
            count+=1
            score=int(cpu.get(j))
            print("id=",d_cpu.get(i))
            print("d_cpu=",i)
            print("cpu=",j)
            append(score,d_cpu.get(i))
            break


    if match==False:
        for key,val in baseline.items():
            if key in normalise(i):
                count+=1
                score=int(val)
                append(score,d_cpu.get(i))
                print("alternate match")
                print("key=",key)

                break
                
            

connection.commit()

