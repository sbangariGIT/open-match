import os
from ..logging.logger import central_logger
import requests
from dotenv import load_dotenv
from pymongo import MongoClient
from .githubHandler import github_handler



class GitHubHandler:
    def __init__(self, github_token):
        """
        Handles GitHub API interactions.

        Args:
        github_token (str): Personal access token for GitHub API authentication.
        """
        self.github_token = github_token
        self.headers = {
            "Authorization": f"token {github_token}",
            "Accept": "application/vnd.github.v3+json",
        }

    def fetch_repo_details(self, repo):
        """
        Fetches details of a GitHub repository.

        Args:
        repo (str): Repository in "owner/repo" format.

        Returns:
        dict: Repository details including name, description, and topics.
        """
        url = f"https://api.github.com/repos/{repo}"
        try:
            response = requests.get(url, headers=self.headers)
            if response.status_code == 200:
                repo_data = response.json()
                repo_data["languages"] = self.fetch_repo_languages(repo_data.get("languages_url"))
                return repo_data
            else:
                central_logger.warning(f"Failed to fetch repo details ({repo}): {response.status_code}")
                return {}
        except requests.RequestException as e:
            central_logger.warning(f"Error fetching repo details ({repo}): {e}")
            return {}

    def fetch_repo_languages(self, lang_url):
        """
        Fetches programming languages used in a repository.

        Args:
        lang_url (str): URL for fetching repository languages.

        Returns:
        list: List of programming languages.
        """
        try:
            response = requests.get(lang_url, headers=self.headers)
            if response.status_code == 200:
                return list(response.json().keys())
            else:
                central_logger.warning(f"Failed to fetch repo languages: {response.status_code}")
                return []
        except requests.RequestException as e:
            central_logger.warning(f"Error fetching repo languages: {e}")
            return []


class MongoDBHandler:
    def __init__(self, db_uri, github_handler):
        """
        Handles MongoDB interactions.

        Args:
        db_uri (str): MongoDB connection URI.
        github_handler (GitHubHandler): Instance of GitHubHandler for API interactions.
        """
        client = MongoClient(db_uri)
        self.db = client.open_match
        self.issues_collection = self.db.issues_bot_gen
        self.repo_collection = self.db.repo
        self.github_handler = github_handler

    def build_issue_object(self, repo, issue):
        """
        Builds a structured issue object for MongoDB.

        Args:
        repo (dict): Repository details.
        issue (dict): Issue details.

        Returns:
        dict: Structured issue object.
        """
        return {
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
            "labels": [label.get("name") for label in issue.get("labels", [])],
        }

    def add_repo(self, repo_name):
        """
        Adds a repository to the database.

        Args:
        repo_name (str): Repository name in "owner/repo" format.
        """
        repo_details = self.github_handler.fetch_repo_details(repo_name)
        if repo_details:
            self.repo_collection.insert_one(repo_details)
            central_logger.info(f"Added repository {repo_name} to the database.")
        else:
            central_logger.warning(f"Failed to add repository {repo_name}.")

    def add_issue(self, repo_name, issue):
        """
        Adds an issue to the database.

        Args:
        repo_name (str): Repository name in "owner/repo" format.
        issue (dict): Issue details fetched from GitHub API.
        """
        repo_details = self.github_handler.fetch_repo_details(repo_name)
        if repo_details:
            issue_obj = self.build_issue_object(repo_details, issue)
            self.issues_collection.insert_one(issue_obj)
            central_logger.info(f"Added issue #{issue['number']} from {repo_name} to the database.")
        else:
            central_logger.warning(f"Failed to add issue #{issue.get('number')} from {repo_name}.")

    def remove_issue(self, repo_name, issue):
        """
        Removes an issue from the database.

        Args:
        repo_name (str): Repository name in "owner/repo" format.
        issue (dict): Issue details fetched from GitHub API.
        """
        try:
            # Extract issue number and repo_full_name
            issue_number = issue.get('number')
            repo_full_name = repo_name

            # Construct the filter to locate the issue in the database
            filter_query = {
                "repo_full_name": repo_full_name,
                "issue_number": issue_number
            }

            # Attempt to delete the document
            result = self.issues_collection.delete_one(filter_query)

            if result.deleted_count > 0:
                central_logger.info(f"Removed issue #{issue_number} from {repo_full_name} from the database.")
            else:
                central_logger.warning(f"Issue #{issue_number} not found in {repo_full_name}. No action taken.")
        except Exception as e:
            central_logger.warning(f"Failed to remove issue #{issue.get('number')} from {repo_name}: {e}")

    def update_issue(self, repo_name, issue):
        """
        Updates an issue in the database by replacing the labels.

        Args:
        repo_name (str): Repository name in "owner/repo" format.
        issue (dict): Issue details fetched from GitHub API.
        """
        try:
            # Extract issue number and repo_full_name
            issue_number = issue.get('number')
            repo_full_name = repo_name

            # Construct the filter to locate the issue in the database
            filter_query = {
                "repo_full_name": repo_full_name,
                "issue_number": issue_number
            }

            update = {
            "issue_html_url": issue.get("html_url"),
            "issue_number": issue.get("number"),
            "issue_title": issue.get("title"),
            "labels": [label.get("name") for label in issue.get("labels", [])],
            }

            # Define the update operation to replace the labels
            update_operation = {
                "$set": update
            }

            # Attempt to update the document
            result = self.issues_collection.update_one(filter_query, update_operation)

            if result.matched_count > 0:
                central_logger.info(f"Replaced labels for issue #{issue_number} in {repo_full_name} with {new_labels}.")
            else:
                central_logger.warning(f"Issue #{issue_number} not found in {repo_full_name}. No action taken.")
        except Exception as e:
            central_logger.warning(f"Failed to replace labels for issue #{issue.get('number')} in {repo_name}: {e}")



# Load environment variables
load_dotenv()
MONGO_DB_URI = os.getenv("MONGO_DB_URI")
mongo_handler = MongoDBHandler(db_uri=MONGO_DB_URI, github_handler=github_handler)
