import sqlite3

conn = sqlite3.connect('CrawlData.db')
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE CRAWL1 
(NAME CHAR(32), TITLE CHAR(32), HTML CHAR(128), PRIMARY KEY) 
""")
cursor.execute("""
INSERT INTO PHONEBOOK (NAME, PHONE, EMAIL) 
VALUES(?, ?, ?)
""", ('김범수', '021-445-2424', 'visual@bskim.com'))

id = cursor.lastrowid
print(id)

conn.commit()

cursor.close()
conn.close()