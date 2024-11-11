import React from "react";
import { IssueCard } from "../models/IssueCard";

type IssueMatcherProps = {
  issueCards: IssueCard[];
  isLoading: boolean;
  isError: boolean;
};

const IssueMatcher: React.FC<IssueMatcherProps> = ({ issueCards, isLoading, isError }) => {
  if (isError) {
    return (
      <div>
        Error
      </div>
    )
  }

  if (isLoading) {
    return (
      <div>
        Loading
      </div>
    )
  }

  if (issueCards.length > 0) {
    return (
      <div>
        We have Issues to show
      </div>
    );
  }

  return (
    <div className="flex justify-center items-center">
      <div className="border-2 border-white rounded-lg text-center bg-black min-h-[800px] w-[950px]">
        <img src="welcome.svg" alt="Welcome" className="mx-auto h-40 w-auto m-40" />
        <p className="text-white text-xl sm:text-2xl leading-relaxed p-2">
          Let us get to know you! We’d love to learn more about your interests, the projects you’ve worked on, and what drives your passion.
          <br></br>
          <br></br>
          This will help us better understand how we can collaborate and match you with opportunities that align with your goals and aspirations.
        </p>
      </div>
    </div>

  )
}

export default IssueMatcher;