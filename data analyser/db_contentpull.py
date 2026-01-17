import sqlite3

connection=sqlite3.connect("test_data.db")
cur=connection.cursor()

cur.execute("SELECT * FROM sreq_rec where appid=292030")
#cur.execute("SELECT * FROM game_details ")
#cur.execute("SELECT COUNT(appid) from game_details")
results=cur.fetchall()
print(results)