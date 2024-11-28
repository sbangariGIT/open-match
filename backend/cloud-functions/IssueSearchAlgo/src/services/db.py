from pymongo import MongoClient
import os
from dotenv import load_dotenv


class DBService:
    def __init__(self):
        self.client = MongoClient(os.environ.get("MONGODB_URI"))
        self.db =  self.client.open_match
        self.collection = self.db.issues_bot_gen
    
    def _format_db_respose(self, issue):
        try:
           return {
                "repo_name": issue.get("repo_name"),
                "repo_full_name": issue.get("repo_full_name"),
                "repo_html_url": issue.get("repo_html_url"),
                "repo_description": issue.get("repo_description"),
                "repo_stars": issue.get("repo_stars"),
                "repo_watchers": issue.get("repo_watchers"),
                "languages": issue.get("languages"),
                "repo_topics": issue.get("repo_topics"),
                "issue_html_url": issue.get("issue_html_url"),
                "issue_number": issue.get("issue_number"),
                "issue_title": issue.get("issue_title"),
                "labels": issue.get("labels"),
            }
        except Exception as e:
            return {
                "repo_name": "N/A",
                "repo_full_name": "N/A",
                "repo_html_url": "N/A",
                "repo_description": "N/A",
                "repo_stars": 0,
                "repo_watchers": 0,
                "languages": ["N/A"],
                "repo_topics": ["N/A"],
                "issue_html_url": "N/A",
                "issue_number": 0,
                "issue_title": "N/A",
                "labels": ["N/A"],
            }

    def get_issues(self):
        # Fetch all documents
        results = self.collection.find({})
        docs = []
        for doc in results:
            doc.pop('_id', None)  # Remove '_id' if it exists
            docs.append(self._format_db_respose(doc))
        return {"results": docs}

# Load environment variables
load_dotenv()
DB = DBService()
