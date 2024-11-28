# Issue Search Algorithm
Endpoint for getting the list of Issues.

TODO:
1. Work on pagination
2. Work on filters

#### GET Request

#### Response
Sample response

```
{
    "result": [
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
        ]
}
```

# Deploy to Cloud

Deploy the functions to Prod

Install: `gcloud cli`

Make sure that you are logged in and in the write project.

Run: `gcloud functions deploy <name_the_function> --runtime=python312 --source=<path to src> --entry-point=<entry-point> --trigger-http --allow-unauthenticated`

Example

`gcloud functions deploy get_issue_search --runtime=python312 --source=. --entry-point=get_issue_search --trigger-http --allow-unauthenticated`

Note: update the source key based on where the src folder is. For more details head to the google console for a cli implementation of this project.

# Run Locally

Follow the steps to be able to run the cloud function on your local environment.

1. cd into the src file of the cloud function you want test
2. Run `functions-framework-python --target <name of the function>`, example `functions-framework-python --target get_issue_search`