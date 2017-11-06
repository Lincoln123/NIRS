import sqlite3

con = sqlite3.connect('./Texts_db.sqlite')
cursor = con.cursor()
cursor.execute('CREATE TABLE files(gid INT, filename VARCHAR(30), newfilename VARCHAR(30), checksum VARCHAR(64),\
status VARCHAR(4))')
con.commit()

con.close()