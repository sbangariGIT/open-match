from openai import OpenAI
import base64
import fitz
from dotenv import load_dotenv

SYSTEM_PROMPT = """
You are an AI assistant tasked with providing a comprehensive summary of a user. You are given a users interests, resume and/or their github, LinkedIn, Project Links.
If possible read the urls and get more information about this user.
Based on this information provide a summary of user's interests for the type of projects that the user might be interested in working, which can be used to search github open issues that they can work on.
Only provide the keywords in your summary that can be used for a semantic search. Keep your response less than 300 words.

Only reply with the summary that is going to be used to create an embedding and nothing else.
"""
MODEL = "gpt-4o-mini"


class LLMService:
    def __init__(self):
        load_dotenv()
        self.client = OpenAI()

    def pdf_to_text(self, base64_pdf: str) -> str:
        if base64_pdf == "":
            return ""
        # Decode the base64 string into binary data
        pdf_data = base64.b64decode(base64_pdf)

        # Open the binary PDF data using PyMuPDF
        pdf_document = fitz.open(stream=pdf_data, filetype="pdf")

        # Extract text from each page
        text = ""
        for page_num in range(pdf_document.page_count):
            page = pdf_document.load_page(page_num)
            text += page.get_text()

        pdf_document.close()
        return text

    def get_user_summary(self, user):
        content = [
            {
                "type": "text",
                "text": SYSTEM_PROMPT,
            },
            {
                "type": "text",
                "text": f"Interests: {user.interests}, URLS: {user.urls}",
            },
            {
                "type": "text",
                "text": f"Resume Text Extracted from PDF:{self.pdf_to_text(user.resume)}",
            },
        ]
        try:
            response = self.client.chat.completions.create(
                model=MODEL, messages=[{"role": "user", "content": content}]
            )
            return response.choices[0].message.content
        except Exception as e:
            # TODO: Log this, better solution needed
            return """Languages: Python, GoLang, JavaScript, Dart.
Frameworks & Tools: LangChain, Flask, React, Kafka, Redis, MongoDB, Firebase, Docker, Kubernetes.
Topics of Interest: AI-powered applications, microservices, cloud infrastructure, CI/CD pipelines, backend architecture, LLM integrations, tech."""  # fallback string

    def create_an_embedding(self, summary: str) -> list[float]:
        return self.client.embeddings.create(input = [summary], model="text-embedding-3-small").data[0].embedding


LLMSERVICE = LLMService() 