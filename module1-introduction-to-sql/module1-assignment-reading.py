import sqlite3

# connect to db
conn = sqlite3.connect("rpg_db.sqlite3")
# create cursor from connection
curs = conn.cursor()
print("1. How many total Characters are there?")
query = "SELECT * FROM charactercreator_character;"
characters = curs.execute(query).fetchall()
print(f"# Characters: {len(characters)} \n")

print("2. How many of each specific subclass?")
type_queries = [
    ("mage", "SELECT * FROM charactercreator_mage;"),
    ("thief", "SELECT * FROM charactercreator_thief;"),
    ("cleric", "SELECT * FROM charactercreator_cleric"),
    ("fighter","SELECT * FROM charactercreator_fighter;")
]

for query in type_queries:
    characters = curs.execute(query[1]).fetchall()
    print(f"# {query[0]} Characters: {len(characters)} \n")


print("3. How many total Items?")
query = "SELECT * FROM armory_item;"
items = curs.execute(query).fetchall()
print(f"# Items: {len(items)} \n")

print("4. How many of the Items are weapons? How many are not?")
query = "SELECT item_ptr_id FROM armory_weapon;"
weapons = curs.execute(query).fetchall()
print(f"# Weapon Items: {len(weapons)} # Non Weapon Items: {len(items)-len(weapons)} \n")

print("5. How many Items does each character have? (Return first 20 rows)")
query = """SELECT cc.name, ai.name
FROM charactercreator_character as cc, 
charactercreator_character_inventory as ci,
armory_item as ai
WHERE cc.character_id = ci.character_id 
AND ci.item_id = ai.item_id;"""
rows = curs.execute(query).fetchall()
for i in range(20):
    print(rows[i])
print()

print("6. How many Weapons does each character have? (Return first 20 rows)")
# weapon_ids = [item[0] for item in weapons]
query = """
SELECT cc.name, COUNT(ci.item_id)
FROM charactercreator_character as cc, 
charactercreator_character_inventory as ci,
armory_item as ai
WHERE cc.character_id = ci.character_id 
AND ci.item_id = ai.item_id
AND ai.item_id IN (SELECT item_ptr_id FROM armory_weapon)
GROUP BY cc.character_id;
"""
rows = curs.execute(query).fetchall()
for i in range(20):
    print(rows[i])
print()

print("7. On average, how many Items does each Character have?")
query = """
SELECT * 
FROM charactercreator_character_inventory;
"""
item_list = curs.execute(query).fetchall()
print(f"{len(item_list)/len(characters)} \n")

print("8. On average, how many Weapons does each character have?")
query = """
SELECT * 
FROM charactercreator_character_inventory
WHERE item_id IN (SELECT item_ptr_id FROM armory_weapon);
"""
weapon_list = curs.execute(query).fetchall()
print(f"{len(weapon_list)/len(characters)} \n")

curs.close()
