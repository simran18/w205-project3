import sqlite3

#define connection and cursor

connection = sqlite3.connect('guild.db')

cursor = connection.cursor()

# Create store table

command1 = """CREATE TABLE IF NOT EXISTS
guild(guild_id INTEGER PRIMARY KEY, name TEXT)"""

cursor.execute(command1)

# Add to Stores

cursor.execute("INSERT INTO guild VALUES (1, 'Fighters Guild')")
cursor.execute("INSERT INTO guild VALUES (2, 'Mages Guild')")
cursor.execute("INSERT INTO guild VALUES (3, 'Thieves Guild')")
cursor.execute("INSERT INTO guild VALUES (4, 'Data Wranglers Guild')")
cursor.execute("INSERT INTO guild VALUES (5, 'Traders Guild')")
cursor.execute("INSERT INTO guild VALUES (6, 'Assassins Guild')")
cursor.execute("INSERT INTO guild VALUES (7, 'Knights Templar')")

connection.commit()

# See Results for debug only
#cursor.execute("SELECT * FROM inventory")

#results = cursor.fetchall()
#print(results)

connection.close()