from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

SYSTEM_PROMPT = """
You are an AI assistant tasked with providing a comprehensive summary of an issue. You will be given documents from vector store that has the code base, these documents might be of use.
Using the information provided to you come up with a summary on what the issue is and how one can solve this issue if they were to put a PR to fix it.
If you have enough information to solve this for the user please reply with just the solution. Keep your summary less than 200 words.
"""
MODEL = "gpt-4o-mini"


class LLMService:
    def __init__(self):
        load_dotenv()
        self.client = ChatOpenAI(model=MODEL)

    def get_issue_summary(self, issues, relevant):
        """
        Generates a comprehensive summary for an issue using the issue description 
        and relevant code documents.
        
        Args:
            issues (str): Description of the issue.
            relevant (list): List of relevant code or context documents.
        
        Returns:
            str: A detailed summary including the nature of the issue and possible steps to fix it.
        """
        # Combine the inputs into a clear user prompt
        user_input = f"Issue Description:\n{issues}\n\nRelevant Documents:\n{relevant}"
        messages = [
            ("system", SYSTEM_PROMPT),
            ("user", user_input)
        ]

        response = self.client.invoke(messages)
        return response.content


llm_service = LLMService()
