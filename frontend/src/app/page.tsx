"use client"; // Add this line at the top of the file to mark the component as a Client Component

import Header from "@/app/components/Header";
import Hero from "@/app/components/Hero";
import Dashboard from "@/app/components/Dashboard";
import React, { useRef } from 'react';
export default function Home() {
  // Create a reference to the "dashboard" section
  const dashboardRef = useRef<HTMLElement | null>(null);

  const handleClick = () => {
    if (dashboardRef.current) {
      dashboardRef.current.scrollIntoView({ behavior: 'smooth' });
    }
  };
  return (
    <>
      <Header appName="OPEN MATCH" />
      <div className="grid grid-rows-[20px_1fr_20px] p-8 pb-20 gap-16 sm:p-20 font-[family-name:var(--font-geist-sans)]">
        <main className="flex flex-col gap-8 row-start-2 items-center sm:items-start">
          <Hero />
          <button
            className="px-6 py-3 bg-blue-600 hover:bg-blue-700 text-white font-semibold rounded-md shadow-lg transition duration-300"
            onClick={handleClick}
          >
            Get Started
          </button>
        </main>
        <div className="row-start-2 w-full mt-8">
          <img src={'hero.svg'} alt="Hero" className="w-full h-auto" />
        </div>
      </div>
      <section className="dashboard" ref={dashboardRef}>
        <Dashboard />
      </section>
      <footer className="row-start-3 flex gap-6 p-20 flex-wrap items-center justify-center">
      </footer>
    </>
  );
}
