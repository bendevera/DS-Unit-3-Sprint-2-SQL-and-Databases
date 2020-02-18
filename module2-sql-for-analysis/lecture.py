import psycopg2

conn = psycopg2.connect(
    host="rajje.db.elephantsql.com", 
    dbname="wtnyewuq", 
    user="wtnyewuq", 
    password="0QLakbkJRZqDXSnoC6OPWzpR6EVcHyqV"
)
cur = conn.cursor()

check_query = "select exists(select * from information_schema.tables where table_name='test_table')"
cur.execute(check_query)
if not cur.fetchone()[0]:
    print("Building test_table")
    query = """
    CREATE TABLE test_table (
        id        SERIAL PRIMARY KEY,
        name  varchar(40) NOT NULL,
        data    JSONB
    );
    """
    cur.execute(query)
    query = """
    INSERT INTO test_table (name, data) VALUES
    (
        'A row name',
        null
    ),
    (
        'Another row, with JSON',
        '{ "a": 1, "b": ["dog", "cat", 42], "c": true }'::JSONB
    );
    """
    cur.execute(query)

query = "SELECT * FROM test_table"
cur.execute(query)
rows = cur.fetchall()
for row in rows:
    print(row)

# commit changes and close connection
conn.commit()
cur.close()
print("Done.")

