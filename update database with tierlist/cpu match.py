import sqlite3
import csv
import re

connection=sqlite3.connect("data6_partial.db")
cur=connection.cursor()

cur.execute("SELECT * FROM sreq_min")
#cur.execute("SELECT * FROM game_details where appid=73010")
#cur.execute("SELECT COUNT(appid) from game_details")
results=cur.fetchall()

m=0
count=0

def normalise(text):
    text=text.lower()
    text=text.replace("/"," ")
    text=text.replace("-"," ")
    
    
    before=text.split("@")
    text = re.sub(r"[^a-z0-9 ]", " ", text)
    words=before[0].split()

    remove={"intel","core","amd","or","higher","greater","better"}
    
    final_words=[]
    for w in words:
        if w not in remove:
            final_words.append(w)

    phrase=" ".join(final_words)

    return phrase


cpu={} #full data from reference sheet
with open("cpu_data_tagged.csv","r",encoding="utf-8") as f:
    reader=csv.reader(f)
    
    for lines in reader:
        #gpu.append(lines[0])
        cpu[lines[0]]=lines[1]
        count+=1

d_cpu=[] # data from steam database
m=0
for row in results:
    d_cpu.append(results[m][1])
    m+=1

#print(d_cpu)

count=0

baseline={"i3":2000,"i5":3000,"i7":4000,"i9":5000,"ryzen 3":2000,"ryzen 5":4000,"ryzen 7":5000,"ryzen 9":6000}



for i in d_cpu:
    match=False
    for j in cpu:
        if normalise(j) in normalise(i):
            match=True
            count+=1
            print("d_cpu=",i)
            print("cpu=",j)
            print("score=",cpu.get(j))

    if match==False:
        for key,val in baseline.items():
            if key in normalise(i):
                count+=1
                print("d_cpu=",i)
                print("cpu=",key)
                print("score=",val)
                print("alternate match")

print(count)
