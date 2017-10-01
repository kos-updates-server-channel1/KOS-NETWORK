import sqlite3
conn = sqlite3.connect('minutediary.db')
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE DIARY (
DIARY_ID INTEGER PRIMARY KEY AUTOINCREMENT, 
CREATEDATE DATETIME, 
NOTE CHAR(140))
""")

cursor.execute("""
CREATE TABLE DIARY_IMG (
IMG_ID INTEGER PRIMARY KEY AUTOINCREMENT, 
IMG BLOB, 
DIARY_ID INTEGER, 
FOREIGN KEY(DIARY_ID) REFERENCES DIARY(DIARY_ID))
""")

cursor.execute("SELECT name FROM sqlite_master")
for row in cursor:
   print ("TABLE = ", row[0])
   
cursor.close()
conn.close()