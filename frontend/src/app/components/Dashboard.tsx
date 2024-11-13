'use client';

import React, { useState, useRef } from 'react';
import Form, { ProfileFormValues } from './Form';
import { IssueCard } from '../models/IssueCard';
import IssueMatcher from './IssueMatcher';
import { getIssueCards } from '../services/db';

const Dashboard: React.FC = () => {
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [isError, setIsError] = useState<boolean>(false);
  const [issues, setIssues] = useState<IssueCard[]>([]);
  const resultRef = useRef<HTMLElement | null>(null);

  const handleFormSubmit = async (data: ProfileFormValues) => {
    setIsLoading(true);
    setIsError(false); // Reset error state before new request
    if (resultRef.current) {
      resultRef.current.scrollIntoView({ behavior: 'smooth' });
    }
    try {
      const result = await getIssueCards(data);
      setIssues(result);
    } catch (error) {
      setIsError(true); // Handle error if API call fails
      alert(error);
    } finally {
      setIsLoading(false); // Stop loading state once the request is done
    }
  };

  return (
    <div id="dashboard" className="grid gap-8 font-[family-name:var(--font-geist-sans)]">
    <h1 className="text-5xl font-bold text-center mt-10">Fill your profile</h1>
    <div className="row-start-2">
    <Form onSubmit={handleFormSubmit} />
    </div>
    <div className="flex items-center justify-center mt-4">
    <section id='results' ref={resultRef}>
    <IssueMatcher issueCards={issues} isLoading={isLoading} isError={isError}/>
    </section>
    </div>
    </div>
  );
};

export default Dashboard;