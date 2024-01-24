from bson import ObjectId
from pymongo import MongoClient


class CoolConfig:
    def __init__(self, username, password, bdd):
        self.username = username
        self.password = password
        self.bdd = bdd
        self.url = (f"mongodb+srv://{self.username}:{self.password}@cloud.mzoqfws.mongodb.net/?retryWrites=true&w"
                    f"=majority")
        self.collection = "user"
        self.object_id = ""

    def connect_mongo(self):
        client = MongoClient(self.url)
        if client.server_info():
            db = client[self.bdd]
            collection = db["user"]
            return collection, db

    def insert_data(self, data: dict):
        collection, db = self.connect_mongo()
        result = collection.insert_one(data)
        return result.inserted_id

    def get_element(self, object_id):
        collection, db = self.connect_mongo()
        result = collection.find_one({"_id": ObjectId(object_id)})
        return result

    def delete_element(self):
        collection, db = self.connect_mongo()
        collection.delete_many({})
