import sqlite3 
import pandas as pd 

# create connection to db
conn = sqlite3.connect("buddymove_holidayiq.sqlite3")
# create cursor from connection
curs = conn.cursor()

# run check query to see if table exists
check_query = "SELECT name FROM sqlite_master WHERE type='table' AND name='reviews';"
if not curs.execute(check_query).fetchone():
    print("table not found so making from csv.")
    # create df from csv
    df = pd.read_csv("buddymove_holidayiq.csv")
    # converts df to sql table and names it reviews
    df.to_sql("reviews", conn)

query = """
SELECT * 
FROM reviews;
"""
rows = curs.execute(query).fetchall()
print(f"# rows: {len(rows)} \n")

query = """
SELECT * 
FROM reviews
WHERE Nature > 100 AND Shopping > 100;
"""
rows = curs.execute(query).fetchall()
print(f"# rows with large vals: {len(rows)} \n")

query = """
SELECT AVG(Sports), 
AVG(Religious), 
AVG(Nature),
AVG(Theatre), 
AVG(Shopping), 
AVG(Picnic)
FROM reviews;
"""
averages = curs.execute(query).fetchall()
print(averages, "\n")

curs.close()
print("done.")