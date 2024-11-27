import os
import requests
from ..logging.logger import central_logger 
from dotenv import load_dotenv



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


# Load environment variables
load_dotenv()
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

# Instantiate handlers
github_handler = GitHubHandler(github_token=GITHUB_TOKEN)