import pandas as pd 
import psycopg2
import os
from dotenv import load_dotenv
load_dotenv()

# read in our data
df = pd.read_csv('./titanic.csv')
print(f"DF shape: {df.shape}")

# create connection to db we want to move the data to
conn = psycopg2.connect(
    host=os.getenv('DB_HOST'), 
    dbname=os.getenv('DB_USER'), 
    user=os.getenv('DB_USER'), 
    password=os.getenv('DB_PASSWORD')
)
cur = conn.cursor()

# ensure the table is fresh by dropping if exists and creating from scratch
query = "select exists(select * from information_schema.tables where table_name='titantic')"
cur.execute(query)

if cur.fetchone()[0]:
    print("dropping table...")
    query = "DROP TABLE titantic;"
    cur.execute(query)

print("creating table...")
query = """
CREATE TABLE titantic (
    id  SERIAL PRIMARY KEY,
    survived BOOLEAN,
    class TEXT,
    name TEXT,
    sex TEXT,
    age INTEGER,
    siblings BOOLEAN,
    parents BOOLEAN,
    fare REAL
)
"""
cur.execute(query)

def get_name(name):
    return name.replace("'", "")

def get_row(row):
    return (bool(row[0]), row[1], get_name(row[2]), row[3], row[4], bool(row[5]), bool(row[6]), row[7])

# for each row in the csv, add a row to the postgres db
print("adding rows...")
for row in df.values:
    query = "INSERT INTO titantic (survived, class, name, sex, age, siblings, parents, fare) VALUES " + str(get_row(row)) + ";"
    cur.execute(query)

query = "SELECT * FROM titantic"
cur.execute(query)
rows = cur.fetchall()
print(f"Num rows: {len(rows)}")
conn.commit()
cur.close()