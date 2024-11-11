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
                match: 85
            },
            {
                title: "Improve landing page UI",
                repoName: "frontend",
                issueNumber: "2",
                issueLink: "https://github.com/frontend/issues/2",
                description: "Enhance the UI/UX for the landing page",
                tags: ["enhancement", "UI/UX"],
                match: 90
            },
            {
                title: "Add unit tests for auth services",
                repoName: "auth-service",
                issueNumber: "3",
                issueLink: "https://github.com/auth-service/issues/3",
                description: "Add unit tests to improve code coverage",
                tags: ["testing", "auth"],
                match: 75
            },
            {
                title: "Optimize database queries",
                repoName: "backend",
                issueNumber: "4",
                issueLink: "https://github.com/backend/issues/4",
                description: "Improve database query performance",
                tags: ["optimization", "backend"],
                match: 80
            }
        ];
    } else {
        // Fetch issue cards from the API if environment is not local
        // Replace the API URL with your actual endpoint
      const response = await fetch('/api/issues', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData), // Send form data as JSON
      });
      const data: IssueCard[] = await response.json();
      return data;
    }
}