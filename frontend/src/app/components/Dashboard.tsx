'use client';

import React, { useState, useRef } from 'react';
import Form, { ProfileFormValues } from './Form';
import { IssueCard } from '../models/IssueCard';
import IssueMatcher from './IssueMatcher';
import { getIssueCards } from '../services/db';
import IssueBoard from './IssueSearch';
import { Issue } from "../models/issues";

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
  const sampleIssues: Issue[] = [
    {
      repo_name: "react",
      repo_full_name: "facebook/react",
      repo_html_url: "https://github.com/facebook/react",
      repo_description: "A JavaScript library for building user interfaces",
      repo_stars: 210000,
      repo_watchers: 8000,
      languages: ["JavaScript", "TypeScript"],
      repo_topics: ["frontend", "ui", "framework"],
      issue_html_url: "https://github.com/facebook/react/issues/1",
      issue_number: 1,
      issue_title: "Add better error messages for hooks",
      labels: ["enhancement", "good first issue"],
    },
    {
      repo_name: "tensorflow",
      repo_full_name: "tensorflow/tensorflow",
      repo_html_url: "https://github.com/tensorflow/tensorflow",
      repo_description: "An Open Source Machine Learning Framework",
      repo_stars: 180000,
      repo_watchers: 6000,
      languages: ["Python", "C++"],
      repo_topics: ["machine-learning", "neural-networks"],
      issue_html_url: "https://github.com/tensorflow/tensorflow/issues/2",
      issue_number: 2,
      issue_title: "Update documentation for custom layers",
      labels: ["documentation", "help wanted"],
    },
    {
      repo_name: "flask",
      repo_full_name: "pallets/flask",
      repo_html_url: "https://github.com/pallets/flask",
      repo_description: "A lightweight WSGI web application framework",
      repo_stars: 65000,
      repo_watchers: 2000,
      languages: ["Python"],
      repo_topics: ["web", "framework", "backend"],
      issue_html_url: "https://github.com/pallets/flask/issues/3",
      issue_number: 3,
      issue_title: "Deprecation warning on Werkzeug update",
      labels: ["bug", "good first issue"],
    },
    {
      repo_name: "vue",
      repo_full_name: "vuejs/vue",
      repo_html_url: "https://github.com/vuejs/vue",
      repo_description: "The Progressive JavaScript Framework",
      repo_stars: 210000,
      repo_watchers: 7000,
      languages: ["JavaScript", "TypeScript"],
      repo_topics: ["frontend", "ui", "framework"],
      issue_html_url: "https://github.com/vuejs/vue/issues/4",
      issue_number: 4,
      issue_title: "Improve performance for large lists",
      labels: ["performance", "enhancement"],
    },
    {
      repo_name: "django",
      repo_full_name: "django/django",
      repo_html_url: "https://github.com/django/django",
      repo_description: "The Web framework for perfectionists with deadlines",
      repo_stars: 75000,
      repo_watchers: 3000,
      languages: ["Python"],
      repo_topics: ["web", "framework", "backend"],
      issue_html_url: "https://github.com/django/django/issues/5",
      issue_number: 5,
      issue_title: "Add async support for ORM queries",
      labels: ["enhancement", "help wanted"],
    },
    {
      repo_name: "angular",
      repo_full_name: "angular/angular",
      repo_html_url: "https://github.com/angular/angular",
      repo_description: "The modern web developer's platform",
      repo_stars: 88000,
      repo_watchers: 4000,
      languages: ["TypeScript", "JavaScript"],
      repo_topics: ["frontend", "framework"],
      issue_html_url: "https://github.com/angular/angular/issues/6",
      issue_number: 6,
      issue_title: "Support for new ES features in templates",
      labels: ["feature", "help wanted"],
    },
    {
      repo_name: "kubernetes",
      repo_full_name: "kubernetes/kubernetes",
      repo_html_url: "https://github.com/kubernetes/kubernetes",
      repo_description: "Production-Grade Container Scheduling and Management",
      repo_stars: 95000,
      repo_watchers: 7000,
      languages: ["Go"],
      repo_topics: ["orchestration", "containers"],
      issue_html_url: "https://github.com/kubernetes/kubernetes/issues/7",
      issue_number: 7,
      issue_title: "Fix race condition in scheduling algorithm",
      labels: ["bug", "help wanted"],
    },
    {
      repo_name: "numpy",
      repo_full_name: "numpy/numpy",
      repo_html_url: "https://github.com/numpy/numpy",
      repo_description: "The fundamental package for scientific computing",
      repo_stars: 23000,
      repo_watchers: 1200,
      languages: ["Python", "C"],
      repo_topics: ["data", "science", "math"],
      issue_html_url: "https://github.com/numpy/numpy/issues/8",
      issue_number: 8,
      issue_title: "Add support for additional random distributions",
      labels: ["enhancement", "good first issue"],
    },
    {
      repo_name: "bootstrap",
      repo_full_name: "twbs/bootstrap",
      repo_html_url: "https://github.com/twbs/bootstrap",
      repo_description: "The most popular HTML, CSS, and JS library",
      repo_stars: 160000,
      repo_watchers: 5000,
      languages: ["CSS", "JavaScript"],
      repo_topics: ["frontend", "framework", "css"],
      issue_html_url: "https://github.com/twbs/bootstrap/issues/9",
      issue_number: 9,
      issue_title: "Fix inconsistency in form validation styles",
      labels: ["bug", "documentation"],
    },
    {
      repo_name: "express",
      repo_full_name: "expressjs/express",
      repo_html_url: "https://github.com/expressjs/express",
      repo_description: "Fast, unopinionated, minimalist web framework for Node.js",
      repo_stars: 60000,
      repo_watchers: 3000,
      languages: ["JavaScript"],
      repo_topics: ["backend", "framework", "web"],
      issue_html_url: "https://github.com/expressjs/express/issues/10",
      issue_number: 10,
      issue_title: "Add support for middleware chaining in async/await",
      labels: ["enhancement", "help wanted"],
    },
  ];

  const [selectedView, setSelectedView] = useState<'IssueSearch' | 'IssueMatching'>('IssueSearch');

  return (
    <div id="dashboard" className="grid gap-8 font-[family-name:var(--font-geist-sans)]">
      <div className="relative mt-10">
  {/* Horizontal line */}
  <div className="absolute top-1/2 w-full h-0.5 bg-gray-300 -translate-y-1/2"></div>
  
  {/* Buttons */}
  <div className="flex justify-center">
    <button
      className={`relative z-10 px-6 py-2 border border-gray-300 rounded-l-full transition-colors duration-300 ${
        selectedView === 'IssueSearch' ? 'bg-white text-black' : 'bg-black text-white'
      }`}
      onClick={() => setSelectedView('IssueSearch')}
    >
      Issue Search
    </button>
    <button
      className={`relative z-10 px-6 py-2 border border-gray-300 rounded-r-full transition-colors duration-300 ${
        selectedView === 'IssueMatching' ? 'bg-white text-black' : 'bg-black text-white'
      }`}
      onClick={() => setSelectedView('IssueMatching')}
    >
      Issue Matching
    </button>
  </div>
</div>
      { selectedView === 'IssueMatching' && 
        (<div>
      <h1 className="text-5xl font-bold text-center mt-10 mb-6">Fill your profile</h1>
      <div className="row-start-2">
      <Form onSubmit={handleFormSubmit} />
      </div>
      <div className="flex items-center justify-center mt-4">
      <section id='results' ref={resultRef}>
      <IssueMatcher issueCards={issues} isLoading={isLoading} isError={isError}/>
      </section>
      </div>
      </div>)}
      { selectedView === 'IssueSearch' && 
        (<div>
      <h1 className="text-5xl font-bold text-center mt-10">Issue Search</h1>
      <div className="row-start-2">
      <IssueBoard issues={sampleIssues}></IssueBoard>
      </div>
      </div>)}
    </div>
  );
};

export default Dashboard;