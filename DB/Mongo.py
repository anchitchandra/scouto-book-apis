from pymongo import MongoClient
import string
import random

class MongoAPI:
    def __init__(self, collection):
        
        self.client  = MongoClient("mongodb+srv://{user}:{password}@scouto.fq6vieu.mongodb.net/?retryWrites=true&w=majority")
        self.db = self.client.test
        database = "books"
        cursor = self.client[database]
        self.collection = cursor[collection]

    def findall(self, filter):
        datax = self.collection.find(filter)
        dataA = []
        for x in datax:
            dataA.append(x)
        return dataA
    
    # def createDummy(self):
    #     data = []
        
    #     for i in range(1, 11):
    #         name  = ''.join(random.choices(string.ascii_lowercase +
    #                          string.digits, k=5))
    #         category = ''.join(random.choices(string.ascii_lowercase +
    #                             string.digits, k=3))
    #         rent = random.randint(111, 999)
    #         x = {"_id":i, "name": name, "category": category, "rent": rent}
    #         data.append(x)

    #     self.collection.insert_many(data)
    #     return "ok"

    def insertTransaction(self, data):
        res = self.collection.insert_one(data)
        if res:
            return True
        return False

    def updateTransaction(self, filter, data):
        
        res = self.collection.update_one(filter, data)
        if res:
            return True
        return False
