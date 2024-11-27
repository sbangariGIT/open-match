import { IssueCard } from "../models/IssueCard";
import { Issue } from '../models/Issues';
import { ProfileFormValues } from "../components/Form";

export const getMatchingIssueCards = async (formData: ProfileFormValues): Promise<IssueCard[]> => {
  const payload = await convertToJSON(formData);
  // change to http://localhost:8080/ to test locally
  const response = await fetch(`${process.env.NEXT_PUBLIC_ISSUES_API_URL}`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: payload, // Send form data as JSON
  });

  // Check if the response is okay
  if (!response.ok) {
    throw new Error(`HTTP error! Status: ${response.status}`);
  }

  const jsonResponse = await response.json();

  // Check if 'results' exist in the response
  if (!jsonResponse.results || !Array.isArray(jsonResponse.results)) {
    if (jsonResponse.error) {
      throw new Error(jsonResponse.error);
    } else {
      throw new Error("There was an error in processing your request");
    }

  }

  const data: IssueCard[] = jsonResponse.results; // Access 'results' field
  return data;
}

async function convertToJSON(payload: ProfileFormValues) {
  const { firstName, lastName, email, urls, resume, interests } = payload;

  // Initialize an empty object for the JSON payload
  const jsonPayload: Record<string, string | string[]> = {
    firstName,
    lastName,
    email,
    interests,
  };

  // Convert resume to Base64 if it exists
  if (resume) {
    const resumeBase64 = await fileToBase64(resume);
    // Include resume only if Base64 conversion is successful
    if (resumeBase64) {
      jsonPayload.resume = resumeBase64;
    }
  }

  // Include 'urls' only if it's not empty or just ['']
  if (urls && urls.length > 0 && !(urls.length === 1 && urls[0] === '')) {
    jsonPayload.urls = urls;
  }
  return JSON.stringify(jsonPayload);
}

function fileToBase64(file: File): Promise<string> {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.readAsDataURL(file);
    reader.onload = () => resolve(reader.result as string);
    reader.onerror = (error) => reject(error);
  });
}

export const getSearchIssueCards = async (): Promise<Issue[]> => {
  //TODO: Change this to an API call
  const sampleIssues: Issue[] = [
    {
      repo_name: "react",
      repo_full_name: "facebook/react",
      repo_html_url: "https://github.com/facebook/react",
      repo_description: "A JavaScript library for building user interfaces",
      repo_stars: 210000,
      repo_watchers: 8000,
      languages: ["JavaScript", "TypeScript"],
      repo_topics: ["frontend", "ui", "framework"],
      issue_html_url: "https://github.com/facebook/react/issues/1",
      issue_number: 1,
      issue_title: "Add better error messages for hooks",
      labels: ["enhancement", "good first issue"],
    },
    {
      repo_name: "tensorflow",
      repo_full_name: "tensorflow/tensorflow",
      repo_html_url: "https://github.com/tensorflow/tensorflow",
      repo_description: "An Open Source Machine Learning Framework",
      repo_stars: 180000,
      repo_watchers: 6000,
      languages: ["Python", "C++"],
      repo_topics: ["machine-learning", "neural-networks"],
      issue_html_url: "https://github.com/tensorflow/tensorflow/issues/2",
      issue_number: 2,
      issue_title: "Update documentation for custom layers",
      labels: ["documentation", "help wanted"],
    },
    {
      repo_name: "flask",
      repo_full_name: "pallets/flask",
      repo_html_url: "https://github.com/pallets/flask",
      repo_description: "A lightweight WSGI web application framework",
      repo_stars: 65000,
      repo_watchers: 2000,
      languages: ["Python"],
      repo_topics: ["web", "framework", "backend"],
      issue_html_url: "https://github.com/pallets/flask/issues/3",
      issue_number: 3,
      issue_title: "Deprecation warning on Werkzeug update",
      labels: ["bug", "good first issue"],
    },
    {
      repo_name: "vue",
      repo_full_name: "vuejs/vue",
      repo_html_url: "https://github.com/vuejs/vue",
      repo_description: "The Progressive JavaScript Framework",
      repo_stars: 210000,
      repo_watchers: 7000,
      languages: ["JavaScript", "TypeScript"],
      repo_topics: ["frontend", "ui", "framework"],
      issue_html_url: "https://github.com/vuejs/vue/issues/4",
      issue_number: 4,
      issue_title: "Improve performance for large lists",
      labels: ["performance", "enhancement"],
    },
    {
      repo_name: "django",
      repo_full_name: "django/django",
      repo_html_url: "https://github.com/django/django",
      repo_description: "The Web framework for perfectionists with deadlines",
      repo_stars: 75000,
      repo_watchers: 3000,
      languages: ["Python"],
      repo_topics: ["web", "framework", "backend"],
      issue_html_url: "https://github.com/django/django/issues/5",
      issue_number: 5,
      issue_title: "Add async support for ORM queries",
      labels: ["enhancement", "help wanted"],
    },
    {
      repo_name: "angular",
      repo_full_name: "angular/angular",
      repo_html_url: "https://github.com/angular/angular",
      repo_description: "The modern web developer's platform",
      repo_stars: 88000,
      repo_watchers: 4000,
      languages: ["TypeScript", "JavaScript"],
      repo_topics: ["frontend", "framework"],
      issue_html_url: "https://github.com/angular/angular/issues/6",
      issue_number: 6,
      issue_title: "Support for new ES features in templates",
      labels: ["feature", "help wanted"],
    },
  ];

  // change to http://localhost:8080/ to test locally
  const response = await fetch(`${process.env.NEXT_PUBLIC_ISSUES_SEARCH_API_URL}`, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
    },
  });

  // Check if the response is okay
  if (!response.ok) {
    throw new Error(`HTTP error! Status: ${response.status}`);
  }

  const jsonResponse = await response.json();

  // Check if 'results' exist in the response
  if (!jsonResponse.results || !Array.isArray(jsonResponse.results)) {
    if (jsonResponse.error) {
      throw new Error(jsonResponse.error);
    } else {
      throw new Error("There was an error in processing your request");
    }

  }

  const data: Issue[] = jsonResponse.results; // Access 'results' field
  return data;
}