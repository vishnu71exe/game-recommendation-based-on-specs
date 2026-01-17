import sqlite3
import csv

connection=sqlite3.connect("data6_partial.db")
cur=connection.cursor()

cur.execute("SELECT tier FROM sreq_min" )
#cur.execute("SELECT * FROM sreq_rec where process='intel core ultra' ")
#cur.execute("SELECT COUNT(appid) from game_details")
results=cur.fetchall()
print(results)