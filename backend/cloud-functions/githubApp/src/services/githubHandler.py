import os
import requests
from ..logging.logger import central_logger
from langchain_community.document_loaders import GithubFileLoader
from dotenv import load_dotenv

LANGUAGE_EXTENSTIONS = (
    ".py", ".pyw", ".pyc", ".pyo", 
    ".js", ".mjs", ".cjs", 
    ".ts", ".tsx", 
    ".java", 
    ".c", ".h", 
    ".cpp", ".cc", ".cxx", ".h", ".hpp", ".hxx", 
    ".rb", ".rbw", 
    ".php", ".php3", ".php4", ".php5", ".phtml", 
    ".swift", 
    ".go", 
    ".rs", 
    ".kt", ".kts", 
    ".scala", 
    ".m", ".h", 
    ".html", ".htm", 
    ".css", 
    ".scss", ".sass", 
    ".less", 
    ".json", 
    ".xml", 
    ".yaml", ".yml", 
    ".md", ".markdown", 
    ".lua", 
    ".sh", ".bash", ".zsh", 
    ".r", ".rmd", 
    ".m", 
    ".hs", 
    ".pl", ".pm", ".t", 
    ".sql", 
    ".tex", 
    ".dart", 
    ".ex", ".exs", 
    ".cs", 
    ".fs", 
    ".vhdl", ".vhd", 
    ".v", ".sv", ".svh", 
    ".cob", ".cbl", 
    ".f90", ".f95", ".f03", ".f08", 
    ".asm", ".s", 
    ".as", 
    ".pl", ".pro", 
    ".rkt", 
    ".vala", 
    ".cr", 
    ".4th", ".fs", 
    ".jl", 
    ".hh", ".php", ".hack", 
    ".tcl", 
    ".scm", ".ss", 
    ".sol", 
    ".coffee"
)


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
        
    def get_repo_files(self, repo, repo_details):
        """
        Index the repo and store it in vector DB

        Args:
        repo (str): Repository in "owner/repo" format.

        Returns:
        documents: of repo files
        """
        try:
            loader = GithubFileLoader(
                repo=repo,  # the repo name
                branch=repo_details.get("default_branch"),
                access_token=self.github_token,
                github_api_url="https://api.github.com",
                file_filter=lambda file_path: file_path.endswith(
                    LANGUAGE_EXTENSTIONS # load all markdowns files.
                ),
            )
            documents = loader.load()
            for document in documents:
                document["repo_name"] = repo  # Adding the repo_name field to help with filtering
            return documents
        except Exception as e:
            central_logger.severe(f"Failed to Index files of repo {repo}")
            print(e)


# Load environment variables
load_dotenv()
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

# Instantiate handlers
github_handler = GitHubHandler(github_token=GITHUB_TOKEN)