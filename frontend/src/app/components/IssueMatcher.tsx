import React from "react";
import { IssueCard } from "../models/IssueCard";
import IssueCardContainer from "./IssueCard";

type IssueMatcherProps = {
  issueCards: IssueCard[];
  isLoading: boolean;
  isError: boolean;
};

const IssueMatcher: React.FC<IssueMatcherProps> = ({ issueCards, isLoading, isError }) => {
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
    <h2 className="text-white text-3xl font-bold mb-4">Hold Tight, We’re Matching You with the Perfect Opportunity!</h2>
    <p className="text-white text-lg mb-6">Exploring open-source issues that align with your skills and passions...</p>
    <p className="text-white text-xl font-semibold animate-pulse">This will only take a moment!</p>
  </div>
  </div>

    )
  }

  if (issueCards.length > 0) {
    return (
      <div>
        <h1 className="text-5xl font-bold text-center mt-10 p-10">Results</h1>
      <div className="flex justify-center items-center">
      <div className="border-2 border-white rounded-lg text-center bg-black min-h-[800px] min-w-[900px]">
      {issueCards.map((issueCard, index) => (
        <IssueCardContainer key={index} index={index} issueCard={issueCard} />
      ))}
      </div>
    </div>
    </div>
    );
  }

  return (
    <div className="flex justify-center items-center">
    </div>

  )
}

export default IssueMatcher;