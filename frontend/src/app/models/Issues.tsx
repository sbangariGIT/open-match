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
class IssueClass {
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
  
    constructor(data: any) {
      this.repo_name = data.repo_name || "";
      this.repo_full_name = data.repo_full_name || "";
      this.repo_html_url = data.repo_html_url || "";
      this.repo_description = data.repo_description || "";
      this.repo_stars = data.repo_stars?.$numberInt ? parseInt(data.repo_stars.$numberInt) : 0;
      this.repo_watchers = data.repo_watchers?.$numberInt ? parseInt(data.repo_watchers.$numberInt) : 0;
      this.languages = Array.isArray(data.languages) ? data.languages : [];
      this.repo_topics = Array.isArray(data.repo_topics) ? data.repo_topics : [];
      this.issue_html_url = data.issue_html_url || "";
      this.issue_number = data.issue_number?.$numberInt ? parseInt(data.issue_number.$numberInt) : 0;
      this.issue_title = data.issue_title || "";
      this.labels = Array.isArray(data.labels) ? data.labels : [];
    }
  
    static fromJSON(json: any): IssueClass {
      return new IssueClass(json);
    }
  }
  