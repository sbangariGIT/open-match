import requests
import time
import json

JSON_FILE = "../../issues_data.json"

# Replace 'YOUR_GITHUB_TOKEN' with your actual GitHub personal access token
GITHUB_TOKEN = "YOUR_GITHUB_TOKEN"

# API URL for GitHub search
REPO_SEARCH_API_URL = "https://api.github.com/search/repositories"
REPO_ISSUES_API_URL = "https://api.github.com/repos/{repo_name}/issues"

LANGUAGES = [
    "Python", "JavaScript", "Java", "Ruby", "PHP", "C++", "C#", "TypeScript",
    "Go", "Swift", "Kotlin", "Rust", "Scala", "Objective-C", "Shell", "R",
    "Perl", "Dart", "Haskell", "Lua", "Elixir", "Clojure"
]

ISSUES = []

def build_issue_object(repo, issue):

    labels = [ l["name"] for l in issue["labels"]]
    issue_obj = {
        "repo_name":        repo["name"],
        "repo_full_name":   repo["full_name"],
        "repo_html_url":    repo["html_url"],
        "repo_description": repo["description"],
        "repo_languages":   repo["languages"],
        "repo_topics":      repo["topics"],
        "issue_html_url":   issue["issue_html_url"],
        "issue_number":     issue["issue_number"],
        "issue_title":      issue["issue_title"],
        "issue_labels":     labels
    }
    return issue_obj

def fetch_repo_issues(repo, issues_per_page=50):
    """
    Fetches open issues for a given GitHub repository.

    Args:
    repo (str): The repository in "owner/repo" format (e.g., "microsoft/vscode").

    Returns:
    list: A list of open issues with details like title, URL, and creator.
    """
    issues = []
    num_issues = repo["open_issues_count"]
    pages = num_issues//issues_per_page
    if num_issues%issues_per_page > 0:
        pages += 1
    issue_url = REPO_ISSUES_API_URL.format(repo_name=repo["full_name"])
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    cur_page = 1
    while cur_page <= pages:
        params = {
            "state": "open",
            "per_page": issues_per_page,
            "page": cur_page
        }
        response = requests.get(issue_url, headers=headers, params=params)

        if response.status_code == 200:
            issues_data = response.json()
            issues += [
                {
                    "issue_number"  : issue["number"],
                    "issue_title"   : issue["title"],
                    "labels"        : issue["labels"],
                    "issue_html_url": issue["html_url"]
                }
                for issue in issues_data if "pull_request" not in issue
            ]

            cur_page += 1
        else:
            print(f"Failed to fetch issues for {repo}: {response.status_code}")
            print("Retrying in 10 seconds")
            time.sleep(10)
            print("Retrying...")

    return issues

def get_languages(lang_url):
    """
    Fetch languages used in the particular Repo

    Args:
    lang_url (str): Github repo languages API URL

    Returns:
    list: A list of all the languages used in the repo
    """
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
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
            print("Retrying in 10 seconds")
            time.sleep(10)
            print("Retrying...")

def get_repo_by_language(language="python", sort_by="stars", per_page=30, page=1):
    """
    Fetch trending repositories on GitHub based on programming language and sorting criteria.

    Args:
    language (str): Programming language to filter by (e.g., 'python', 'javascript').
    sort_by (str): Criteria to sort by, e.g., 'stars', 'forks', 'updated'.
    per_page (int): Number of repositories per page.
    page (int): Page number for paginated results.

    Returns:
    list: A list of repositories with details like name, owner, stars, and repo URL.
    """
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    params = {
        "q": f"language:{language}",
        "sort": sort_by,
        "order": "desc",
        "per_page": per_page,
        "page": page
    }
    while 1:
        response = requests.get(REPO_SEARCH_API_URL, headers=headers, params=params)
        if response.status_code == 200:
            repo_data = response.json().get("items", [])
            repos = []
            for repo in repo_data:
                languages = get_languages(repo["languages_url"])
                repos = [
                    {
                        "name": repo["name"],
                        "full_name": repo["full_name"],
                        "forks": repo["forks"],
                        "html_url": repo["html_url"],
                        "languages": languages,
                        "issues_url": repo["issues_url"],
                        "open_issues_count": repo["open_issues_count"],
                        "topics": repo["topics"],
                        "description": repo["description"]
                    }
                ]
            return repos
        else:
            print(f"Failed to fetch repositories: {response.status_code}")
            print("Retrying in 10 seconds")
            time.sleep(10)
            print("Retrying...")


if __name__ == "__main__":
    # Example usage: Fetch top 5 Python repositories sorted by stars
    for language in LANGUAGES:

        print(f"Fetching {language}")
        trending_repos = get_repo_by_language(language=language, sort_by="forks", per_page=30)
        print(f"Trending {language} Repositories:")
        for i, repo in enumerate(trending_repos, start=1):
            issues = fetch_repo_issues(repo)
            for issue in issues:
                ISSUES.append(build_issue_object(repo, issue))
        time.sleep(3)

    with open(JSON_FILE, "w") as file:
        json.dump(ISSUES, file, indent=2)
