import psycopg2
import sqlite3
import os
from dotenv import load_dotenv
load_dotenv()

'''
Purpose:
this script moves the RPG database from a SQLite file into a Cloud Postgres
Database. ETL pipeline to productionize a SQLite file.
'''

conn = psycopg2.connect(
    host=os.getenv('DB_HOST'), 
    dbname=os.getenv('DB_USER'), 
    user=os.getenv('DB_USER'), 
    password=os.getenv('DB_PASSWORD')
)
cur = conn.cursor()

sql_path = "/Users/bendevera/Desktop/development/data_science/DS-Unit-3-Sprint-2-SQL-and-Databases/module1-introduction-to-sql/rpg_db.sqlite3"
lite_conn = sqlite3.connect(sql_path)
lite_cur = lite_conn.cursor()

print("Made connections...")

# santiy check part 1
sanity_query = "SELECT COUNT(*) FROM charactercreator_character;"
print(f"# Characters in Postgres: {lite_cur.execute(sanity_query).fetchone()[0]}")

# lite_cur.execute("PRAGMA table_info(charactercreator_character);").fetchalll()
# drop table to start from new
drop_character = "DROP TABLE charactercreator_character;"
cur.execute(drop_character)
conn.commit()
# create character table
create_character = """
CREATE TABLE charactercreator_character (
    character_id SERIAL PRIMARY KEY,
    name VARCHAR(30),
    level INT,
    exp INT,
    hp INT,
    strength INT,
    intelligence INT,
    dexterity INT,
    wisdom INT
);
"""
cur.execute(create_character)
conn.commit()

print("Created table...")

get_characters = "SELECT * FROM charactercreator_character;"
insert_character = """
INSERT INTO charactercreator_character
(name, level, exp, hp, strength, intelligence, dexterity, wisdom)
VALUES
"""
# get characters from sqlite
rows = lite_cur.execute(get_characters).fetchall()
print("Adding characters to postgres db...")
for row in rows:
    # add each row to postgres
    cur_query = insert_character + str(row[1:]) + ";"
    cur.execute(cur_query)

conn.commit()

# sanity check part 2
cur.execute(sanity_query)
print(f"# Characters in Postgres: {cur.fetchone()[0]}")
cur.close()
lite_cur.close()

print("Done.")