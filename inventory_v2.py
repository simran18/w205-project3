import sqlite3

#define connection and cursor

connection = sqlite3.connect('store_transactions.db')

cursor = connection.cursor()

# Create store table

command1 = """CREATE TABLE IF NOT EXISTS
stores(store_id INTEGER PRIMARY KEY, location TEXT)"""

cursor.execute(command1)

# Create Purchase Table

command2 = """CREATE TABLE IF NOT EXISTS
inventory(inventory_id INTEGER PRIMARY KEY, category STRING, item_name STRING, store_id INTEGER, total_cost FLOAT, on_hand_qty INTEGER, event_type TEXT,
FOREIGN KEY(store_id) REFERENCES stores(store_id))"""

cursor.execute(command2)

# Add to Stores

cursor.execute("INSERT INTO stores VALUES (1, 'Jita')")
cursor.execute("INSERT INTO stores VALUES (2, 'Amarr')")
cursor.execute("INSERT INTO stores VALUES (3, 'Dodixie')")
cursor.execute("INSERT INTO stores VALUES (4, 'Rens')")
cursor.execute("INSERT INTO stores VALUES (5, 'Hek')")

# Add Inventory

cursor.execute("INSERT INTO inventory VALUES (1001, 'Sword', 'Master Sword', 1, 1000.00, 7, 'transaction')")
cursor.execute("INSERT INTO inventory VALUES (1002, 'Sword', 'Master Sword', 2, 1000.00, 7, 'transaction')")
cursor.execute("INSERT INTO inventory VALUES (1003, 'Sword', 'Master Sword', 3, 1000.00, 7, 'transaction')")
cursor.execute("INSERT INTO inventory VALUES (1004, 'Sword', 'Master Sword', 4, 1000.00, 7, 'transaction')")
cursor.execute("INSERT INTO inventory VALUES (1005, 'Sword', 'Master Sword', 5, 1000.00, 7, 'transaction')")
cursor.execute("INSERT INTO inventory VALUES (1006, 'Bow', 'Sacred Bow', 1, 1500.00, 7, 'transaction')")
cursor.execute("INSERT INTO inventory VALUES (1007, 'Bow', 'Sacred Bow', 2, 1500.00, 7, 'transaction')")
cursor.execute("INSERT INTO inventory VALUES (1008, 'Bow', 'Sacred Bow', 3, 1500.00, 7, 'transaction')")
cursor.execute("INSERT INTO inventory VALUES (1009, 'Bow', 'Sacred Bow', 4, 1500.00, 7, 'transaction')")
cursor.execute("INSERT INTO inventory VALUES (1010, 'Bow', 'Sacred Bow', 5, 1500.00, 7, 'transaction')")
cursor.execute("INSERT INTO inventory VALUES (1011, 'Armor', 'Plate Armor', 1, 500.00, 7, 'transaction')")
cursor.execute("INSERT INTO inventory VALUES (1012, 'Armor', 'Plate Armor', 2, 500.00, 7, 'transaction')")
cursor.execute("INSERT INTO inventory VALUES (1013, 'Armor', 'Plate Armor', 3, 500.00, 7, 'transaction')")
cursor.execute("INSERT INTO inventory VALUES (1014, 'Armor', 'Plate Armor', 4, 500.00, 7, 'transaction')")
cursor.execute("INSERT INTO inventory VALUES (1015, 'Armor', 'Plate Armor', 5, 500.00, 7, 'transaction')")

connection.commit()

# See Results
cursor.execute("SELECT * FROM inventory")

results = cursor.fetchall()
print(results)

connection.close()