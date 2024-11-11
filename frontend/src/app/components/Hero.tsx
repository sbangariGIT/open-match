'use client';

import React from 'react';


const Hero: React.FC = () => {

  return (
    <div className="max-w-2xl">
      <h1 className="text-5xl md:text-6xl font-extrabold bg-gradient-to-r from-blue-400 to-purple-600 text-transparent bg-clip-text mb-6">
        Unlock Your Potential in Open Source
      </h1>
      <p className="text-lg md:text-xl text-gray-300 mb-8">
        Upload your resume and choose your interests to discover open-source issues tailored to your skills. Start contributing to projects that matter.
      </p>
    </div>
  );
};

export default Hero;
