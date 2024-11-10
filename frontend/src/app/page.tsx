"use client"; // Add this line at the top of the file to mark the component as a Client Component

import Header from "@/components/Header";
import Hero from "@/components/Hero";

export default function Home() {
   // Create a reference to the "dashboard" section

   const handleClick = () => {
     console.log('Get Started button clicked!');
     // move to dashboard section
   };

  return (
    <>
      <Header appName="OPEN MATCH" />
      <div className="grid grid-rows-[20px_1fr_20px] items-center justify-items-center p-8 pb-20 gap-16 sm:p-20 font-[family-name:var(--font-geist-sans)]">
        <main className="flex flex-col gap-8 row-start-2 items-center sm:items-start">
          <Hero />
          <button
            className="px-6 py-3 bg-blue-600 hover:bg-blue-700 text-white font-semibold rounded-md shadow-lg transition duration-300"
            onClick={handleClick}  // Moved logic into a separate function for clarity
          >
            Get Started
          </button>
        </main>
        <footer className="row-start-3 flex gap-6 flex-wrap items-center justify-center">
          {/* Footer content goes here */}
        </footer>
      </div>
    </>
  );
}
