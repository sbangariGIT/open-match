import React, { useState, useEffect } from "react";
import { Issue } from "../models/Issues";

type Props = {
    issues: Issue[]; // List of issues passed as a prop
    isLoading: boolean;
    isError: boolean;
};

const IssueBoard: React.FC<Props> = ({ issues,  isLoading, isError }) => {
    // State for filters and pagination
    const [filterLabels, setFilterLabels] = useState<string[]>([]);
    const [filterLanguages, setFilterLanguages] = useState<string[]>([]);
    const [filteredIssues, setFilteredIssues] = useState<Issue[]>(issues);
    const [currentPage, setCurrentPage] = useState(1); // current page number
    const [totalPages, setTotalPages] = useState(1); // total number of pages

    // Update filteredIssues whenever filters change
    useEffect(() => {
        setFilteredIssues(
            issues.filter((issue) => {
                const matchesLabels =
                    filterLabels.length === 0 ||
                    filterLabels.every((label) => issue.labels.includes(label));
                const matchesLanguages =
                    filterLanguages.length === 0 ||
                    filterLanguages.every((lang) => issue.languages.includes(lang));

                return matchesLabels && matchesLanguages;
            })
        );
    }, [issues, filterLabels, filterLanguages]);

    // Handle page change
    const handlePageChange = (page: number) => {
        setCurrentPage(page);
        // Fetch paginated data here (e.g., make an API call to fetch issues for the selected page)
        fetchIssues(page);
    };

    const fetchIssues = async (page: number) => {
        const limit = 20; // You can adjust this value based on your needs
        const response = await fetch(`/api/issues?limit=${limit}&page=${page}`);
        const data = await response.json();

        // Update filtered issues based on the fetched data
        setFilteredIssues(data.issues);
        setTotalPages(data.totalPages); // Assuming backend returns the total number of pages
    };

    // Handlers for filter changes
    const handleLabelChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        const value = event.target.value;
        setFilterLabels(
            filterLabels.includes(value)
                ? filterLabels.filter((label) => label !== value)
                : [...filterLabels, value]
        );
    };

    const handleLanguageChange = (
        event: React.ChangeEvent<HTMLInputElement>
    ) => {
        const value = event.target.value;
        setFilterLanguages(
            filterLanguages.includes(value)
                ? filterLanguages.filter((lang) => lang !== value)
                : [...filterLanguages, value]
        );
    };

    if (isError) {
        return (
          <div className="flex justify-center items-center">
          <div className="border-2 border-white rounded-lg text-center bg-black min-h-[800px] w-[900px] flex flex-col justify-center items-center p-6">
            <img src="error.svg" alt="Oops! Something went wrong..." className="mx-auto h-40 w-auto mb-8" />
            <h2 className="text-white text-3xl font-bold mb-4">Oops! Something Went Wrong</h2>
            <p className="text-white text-lg mb-6">We hit a bump while looking for matching opportunities. But don’t worry, we’re on it!</p>
            <p className="text-white text-xl font-semibold">Please try again in a moment...</p>
          </div>
        </div>
        )
      }
    
      if (isLoading) {
        return (
      <div className="flex justify-center items-center">
      <div className="border-2 border-white rounded-lg text-center bg-black min-h-[800px] w-[900px] flex flex-col justify-center items-center p-6">
        <img src="loading.svg" alt="Searching for opportunities..." className="mx-auto h-40 w-auto mb-8 animate-pulse" />
        <h2 className="text-white text-3xl font-bold mb-4">Hold Tight, While we get you some great projects to work on!</h2>
        <p className="text-white text-lg mb-6">Exploring open-source issues that align with your skills and passions...</p>
        <p className="text-white text-xl font-semibold animate-pulse">This will only take a moment!</p>
      </div>
      </div>
    
        )
      }
      
    return (
        <div className="min-h-screen bg-black text-white p-6 flex">
            {/* Filters Section */}
            <div className="w-full lg:w-1/4 p-4 bg-gray-900 rounded-lg shadow-lg">
                {/* Labels Filter */}
                <div className="space-y-6">
                    <div className="bg-gray-800 p-6 rounded-lg shadow-lg">
                        <h3 className="text-lg font-semibold mb-4 text-white">Labels</h3>
                        <div className="space-y-2">
                            {[...new Set(issues.flatMap((issue) => issue.labels))].map((label) => (
                                <label
                                    key={label}
                                    className="flex items-center gap-3 text-sm text-gray-400 cursor-pointer hover:text-white transition"
                                >
                                    <input
                                        type="checkbox"
                                        className="w-4 h-4 accent-blue-500 rounded focus:ring-2 focus:ring-blue-400 focus:outline-none"
                                        value={label}
                                        checked={filterLabels.includes(label)}
                                        onChange={handleLabelChange}
                                    />
                                    <span className="capitalize">{label}</span>
                                </label>
                            ))}
                        </div>
                    </div>

                    {/* Languages Filter */}
                    <div className="bg-gray-800 p-6 rounded-lg shadow-lg">
                        <h3 className="text-lg font-semibold mb-4 text-white">Languages</h3>
                        <div className="space-y-2">
                            {[...new Set(issues.flatMap((issue) => issue.languages))].map((lang) => (
                                <label
                                    key={lang}
                                    className="flex items-center gap-3 text-sm text-gray-400 cursor-pointer hover:text-white transition"
                                >
                                    <input
                                        type="checkbox"
                                        className="w-4 h-4 accent-green-500 rounded focus:ring-2 focus:ring-green-400 focus:outline-none"
                                        value={lang}
                                        checked={filterLanguages.includes(lang)}
                                        onChange={handleLanguageChange}
                                    />
                                    <span className="capitalize">{lang}</span>
                                </label>
                            ))}
                        </div>
                    </div>
                </div>
            </div>

            {/* Issues Section */}
            <div className="flex-grow p-4">
                {/* Issues Display */}
                <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
                    {filteredIssues.length > 0 ? (
                        filteredIssues.map((issue, index) => (
                            <div
                                key={issue.issue_number}
                                className="p-4 mb-4 border rounded-lg shadow-md"
                                style={{ backgroundColor: index % 2 === 0 ? '#6C63FF' : '#000000' }}
                            >
                                <h2 className="text-xl font-semibold mb-2 text-white">
                                    <a
                                        href={issue.issue_html_url}
                                        target="_blank"
                                        rel="noopener noreferrer"
                                        className="hover:underline"
                                    >
                                        {issue.issue_title}
                                    </a>
                                </h2>

                                <div className="text-sm mb-2 text-gray-300">
                                    <span>Repository: </span>
                                    <a
                                        href={issue.repo_html_url}
                                        target="_blank"
                                        rel="noopener noreferrer"
                                        className="hover:underline text-blue-400"
                                    >
                                        {issue.repo_full_name}
                                    </a>
                                </div>

                                <p className="mb-4 text-gray-400">{issue.repo_description}</p>

                                <div className="flex flex-wrap gap-2 mb-4">
                                    {issue.labels.map((label, idx) => (
                                        <span
                                            key={idx}
                                            className="px-3 py-1 text-sm border-2 border-white rounded-full text-center"
                                        >
                                            {label}
                                        </span>
                                    ))}
                                </div>

                                <div className="flex flex-wrap gap-2 mb-4">
                                    {issue.languages.map((lang, idx) => (
                                        <span
                                            key={idx}
                                            className="px-3 py-1 text-sm border-2 border-gray-400 rounded-full text-center"
                                        >
                                            {lang}
                                        </span>
                                    ))}
                                </div>

                                <div className="flex justify-between items-center text-white">
                                    <span className="text-lg font-bold">
                                        Stars: {issue.repo_stars} | Watchers: {issue.repo_watchers}
                                    </span>
                                    <a
                                        href={issue.issue_html_url}
                                        target="_blank"
                                        rel="noopener noreferrer"
                                        className="text-sm text-blue-400 hover:underline"
                                    >
                                        View Issue
                                    </a>
                                </div>
                            </div>
                        ))
                    ) : (
                        <p className="col-span-full text-center text-gray-500">
                            No results match your filters.
                        </p>
                    )}
                </div>

                {/* Pagination Controls */}
                <div className="flex justify-center gap-4 mt-6">
                    <button
                        onClick={() => handlePageChange(currentPage - 1)}
                        disabled={currentPage === 1}
                        className="px-4 py-2 bg-blue-600 rounded-lg hover:bg-blue-500 disabled:bg-gray-600 transition-all"
                    >
                        Previous
                    </button>
                    <span className="text-lg font-semibold">
                        Page {currentPage} of {totalPages}
                    </span>
                    <button
                        onClick={() => handlePageChange(currentPage + 1)}
                        disabled={currentPage === totalPages}
                        className="px-4 py-2 bg-blue-600 rounded-lg hover:bg-blue-500 disabled:bg-gray-600 transition-all"
                    >
                        Next
                    </button>
                </div>
            </div>
        </div>
    );

};

export default IssueBoard;
