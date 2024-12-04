import os
from ..logging.logger import central_logger
from dotenv import load_dotenv
from pymongo import MongoClient
from .githubHandler import github_handler
# from langchain_community.vectorstores import MongoDBAtlasVectorSearch
# from langchain_openai import OpenAIEmbeddings

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
        # self.embedding_function =  OpenAIEmbeddings()

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
            result = self.repo_collection.update_one(
                {"full_name": repo_details['full_name']},  # Filter by unique field
                {"$set": repo_details},                  # Update the document
                upsert=True                              # Insert if not exists
            )
            if result.matched_count:
                central_logger.info(f"Updated repository {repo_name} in the database.")
            elif result.upserted_id:
                central_logger.info(f"Added new repository {repo_name} to the database.")
        else:
            central_logger.warning(f"Failed to fetch details for repository {repo_name}.")

    def remove_repo(self, repo_name):
        """
        Removes a repository to the database.

        Args:
        repo_name (str): Repository name in "owner/repo" format.
        """
        try:
            repo_full_name = repo_name

            # Construct the filter to locate the issue in the database
            filter_query = {
                "full_name": repo_full_name,
            }

            # Attempt to delete the document
            result = self.repo_collection.delete_one(filter_query)

            if result.deleted_count > 0:
                central_logger.info(f"Removed {repo_full_name} from the database.")
            else:
                central_logger.warning(f"Repo {repo_full_name} not found in . No action taken.")
        except Exception as e:
            central_logger.warning(f"Failed to remove repo {repo_name}: {e}")


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
                central_logger.info(f"Updated issue #{issue_number} in {repo_full_name} with {update}.")
            else:
                central_logger.warning(f"Issue #{issue_number} not found in {repo_full_name}. No action taken.")
        except Exception as e:
            central_logger.warning(f"Failed to update issue #{issue.get('number')} in {repo_name}: {e}")

    # def make_vector_store_embedding(self, repo_name):
    #     try:
    #         documents = github_handler.get_repo_files(repo=repo_name)
    #         MongoDBAtlasVectorSearch.from_documents(
    #             documents=documents, embedding=self.embedding_function, collection=self.repo_collection #TODO: repo specific collection needs to be made
    #         )
    #         central_logger.info(f"Successfully loaded documents to vector store for repo {repo_name}")
    #     except Exception as e:
    #         central_logger.severe(f"Unable to load documents to vector store for repo {repo_name}")
    #         print(e)

    # def perform_vector_search(self, query, repo_name, index_name, k=5):
    #     try:
    #         # Create the vector store
    #         vector_store = MongoDBAtlasVectorSearch(
    #             embedding=self.embedding_function,
    #             collection=self.repo_collection, #TODO: Repo specific collection needs to be made
    #             index_name=index_name,
    #             relevance_score_fn="cosine"
    #         )

    #         # Perform the vector search
    #         results = vector_store.similarity_search(query, k=k)

    #         return results
    #     except Exception as e:
    #         central_logger.severe(f"Unable to perform vector search for repo {repo_name}")
    #         print(e)



# Load environment variables
load_dotenv()
MONGO_DB_URI = os.getenv("MONGO_DB_URI")
mongo_handler = MongoDBHandler(db_uri=MONGO_DB_URI, github_handler=github_handler)
