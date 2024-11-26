import os
from dotenv import load_dotenv
from pymongo import MongoClient
import requests


class MongoDBHandler:
    def __init__(self):
        # Load environment variables from .env file
        load_dotenv()
        MONGO_DB_URI = os.getenv("MONGO_DB_URI")
        self.client = MongoClient(MONGO_DB_URI)
        self.db = self.client.open_match
        self.collection = self.db.issues_bot_gen
        self.collection_2 = self.db.repo

    def get_languages(self, lang_url, github_token):
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
    
    def fetch_repo_details(self, repo, github_token):
        """
        Fetches information about for a given GitHub repository.

        Args:
        repo (str): The repository in "owner/repo" format (e.g., "microsoft/vscode").
        github_token (str): GitHub token for authentication.

        Returns:
        dict: Repo object with details like owner, urls, license, topics.
        """
        try: 
            headers = {
                "Authorization": f"token {github_token}",
                "Accept": "application/vnd.github.v3+json",
            }
            response = requests.get("https://api.github.com/repos/{repo_name}".format(repo_name=repo), headers=headers)
            if response.status_code == 200:
                repo_data = response.json()
                repo_data["languages"] = self.get_languages(repo_data.get("languages_url"), github_token=github_token)
                return repo_data
            return {}
        except Exception as e:
            print("there was an error in fetch_repo_details")
            return {}
    
    def fetch_issue_details(self, repo, issue, github_token):
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
        response = requests.get(f"https://api.github.com/repos/{repo}/issues/{issue}", headers=headers)
        if response.status_code == 200:
            issues_data = response.json()
            if not issues_data:  # Break if no more issues are returned
                return {}
            issue = {
                    "issue_number": issue.get("number"),
                    "issue_title": issue.get("title"),
                    "labels": [label.get("name") for label in issue.get("labels")],
                    "issue_html_url": issue.get("html_url"),
                }
            return issue
        return {}
    
    def build_issue_object(self, repo, issue):

        issue_obj = {
            "repo_name": repo.get("name"),
            "repo_full_name": repo.get("full_name"),
            "repo_html_url": repo.get("html_url"),
            "repo_description": repo.get("description"),
            "repo_stars": repo.get("stargazers_count"),
            "repo_watchers": repo.get("watchers_count"),
            "languages": repo.get("languages"),
            "repo_topics": repo.get("topics"),
            "issue_html_url": issue.get("html_url"),
            "issue_number": issue.get("number"),
            "issue_title": issue.get("title"),
            "labels":  [label.get("name") for label in issue.get("labels")],
        }
        return issue_obj

    def add_repo(self, repo: str):
        """
        Adds a new repo to the MongoDB collection.
        :param repo: Name of the repo in the format OWNER/REPONAME.
        """
        repo_details = self.fetch_repo_details(repo, os.getenv("GITHUB_TOKEN"))
        self.collection_2.insert_one(repo_details)

    def add_issue(self, repo, issue):
        """
        Adds a new repo to the MongoDB collection.
        :param repo: Name of the repo in the format OWNER/REPONAME.
        """
        try:
            repo_details = self.fetch_repo_details(repo, os.getenv("GITHUB_TOKEN"))
            # issue_details = self.fetch_issue_details(repo, issue, os.getenv("GITHUB_TOKEN"))
            issue_obj = self.build_issue_object(repo_details, issue)
            print(issue_obj)
            self.collection.insert_one(issue_obj)
        except Exception as e:
            print("There was an error in adding an issue")
            print(str(e))


mongoDBHandler = MongoDBHandler()