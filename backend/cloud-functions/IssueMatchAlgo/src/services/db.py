from pymongo import MongoClient
import os
import random


class DBService:
    def __init__(self):
        self.client = MongoClient(os.environ.get("MONGODB_URI"))
        self.db =  self.client.open_match
        self.collection = self.db.issues
    
    def _format_db_respose(self, issue):
        #TODO: This is bad practice, I need to make a model for this instead of passing along dicts, doing this cause of the time crunch
        try:
           return {
                "title": issue.get("issue_title"),
                "repoName": issue.get("repo_name"),
                "issueNumber": str(issue.get("issue_number")), #TODO: change frontend to take number
                "issueLink": issue.get("issue_html_url"),
                "description": issue.get("summary"),
                "tags": [] + issue.get("repo_topics") + issue.get("repo_languages"),
                "match": random.randint(60, 90) #TODO: Need to dynamically determine the match, for now let me mock it
            }
        except Exception as e:
            return {
                "title": "N/A",
                "repoName": "N/A",
                "issueNumber": "0",
                "issueLink": "N/A",
                "description": "N/A",
                "tags": [],
                "match": random.randint(60, 90) # Need to dynamically determine the match, for now let me mock it
            }

    def get_k_nearest_issues(self, embedding : list[float], k=4):
        results = self.collection.aggregate([
        {"$vectorSearch": {
            "queryVector": embedding,
            "path": "embedding",
            "numCandidates": 100,
            "limit": k,
            "index": "issuesKnnIndex",
            }}
        ])
        docs = []
        for doc in results:
            del doc['embedding']
            del doc['_id']
            docs.append(self._format_db_respose(doc))
        return {"results": docs}

DB = DBService()
