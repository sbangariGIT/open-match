"""
This script is designed to load the first set of open issues into the DB.
"""

from dotenv import load_dotenv
import json
import sys
from openai import OpenAI
from pymongo import MongoClient
import os
import time

load_dotenv()
openai_client = OpenAI()
mongodb_client = MongoClient(os.environ.get("MONGODB_URI"))
db = mongodb_client.open_match
collection = db.issues
MODEL = "gpt-4o-mini"


def write_to_db(issue):
    print("adding", issue["issue_title"])
    collection.insert_one(issue)


def create_an_issue_summary(issue):
    content = [
        {
            "type": "text",
            "text": f"You are an AI Assistant that is reponsible in making a comprehensive summary of a given github issue. Use the information and make the best summary to summarize the issue possible, we have less data so you need to understand well here. Here are the details about that issue: {issue}. Only return the comprehensive summary and keep it less than 100 words",
        },
    ]
    try:
        response = openai_client.chat.completions.create(
            model=MODEL, messages=[{"role": "user", "content": content}]
        )
        print("We got summary", response.choices[0].message.content)
        return response.choices[0].message.content
    except Exception as e:
        return ""


def make_an_embedding(issue, summary):
    text_for_embedding = f"{issue}  Summary: {summary}"
    print("creating an embedding")
    return (
        openai_client.embeddings.create(
            input=[text_for_embedding], model="text-embedding-3-small"
        )
        .data[0]
        .embedding
    )


def parse_json_file(file_path):
    try:
        with open(file_path, "r") as file:
            issues = json.load(file)
        print("Trying to insert ", len(issues), "documents")
        if isinstance(issues, list):
            print("Parsed JSON objects:")
            for issue in issues:
                summary = create_an_issue_summary(issue)
                embedding = make_an_embedding(issue, summary)
                # add embedding
                issue["embedding"] = embedding
                issue["summary"] = summary
                # write to mongo db atlas
                write_to_db(issue)

        else:
            print("The JSON file does not contain a list of objects.")
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python bootstrap.py <path_to_json_file>")
    else:
        parse_json_file(sys.argv[1])
