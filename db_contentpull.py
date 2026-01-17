import sqlite3

connection=sqlite3.connect("data6.db")
cur=connection.cursor()

cur.execute("SELECT * FROM game_details where appid=22380")
#cur.execute("SELECT * FROM game_details ")
#cur.execute("SELECT COUNT(appid) from game_details")
results=cur.fetchall()
print(results)