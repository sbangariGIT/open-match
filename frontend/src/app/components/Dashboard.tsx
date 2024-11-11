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

  const handleTryAgain = () => {
    setIssues([]);
  } 

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
    <h1 className="text-5xl font-bold text-center mt-10">Dashboard</h1>
    { issues.length == 0 &&
    <div className="row-start-2">
    <Form onSubmit={handleFormSubmit} />
    </div>
    }
    <div className="row-start-2">
    <IssueMatcher issueCards={issues} isLoading={isLoading} isError={isError}/>
    </div>
    { issues.length > 0 &&
    <div className="flex items-center justify-center mt-4">
    <button 
      className="bg-[#6C63FF] text-white font-semibold py-2 px-4 rounded hover:bg-[#5a52d4] transition duration-300"
      onClick={handleTryAgain}
    >
      Try Again
    </button>
  </div>
    }
    </div>
  );
};

export default Dashboard;