export interface Issue {
    repo_name: string;
    repo_full_name: string;
    repo_html_url: string;
    repo_description: string;
    repo_stars: number;
    repo_watchers: number;
    languages: string[];
    repo_topics: string[];
    issue_html_url: string;
    issue_number: number;
    issue_title: string;
    labels: string[];
}