import os
from dotenv import load_dotenv
from pymongo import MongoClient
from openai import OpenAI
import requests


class MongoDBHandler:
    def __init__(self):
        # Load environment variables from .env file
        load_dotenv()
        MONGO_DB_URI = os.getenv("MONGO_DB_URI")
        OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
        self.client = MongoClient(MONGO_DB_URI)
        self.openai_client = OpenAI(api_key=OPENAI_API_KEY)
        self.db = self.client.open_match
        self.collection = self.db.issues_new
        self.collection_2 = self.db.repo

    def get_document(self, collection_name: str, document_id: str):
        """
        Fetches a document from the MongoDB collection.
        :param collection_name: Name of the collection to fetch the document from.
        :param document_id: ID of the document to fetch.
        :return: The document data if found, otherwise None.
        """
        collection = self.db[collection_name]
        document = collection.find_one({"uuid": document_id})
        return document

    def update_document(self, collection_name: str, document_id: str, data: dict):
        """
        Updates a document in the MongoDB collection.
        :param collection_name: Name of the collection to update the document in.
        :param document_id: ID of the document to update.
        :param data: Dictionary containing the data to update.
        :return: The result of the update operation.
        """
        collection = self.db[collection_name]
        result = collection.update_one({"uuid": document_id}, {"$set": data})
        return result

    def add_repo(self, repo: str):
        """
        Adds a new repo to the MongoDB collection.
        :param repo: Name of the repo in the format OWNER/REPONAME.
        """
        def get_languages(lang_url, github_token):
            """
            Fetch languages used in the particular Repo

            Args:
            lang_url (str): Github repo languages API URL

            Returns:
            list: A list of all the languages used in the repo
            """

            headers = {
                "Authorization": f"token {github_token}",
                "Accept": "application/vnd.github.v3+json"
            }

            response = requests.get(lang_url, headers=headers)
            if response.status_code == 200:
                languages_data = response.json()
                languages = []
                for lang in languages_data.keys():
                    languages.append(lang)
                return languages
            else:
                print(f"Failed to fetch repo languages: {response.status_code}")
                return []
        def fetch_repo_details(repo, github_token):
            """
            Fetches information about for a given GitHub repository.

            Args:
            repo (str): The repository in "owner/repo" format (e.g., "microsoft/vscode").
            github_token (str): GitHub token for authentication.

            Returns:
            dict: Repo object with details like owner, urls, license, topics.
            """
            headers = {
                "Authorization": f"token {github_token}",
                "Accept": "application/vnd.github.v3+json",
            }
            response = requests.get("https://api.github.com/repos/{repo_name}".format(repo_name=repo), headers=headers)
            if response.status_code == 200:
                repo_data = response.json()
                repo_data["languages"] = get_languages(repo_data["languages_url"], github_token=github_token)
                return repo_data
            return {}
        repo_details = fetch_repo_details(repo, os.getenv("GITHUB_TOKEN"))
        self.collection_2.insert_one(repo_details)

mongoDBHandler = MongoDBHandler()