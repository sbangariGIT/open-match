'use client';

import React, { useState, useRef, useEffect } from 'react';
import Form, { ProfileFormValues } from './Form';
import { IssueCard } from '../models/IssueCard';
import IssueMatcher from './IssueMatcher';
import { getMatchingIssueCards, getSearchIssueCards } from '../services/db';
import IssueBoard from './IssueSearch';
import { Issue } from '../models/Issues';

const Dashboard: React.FC = () => {
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [isError, setIsError] = useState<boolean>(false);
  const [issues, setIssues] = useState<IssueCard[]>([]);
  const [searchIssues, setSearchIssues] = useState<Issue[]>([]);
  const resultRef = useRef<HTMLElement | null>(null);
  const handleFormSubmit = async (data: ProfileFormValues) => {
    setIsLoading(true);
    setIsError(false); // Reset error state before new request
    if (resultRef.current) {
      resultRef.current.scrollIntoView({ behavior: 'smooth' });
    }
    try {
      const result = await getMatchingIssueCards(data);
      setIssues(result);
    } catch (error) {
      setIsError(true); // Handle error if API call fails
      alert(error);
    } finally {
      setIsLoading(false); // Stop loading state once the request is done
    }
  };

  useEffect(() => {
    const loadScreen = async () => {
    try {
      setIsLoading(true);
      setIsError(false); // Reset error state before new request
      const result = await getSearchIssueCards();
      setSearchIssues(result);
    } catch (error) {
      setIsError(true); // Handle error if API call fails
      alert(error);
    } finally {
      setIsLoading(false); // Stop loading state once the request is done
    }
  }
  loadScreen();
  }, []);

  const [selectedView, setSelectedView] = useState<'IssueSearch' | 'IssueMatching'>('IssueSearch');

  return (
    <div id="dashboard" className="grid gap-8 font-[family-name:var(--font-geist-sans)]">
      <div className="relative mt-10">
        {/* Horizontal line */}
        <div className="absolute top-1/2 w-full h-0.5 bg-gray-300 -translate-y-1/2"></div>

        {/* Buttons */}
        <div className="flex justify-center">
          <button
            className={`relative z-10 px-6 py-2 border border-gray-300 rounded-l-full transition-colors duration-300 ${selectedView === 'IssueSearch' ? 'bg-white text-black' : 'bg-black text-white'
              }`}
            onClick={() => setSelectedView('IssueSearch')}
          >
            Issue Search
          </button>
          <button
            className={`relative z-10 px-6 py-2 border border-gray-300 rounded-r-full transition-colors duration-300 ${selectedView === 'IssueMatching' ? 'bg-white text-black' : 'bg-black text-white'
              }`}
            onClick={() => setSelectedView('IssueMatching')}
          >
            Issue Matching
          </button>
        </div>
      </div>
      {selectedView === 'IssueMatching' &&
        (<div>
          <h1 className="text-5xl font-bold text-center mt-10 mb-6">Fill your profile</h1>
          <div className="row-start-2">
            <Form onSubmit={handleFormSubmit} />
          </div>
          <div className="flex items-center justify-center mt-4">
            <section id='results' ref={resultRef}>
              <IssueMatcher issueCards={issues} isLoading={isLoading} isError={isError} />
            </section>
          </div>
        </div>)}
      {selectedView === 'IssueSearch' &&
        (<div>
          <h1 className="text-5xl font-bold text-center mt-10">Issue Search</h1>
          <div className="row-start-2">
            <IssueBoard issues={searchIssues} isLoading={isLoading} isError={isError}></IssueBoard>
          </div>
        </div>)}
    </div>
  );
};

export default Dashboard;