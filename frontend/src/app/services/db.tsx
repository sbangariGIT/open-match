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