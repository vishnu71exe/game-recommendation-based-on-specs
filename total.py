#Total games in file check 

import json
import os
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
except IndexError:
    print("finished")

