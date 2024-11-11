from pydantic import BaseModel, EmailStr, HttpUrl, Field
from typing import List, Optional
from ..services.llm import LLMSERVICE


class UserProfile(BaseModel):
    firstName: str = Field(..., min_length=1, max_length=50)
    lastName: str = Field(..., min_length=1, max_length=50)
    email: EmailStr
    urls: Optional[List[HttpUrl]] = []
    resume: Optional[str] = Field(
        default="",
        pattern=r"^data:application/pdf;base64,[A-Za-z0-9+/=]*$",
        description="Base64 encoded PDF string",
    )
    interests: List[str]

    class Config:
        json_schema_extra = {
            "example": {
                "firstName": "John",
                "lastName": "Doe",
                "email": "john.doe@example.com",
                "urls": [
                    "https://github.com/johndoe",
                    "https://linkedin.com/in/johndoe",
                ],
                "resume": "data:application/pdf;base64,JVBERi0xLjMKJcfsj6IKNSAwIG9iago8PC9...",
                "interests": ["open-source", "web development", "TypeScript"],
            }
        }

    def get_summary_for_embedding(self):
        try:
            summary = LLMSERVICE.get_user_summary(self)
            return summary
        except Exception as e:
            return """Languages: Python, GoLang, JavaScript, Dart.
Frameworks & Tools: LangChain, Flask, React, Kafka, Redis, MongoDB, Firebase, Docker, Kubernetes.
Topics of Interest: AI-powered applications, microservices, cloud infrastructure, CI/CD pipelines, backend architecture, LLM integrations, tech."""

    def get_query_embedding(self):
        try:
            embedding = LLMSERVICE.create_an_embedding(self.get_summary_for_embedding())
            return embedding
        except Exception as e:
            return []
