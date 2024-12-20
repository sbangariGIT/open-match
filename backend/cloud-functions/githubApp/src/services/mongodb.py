import os
import time
from ..logging.logger import central_logger
from dotenv import load_dotenv
from pymongo import MongoClient
from .githubHandler import github_handler
from .llm import llm_service
from langchain_community.vectorstores import MongoDBAtlasVectorSearch
from langchain_openai import OpenAIEmbeddings

class MongoDBHandler:
    def __init__(self, db_uri, github_handler, llm_service):
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
        self.repo_source_code_collection = self.db.repo_source_code
        self.repo_source_code_index = "source_code_knn_search"
        self.github_handler = github_handler
        self.llm_service = llm_service
        self.embedding_function =  OpenAIEmbeddings()

    def build_issue_object(self, repo, issue, summary):
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
            "summary": summary,
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
                central_logger.info(f"Trying to Index new repository {repo_name} to the database.")
                self.make_vector_store_embedding(repo_name=repo_name, repo_details=repo_details, collection=self.repo_source_code_collection)
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
                # Delete all matching documents
                result = self.repo_source_code_collection.delete_many({"repo_name": repo_full_name})
                # Check if the operation was successful
                if result.deleted_count > 0:
                    central_logger.info(f"Success: Deleted {result.deleted_count} documents with repo_name = {repo_full_name}")
                else:
                    central_logger.warning(f"Failed: No documents found with repo_name = {repo_full_name}")
            else:
                central_logger.warning(f"Repo {repo_full_name} not found in . No action taken.")
            # remove all the repo related issues from the DB
            self.remove_issue(repo_name=repo_full_name, issue={}, all=True)
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
            summary = self.generate_issue_summary(issue, repo_name)
            issue_obj = self.build_issue_object(repo_details, issue, summary)
            self.issues_collection.insert_one(issue_obj)
            central_logger.info(f"Added issue #{issue['number']} from {repo_name} to the database.")
        else:
            central_logger.warning(f"Failed to add issue #{issue.get('number')} from {repo_name}.")

    def remove_issue(self, repo_name, issue, all=False):
        """
        Removes an issue from the database.

        Args:
        repo_name (str): Repository name in "owner/repo" format.
        issue (dict): Issue details fetched from GitHub API.
        """
        try:
            # Extract issue number and repo_full_name
            issue_number = issue.get('number', "0")
            repo_full_name = repo_name

            if not all:
                
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
            else:
                filter_query = {
                    "repo_full_name": repo_full_name,
                }
                result = self.issues_collection.delete_many(filter_query)

                if result.deleted_count > 0:
                    central_logger.info(f"Removed {result.deleted_count} issues from {repo_full_name} from the database.")
                else:
                    central_logger.warning(f"Failed to remove issue #{issue.get('number', "0")} from {repo_name}: {e}")
        except Exception as e:
            central_logger.severe(f"Failed to remove issues from {repo_name}: {e}")

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

    def make_vector_store_embedding(self, repo_name, repo_details, collection):
        try:
            start = time.time()
            documents = github_handler.get_repo_files(repo=repo_name,repo_details=repo_details)
            central_logger.info(f"{repo_name} has been coverted to {len(documents)} documents")
            MongoDBAtlasVectorSearch.from_documents(
                documents=documents, embedding=self.embedding_function, collection=collection
            )
            stop = time.time()
            central_logger.info(f"Successfully loaded {len(documents)} documents to vector store for repo {repo_name} in {stop - start} seconds")
        except Exception as e:
            central_logger.severe(f"Unable to load documents to vector store for repo {repo_name}")
            print(e)

    def perform_vector_search(self, query, repo_name, k=5):
        try:
            query_embedding = self.embedding_function.embed_query(query)
            # Create the vector store
            results = self.repo_source_code_collection.aggregate([
                # Vector search stage
                {"$vectorSearch": {
                    "queryVector": query_embedding,
                    "path": "embedding",
                    "numCandidates": 100,
                    "limit": k,
                    "index": self.repo_source_code_index,
                    "filter": {"repo_name": repo_name}  # Match stage to filter by repo_name
                }}
            ])
            docs = []
            for doc in results:
                docs.append(doc['text'])
            return docs
        except Exception as e:
            central_logger.severe(f"Unable to perform vector search for repo {repo_name}")
            print(e)

    def generate_issue_summary(self, issue, repo_name):
        query = self._issue_to_text(issue)
        get_relevant_docs = self.perform_vector_search(query, repo_name)
        central_logger.info(f"For the Issue {query}, here are our relevant document information {get_relevant_docs}")
        return self.llm_service.get_issue_summary(query, get_relevant_docs)
    
    def _issue_to_text(self, issue) -> str:
        #TODO: convert this issue into proper text
        return issue.get('title', 'Could not get issue') #FIXME



# Load environment variables
load_dotenv()
MONGO_DB_URI = os.getenv("MONGO_DB_URI")
mongo_handler = MongoDBHandler(db_uri=MONGO_DB_URI, github_handler=github_handler, llm_service=llm_service)
