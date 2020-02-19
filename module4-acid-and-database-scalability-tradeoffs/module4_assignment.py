import psycopg2
import os
from dotenv import load_dotenv
load_dotenv()

conn = psycopg2.connect(
    dbname=os.getenv("DB_USER"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    host=os.getenv("DB_HOST")
)

curs = conn.cursor()


def execute_query(cursor, query, result_count="many"):
    cursor.execute(query)
    if result_count == "many":
        return cursor.fetchall()
    return cursor.fetchone()


print("1. How many passengers survived, and how many died?")

survived_count = """
SELECT COUNT(*) 
FROM titantic 
WHERE survived = TRUE;
"""
survived_count = execute_query(curs, survived_count, "one")[0]
print(f"Survived: {survived_count}")

not_survived_count = """
SELECT COUNT(*)
FROM titantic
WHERE survived = FALSE;
"""
not_survived_count = execute_query(curs, not_survived_count, "one")[0]
print(f"Not Survived: {not_survived_count} \n")

print("2. How many passengers were in each class?")

num_per_class = """
SELECT class, COUNT(*)
FROM titantic
GROUP BY class
ORDER BY class;
"""
for elem in execute_query(curs, num_per_class):
    print(f"{elem[0]} #: {elem[1]} \n")

print("3. How many passengers survived/died within each class?")
num_alive_per_class = """
SELECT class, COUNT(*)
FROM titantic
WHERE survived = TRUE
GROUP BY class
ORDER BY class;
"""
print("ALIVE: ")
for elem in execute_query(curs, num_alive_per_class):
    print(f"{elem[0]} #: {elem[1]} \n")

num_dead_per_class = """
SELECT class, COUNT(*)
FROM titantic
WHERE survived = FALSE
GROUP BY class
ORDER BY class;
"""
print("DEAD: ")
for elem in execute_query(curs, num_dead_per_class):
    print(f"{elem[0]} #: {elem[1]} \n")

print("4. What was the average age of survivors vs nonsurvivors?")
average_age = """
SELECT AVG(age)
FROM titantic
WHERE survived = TRUE;
"""
average_age = round(execute_query(curs, average_age, "one")[0], 2)
print(f"Average age of survivors: {average_age}")

average_age = """
SELECT AVG(age)
FROM titantic
WHERE survived = FALSE;
"""
average_age = round(execute_query(curs, average_age, "one")[0], 2)
print(f"Average age of nonsurvivors: {average_age} \n")

print("5. What was the average fare by passenger class?")

average_fare_by_class = """
SELECT class, AVG(fare)
FROM titantic
GROUP BY class
ORDER BY class;
"""
for elem in execute_query(curs, average_fare_by_class):
    print(f"{elem[0]}: ${elem[1]} \n")

curs.close()
