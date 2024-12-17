import os
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()
MONGO_DB_URI = os.getenv("MONGO_DB_URI")
client = MongoClient(MONGO_DB_URI)
db = client.open_match
repo_source_code_collection = db.repo_source_code
repo_source_code_collection.create_index("repo_name")