"""
Given a repo this script is going to parse all the open issues and index them into our DB for further processing
"""

import time
import requests
import argparse
from dotenv import load_dotenv
from pymongo import MongoClient
import os
import time

load_dotenv()
mongodb_client = MongoClient(os.environ.get("MONGODB_URI"))
db = mongodb_client.open_match
collection = db.issues_new
collection_2 = db.repo

def write_to_db(issue):
    print("adding", issue["issue_title"])
    collection.insert_one(issue)

def write_to_repo_db(repo):
    print("adding", repo["name"])
    collection_2.insert_one(repo)

REPO_API_URL = "https://api.github.com/repos/{repo_name}"
REPO_ISSUES_API_URL = "https://api.github.com/repos/{repo_name}/issues"
ISSUES_JSON_FILE = "../../issues.json"
REPO_JSON_FILE = "../../repo.json"



def build_issue_object(repo, issue):

    issue_obj = {
        "repo_name": repo["name"],
        "repo_full_name": repo["full_name"],
        "repo_html_url": repo["html_url"],
        "repo_description": repo["description"],
        "repo_stars": repo["stargazers_count"],
        "repo_watchers": repo["watchers_count"],
        "languages": repo.get("languages"),
        "repo_topics": repo["topics"],
        "issue_html_url": issue["issue_html_url"],
        "issue_number": issue["issue_number"],
        "issue_title": issue["issue_title"],
        "labels": issue["labels"],
    }
    return issue_obj

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

    while 1:
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
    response = requests.get(REPO_API_URL.format(repo_name=repo), headers=headers)

    if response.status_code == 200:
        repo_data = response.json()
        repo_data["languages"] = get_languages(repo_data["languages_url"], github_token=github_token)
        return repo_data
    return {}


def fetch_repo_issues(repo, github_token, issues_per_page=50):
    """
    Fetches open issues for a given GitHub repository.

    Args:
    repo (str): The repository in "owner/repo" format (e.g., "microsoft/vscode").
    github_token (str): GitHub token for authentication.
    issues_per_page (int): Number of issues to fetch per page (default: 50).

    Returns:
    list: A list of open issues with details like title, URL, and creator.
    """
    issues = []
    issue_url = REPO_ISSUES_API_URL.format(repo_name=repo)
    headers = {
        "Authorization": f"token {github_token}",
        "Accept": "application/vnd.github.v3+json",
    }
    cur_page = 1

    while True:
        params = {"state": "open", "per_page": issues_per_page, "page": cur_page}
        response = requests.get(issue_url, headers=headers, params=params)

        if response.status_code == 200:
            issues_data = response.json()
            if not issues_data:  # Break if no more issues are returned
                break

            issues += [
                {
                    "issue_number": issue["number"],
                    "issue_title": issue["title"],
                    "labels": [label["name"] for label in issue["labels"]],
                    "issue_html_url": issue["html_url"],
                }
                for issue in issues_data
                if "pull_request" not in issue
            ]
            cur_page += 1
        else:
            print(f"Failed to fetch issues for {repo}: {response.status_code}")
            print("Retrying in 10 seconds...")
            time.sleep(10)

    return issues


if __name__ == "__main__":
    # Create an argument parser
    parser = argparse.ArgumentParser(
        description="Given a repository, this script parses all open issues and indexes them into the database for further processing."
    )

    # Add arguments
    parser.add_argument(
        "--repo",
        type=str,
        help="The repository in 'owner/repo' format (e.g., 'microsoft/vscode').",
    )
    parser.add_argument(
        "--token",
        type=str,
        required=True,
        help="GitHub personal access token for API authentication.",
    )
    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version="issueIndexer 1.0",
        help="Show the version of the script and exit.",
    )

    # Parse arguments
    args = parser.parse_args()

    # Validate repo format
    if "/" not in args.repo:
        print(
            "Error: The repository must be in 'owner/repo' format (e.g., 'microsoft/vscode')."
        )
    else:
        repo_details = fetch_repo_details(args.repo, args.token)
        write_to_repo_db(repo_details)

        # Fetch issues from the repository
        issues = fetch_repo_issues(args.repo, args.token)
        # Print fetched issues for demonstration purposes
        WRITE_TO_ISSUES_DB = []
        for issue in issues:
            WRITE_TO_ISSUES_DB.append(build_issue_object(repo_details, issue))
            write_to_db(build_issue_object(repo_details, issue))
