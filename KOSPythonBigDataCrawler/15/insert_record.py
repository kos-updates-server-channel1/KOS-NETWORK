import sqlite3

conn = sqlite3.connect('test.db')
cursor = conn.cursor()

cursor.execute("""
INSERT INTO PHONEBOOK (NAME, PHONE, EMAIL) 
VALUES(?, ?, ?)
""", ('박신혜', '021-322-1542', 'shinhye@park.com'))

id = cursor.lastrowid
print(id)

cursor.execute("""
INSERT INTO PHONEBOOK (NAME, PHONE, EMAIL) 
VALUES(?, ?, ?)
""", ('김범수', '021-445-2424', 'visual@bskim.com'))

id = cursor.lastrowid
print(id)

conn.commit()

cursor.close()
conn.close()