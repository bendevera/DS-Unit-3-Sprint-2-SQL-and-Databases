import sqlite3


# open connection / also creates file if it doesn't exist
conn = sqlite3.connect('toy_data.db')

# query to create toy table
query = "CREATE TABLE IF NOT EXISTS toy (name varchar(30), size int);"

# create cursor from connection
curs = conn.cursor()

# execute query using cursor
curs.execute(query)

# close cursor
curs.close()

# commit changes
conn.commit()

# create new cursor
curs2 = conn.cursor()

# insert record/isntance into toy database
insert_query = "INSERT INTO toy (name, size) VALUES ('awesome', 27);"
curs2.execute(insert_query)
curs2.close()
conn.commit()

# select all rows from toy table
curs3 = conn.cursor()
print(curs3.execute("SELECT * FROM toy;").fetchall())
