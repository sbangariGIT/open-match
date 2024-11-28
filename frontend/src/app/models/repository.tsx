// interface RepositoryOwner {
//     login: string;
//     id: number;
//     node_id: string;
//     avatar_url: string;
//     gravatar_id: string | null;
//     url: string;
//     html_url: string;
//     followers_url: string;
//     following_url: string;
//     gists_url: string;
//     starred_url: string;
//     subscriptions_url: string;
//     organizations_url: string;
//     repos_url: string;
//     events_url: string;
//     received_events_url: string;
//     type: string;
//     user_view_type: string;
//     site_admin: boolean;
// }

// interface RepositoryLicense {
//     key: string;
//     name: string;
//     spdx_id: string;
//     url: string;
//     node_id: string;
// }

// interface RepositoryPermissions {
//     admin: boolean;
//     maintain: boolean;
//     push: boolean;
//     triage: boolean;
//     pull: boolean;
// }

// interface Repository {
//     id: number;
//     node_id: string;
//     name: string;
//     full_name: string;
//     private: boolean;
//     owner: RepositoryOwner;
//     html_url: string;
//     description: string | null;
//     fork: boolean;
//     url: string;
//     created_at: string;
//     updated_at: string;
//     pushed_at: string;
//     git_url: string;
//     ssh_url: string;
//     clone_url: string;
//     svn_url: string;
//     homepage: string | null;
//     stargazers_count: number;
//     language: string;
//     has_issues: boolean;
//     has_projects: boolean;
//     has_downloads: boolean;
//     has_wiki: boolean;
//     has_pages: boolean;
//     has_discussions: boolean;
//     archived: boolean;
//     disabled: boolean;
//     license: RepositoryLicense | null;
//     allow_forking: boolean;
//     is_template: boolean;
//     web_commit_signoff_required: boolean;
//     topics: string[];
//     visibility: string;
//     default_branch: string;
//     permissions: RepositoryPermissions;
//     custom_properties: object;
//     organization: RepositoryOwner | null;
//     languages: string[];
// }

// class RepositoryClass {
//     id?: number;
//     node_id?: string;
//     name?: string;
//     full_name?: string;
//     private?: boolean;
//     owner?: RepositoryOwner;
//     html_url?: string;
//     description?: string | null;
//     fork?: boolean;
//     url?: string;
//     created_at?: string;
//     updated_at?: string;
//     pushed_at?: string;
//     git_url?: string;
//     ssh_url?: string;
//     clone_url?: string;
//     svn_url?: string;
//     homepage?: string | null;
//     stargazers_count?: number;
//     language?: string;
//     has_issues?: boolean;
//     has_projects?: boolean;
//     has_downloads?: boolean;
//     has_wiki?: boolean;
//     has_pages?: boolean;
//     has_discussions?: boolean;
//     archived?: boolean;
//     disabled?: boolean;
//     license?: RepositoryLicense | null;
//     allow_forking?: boolean;
//     is_template?: boolean;
//     web_commit_signoff_required?: boolean;
//     topics?: string[];
//     visibility?: string;
//     default_branch?: string;
//     permissions?: RepositoryPermissions;
//     custom_properties?: object;
//     organization?: RepositoryOwner | null;
//     languages?: string[];

//     constructor(data: Repository) {
//         Object.assign(this, data);
//     }
// }
