import React from 'react';
import { IssueCard } from "../models/IssueCard";

interface CardProps {
  index: number;
  issueCard: IssueCard;
}

const IssueCardContainer: React.FC<CardProps> = ({ index, issueCard }) => {
  return (
    <div
      className="p-4 mb-4 border rounded-lg shadow-md"
      style={{ backgroundColor: index % 2 === 0 ? '#6C63FF' : '#00000' }}
    >
      <h2 className="text-xl font-semibold mb-2">{issueCard.title}</h2>
      <div className="text-sm mb-2">
        <span>Repository: {issueCard.repoName}</span> | 
        <a href={issueCard.issueLink} className="ml-1">
          Issue #{issueCard.issueNumber}
        </a>
      </div>
      <p className="mb-4">{issueCard.description}</p>

      <div className="flex flex-wrap gap-2 mb-4">
        {issueCard.tags.map((tag, idx) => (
          <span
            key={idx}
            className="px-3 py-1 text-sm border-2 border-white rounded-lg text-center rounded-full"
          >
            {tag}
          </span>
        ))}
      </div>

      <div className="flex justify-between items-center">
        <span className="text-lg font-bold">Match: {issueCard.match}%</span>
        <a href={issueCard.issueLink} className="text-sm">
          View Issue
        </a>
      </div>
    </div>
  );
};

export default IssueCardContainer;
