import sqlite3
import csv
import re

def normalise(text):
    text=text.lower()
    text=text.replace("/"," ")
    text=text.replace("-"," ")
    text=re.sub(r"[^a-z0-9 ]", " ", text) #removes symbols

    words=text.split()
    fixed_words=[]
    for w in words:
        parts = re.findall(r"[a-z]+|\d+", w) #splits merged words and numbers
        for p in parts:
            fixed_words.append(p)
    
    remove = {
        "nvidia", "amd", "geforce", "graphics", "graphic",
        "equivalent", "or", "greater", "than",
        "minimum", "recommended", "series",
        "video", "card", "gpu", "with", "and"
    }

    final_words=[]
    for w in fixed_words:
        if w not in remove:
            final_words.append(w)

    phrase=" ".join(final_words)

    return phrase


connection=sqlite3.connect("data6_partial.db")
cur=connection.cursor()

cur.execute("SELECT * FROM sreq_min")
#cur.execute("SELECT * FROM game_details where appid=73010")
#cur.execute("SELECT COUNT(appid) from game_details")
results=cur.fetchall()

m=0
count=0


'''
gpu={} #full data from reference sheet
with open("data/gpu_data.csv","r",encoding="utf-8") as f:
    reader=csv.reader(f)
    
    for lines in reader:
        #gpu.append(lines[0])
        gpu[lines[0]]=int(lines[1])
        count+=1
#print(gpu)

d_gpu=[] # data from steam database
m=0
for row in results:
    d_gpu.append(results[m][2])
    m+=1


#print(d_gpu)
count=0

for i in d_gpu:
    for j in gpu:
        if normalise(j) in normalise(i):
            count+=1
            print("d_gpu=",i)
            print("gpu=",j)
            print("score=",gpu.get(j))
print(count)
'''