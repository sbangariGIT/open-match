export interface IssueCard {
    title: string;
    repoName: string;
    issueNumber: string;
    issueLink: string;
    description: string;
    tags: string[];
    match: number
}


export function createIssueCard(
    title: string,
    repoName: string,
    issueNumber: string,
    issueLink: string,
    description: string,
    tags: string[],
    match: number
): IssueCard {
    return {
        title,
        repoName,
        issueNumber,
        issueLink,
        description,
        tags,
        match
    };
}
