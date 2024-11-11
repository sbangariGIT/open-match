from pymongo import MongoClient
import os
import random


class DBService:
    def __init__(self):
        self.client = MongoClient(os.environ.get("MONGODB_URI"))
        self.db =  self.client.open-match # type: ignore
        self.collection = self.db.issues
        self.index = "issuesSemanticSearch"

    def get_k_nearest_issues(self, embedding : list[float], k=4):
        results = self.collection.aggregate([
        {"$vectorSearch": {
            "queryVector": embedding,
            "path": "embedding",
            "numCandidates": 100,
            "limit": k,
            "index": "self.index",
            }}
        ])
        docs = []
        for doc in results:
            del doc['embedding']
            doc['match'] = random.randint(60, 90) # Need to dynamically determine the match, for now let me mock it
            docs.append(doc['name'])
        return {"results": docs}, 200

DB = DBService()
