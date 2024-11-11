import { IssueCard } from "../models/IssueCard";
import { ProfileFormValues } from "../components/Form";

export const getIssueCards = async (formData: ProfileFormValues): Promise<IssueCard[]> => {
    const isLocal = process.env.LOCAL_ENV === 'true' || process.env.NODE_ENV === 'development';
    if (isLocal) {
        // Return dummy data if environment is local
        return [
            {
                title: "Fix bug in user authentication",
                repoName: "user-auth",
                issueNumber: "1",
                issueLink: "https://github.com/user-auth/issues/1",
                description: "Bug in the user authentication flow",
                tags: ["bug", "authentication"],
                match: 90
            },
            {
                title: "Improve landing page UI",
                repoName: "frontend",
                issueNumber: "2",
                issueLink: "https://github.com/frontend/issues/2",
                description: "Enhance the UI/UX for the landing page",
                tags: ["enhancement", "UI/UX"],
                match: 85
            },
            {
                title: "Add unit tests for auth services",
                repoName: "auth-service",
                issueNumber: "3",
                issueLink: "https://github.com/auth-service/issues/3",
                description: "Add unit tests to improve code coverage",
                tags: ["testing", "auth"],
                match: 80
            },
            {
                title: "Optimize database queries",
                repoName: "backend",
                issueNumber: "4",
                issueLink: "https://github.com/backend/issues/4",
                description: "Improve database query performance",
                tags: ["optimization", "backend"],
                match: 70
            }
        ];
    } else {
      const payload = await convertToJSON(formData);
      const response = await fetch('/api/issues', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(payload), // Send form data as JSON
      });
      const data: IssueCard[] = await response.json();
      return data;
    }
}

async function convertToJSON(payload: ProfileFormValues) {
    const { firstName, lastName, email, urls, resume, interests } = payload;
    let resumeBase64: string | null = null;
    if (resume) {
      resumeBase64 = await fileToBase64(resume);
    }

    const jsonPayload = {
      firstName,
      lastName,
      email,
      urls,
      resume: resumeBase64,
      interests,
    };
  
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
