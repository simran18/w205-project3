import sqlite3

#define connection and cursor

connection = sqlite3.connect('enemy.db')

cursor = connection.cursor()

# Create store table

command1 = """CREATE TABLE IF NOT EXISTS
enemy(enemy_id INTEGER PRIMARY KEY, name TEXT, level INTEGER)"""

cursor.execute(command1)

# Add to Stores

cursor.execute("INSERT INTO enemy VALUES (1, 'Mr. Meeseeks', 5)")
cursor.execute("INSERT INTO enemy VALUES (2, 'Dragon', 99)")
cursor.execute("INSERT INTO enemy VALUES (3, 'Private', 1)")
cursor.execute("INSERT INTO enemy VALUES (4, 'Nightwalker', 15)")
cursor.execute("INSERT INTO enemy VALUES (5, 'Elf', 7)")
cursor.execute("INSERT INTO enemy VALUES (6, 'Ronald McDonald', 36)")
cursor.execute("INSERT INTO enemy VALUES (7, 'Lex Luther', 47)")
cursor.execute("INSERT INTO enemy VALUES (8, 'Enemy Squire', 3)")
cursor.execute("INSERT INTO enemy VALUES (9, 'Sheep', 1)")