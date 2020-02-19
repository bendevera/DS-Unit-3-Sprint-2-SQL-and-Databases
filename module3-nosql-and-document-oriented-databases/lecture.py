import pymongo
import os
import dotenv
import random
dotenv.load_dotenv()


client = pymongo.MongoClient(
    "mongodb://bendevera:{}@test-cluster-shard-00-00-v2cof.mongodb.net:27017,test-cluster-shard-00-01-v2cof.mongodb.net:27017,test-cluster-shard-00-02-v2cof.mongodb.net:27017/test?ssl=true&replicaSet=test-cluster-shard-0&authSource=admin&retryWrites=true&w=majority".format(os.getenv("MONGO_PASSWORD")))
db = client.test

data = []

for i in range(20):
    value = random.randint(1, 20)
    element = {
        "value": value,
        "even": value % 2 == 0
    }
    data.append(element)

db.test.insert_many(data)

# insert one element and find it
# db.test.insert_one(element)

# print(db.test.count_documents(element))

# find all docs with value key equal to 2
print(list(db.test.find({"value": 2})))

# MONGO DB IS CRUD
# CREATE db.<collection>.insert_one 
# READ db.<collection>.find
# UPDATE db.<collection>.update_one
# DELETE db.<collection>.delete_one
# all _one can be replaced by _many