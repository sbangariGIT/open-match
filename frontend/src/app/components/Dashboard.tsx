'use client';

import React, { useState } from 'react';
import Form, { ProfileFormValues } from './Form';
import { IssueCard } from '../models/IssueCard';
import IssueMatcher from './IssueMatcher';
import { getIssueCards } from '../services/db';

const Dashboard: React.FC = () => {
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [isError, setIsError] = useState<boolean>(false);
  const [issues, setIssues] = useState<IssueCard[]>([]);

  const handleFormSubmit = async (data: ProfileFormValues) => {
    setIsLoading(true);
    setIsError(false); // Reset error state before new request
    try {
      const result = await getIssueCards(data);
      setIssues(result);
    } catch (error) {
      setIsError(true); // Handle error if API call fails
      console.error('Error:', error);
    } finally {
      setIsLoading(false); // Stop loading state once the request is done
    }
  };

  return (
    <div id="dashboard" className="grid gap-8 font-[family-name:var(--font-geist-sans)]">
    <div className="row-start-2">
    <Form onSubmit={handleFormSubmit} />
    </div>
    <div className="row-start-2">
    <IssueMatcher issueCards={issues} isLoading={isLoading} isError={isError}/>
    </div>
    </div>
  );
};

export default Dashboard;