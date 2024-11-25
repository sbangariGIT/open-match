import React, { useState, useEffect } from "react";
import { Issue } from "../models/issues";

type Props = {
    issues: Issue[]; // List of issues passed as a prop
};

const IssueBoard: React.FC<Props> = ({ issues }) => {
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

    return (
        <div className="min-h-screen bg-black text-white p-6">
            <div className="flex flex-wrap justify-center items-center gap-6 mb-10">
                <div className="flex flex-wrap justify-center items-center gap-6 mb-10">
                    {/* Labels Filter */}
                    <div className="bg-gray-800 p-4 rounded-lg shadow-md">
                        <h3 className="text-lg font-semibold mb-3">Labels</h3>
                        {[...new Set(issues.flatMap((issue) => issue.labels))].map((label) => (
                            <label
                                key={label}
                                className="block text-sm flex items-center gap-2 mb-2 cursor-pointer hover:text-gray-300"
                            >
                                <input
                                    type="checkbox"
                                    className="accent-blue-500"
                                    value={label}
                                    checked={filterLabels.includes(label)}
                                    onChange={handleLabelChange}
                                />
                                {label}
                            </label>
                        ))}
                    </div>

                    {/* Languages Filter */}
                    <div className="bg-gray-800 p-4 rounded-lg shadow-md">
                        <h3 className="text-lg font-semibold mb-3">Languages</h3>
                        {[...new Set(issues.flatMap((issue) => issue.languages))].map((lang) => (
                            <label
                                key={lang}
                                className="block text-sm flex items-center gap-2 mb-2 cursor-pointer hover:text-gray-300"
                            >
                                <input
                                    type="checkbox"
                                    className="accent-green-500"
                                    value={lang}
                                    checked={filterLanguages.includes(lang)}
                                    onChange={handleLanguageChange}
                                />
                                {lang}
                            </label>
                        ))}
                    </div>
                </div>
            </div>

            {/* Issues Display */}
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
                {filteredIssues.length > 0 ? (
                    filteredIssues.map((issue) => (
                        <div key={issue.issue_number} className="bg-gray-800 p-6 rounded-lg shadow-md transform hover:scale-105 transition-all duration-300">
                            <h3 className="text-xl font-bold mb-3">
                                <a
                                    href={issue.issue_html_url}
                                    target="_blank"
                                    rel="noopener noreferrer"
                                    className="text-blue-400 hover:underline"
                                >
                                    {issue.issue_title}
                                </a>
                            </h3>
                            <p className="text-gray-400 mb-3">{issue.repo_description}</p>
                            <p>
                                <strong>Repo:</strong>{" "}
                                <a
                                    href={issue.repo_html_url}
                                    target="_blank"
                                    rel="noopener noreferrer"
                                    className="text-green-400 hover:underline"
                                >
                                    {issue.repo_full_name}
                                </a>
                            </p>
                            <p className="mt-2">
                                <strong>Stars:</strong> {issue.repo_stars} |{" "}
                                <strong>Watchers:</strong> {issue.repo_watchers}
                            </p>
                            <p className="mt-2">
                                <strong>Languages:</strong>{" "}
                                <span className="text-gray-300">{issue.languages.join(", ")}</span>
                            </p>
                            <p className="mt-2">
                                <strong>Labels:</strong>{" "}
                                <span className="text-gray-300">{issue.labels.join(", ")}</span>
                            </p>
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
    );
};

export default IssueBoard;
