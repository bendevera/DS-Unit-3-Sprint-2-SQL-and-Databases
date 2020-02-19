import psycopg2
import pymongo
import dotenv
import os
dotenv.load_dotenv()

# postgres connection/cursor
pg_conn = psycopg2.connect(
    dbname=os.getenv("DB_USER"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    host=os.getenv("DB_HOST")
)
pg_curs = pg_conn.cursor()
print("Connected to postgres.")

# mongo connection
client = pymongo.MongoClient(
    "mongodb://bendevera:{}@test-cluster-shard-00-00-v2cof.mongodb.net:27017,test-cluster-shard-00-01-v2cof.mongodb.net:27017,test-cluster-shard-00-02-v2cof.mongodb.net:27017/test?ssl=true&replicaSet=test-cluster-shard-0&authSource=admin&retryWrites=true&w=majority".format(os.getenv("MONGO_PASSWORD")))
db = client.test
print("Connected to mongo.")

get_query = "SELECT * FROM charactercreator_character;"
pg_curs.execute(get_query)
characters = pg_curs.fetchall()
print("Grabbed characters from postgres.")


def prep_data(data):
    return {
        "character_id": data[0],
        "name": data[1],
        "level": data[2],
        "exp": data[3],
        "hp": data[4],
        "strength": data[5],
        "intelligence": data[6],
        "dexterity": data[7],
        "wisdom": data[8]
    }


print("Adding charcters to mongo.")
for character in characters:
    db.test.insert_one(prep_data(character))

# sanity check
print("Sanity check | search for docs with name 'Rem minima': ")
print(list(db.test.find({"name": "Rem minima"})))
# close cursor to postgres
pg_curs.close()
