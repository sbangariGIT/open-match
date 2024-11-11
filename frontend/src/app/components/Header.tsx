import React from 'react';

type HeaderProps = {
  appName: string;
};

const Header: React.FC<HeaderProps> = ({ appName }) => {
  return (
    <header style={headerStyle}>
        <div className='text-1xl md:text-4xl font-extrabold bg-gradient-to-r from-purple-400 to-blue-600 text-transparent bg-clip-text mb-3'>
          <h1>{appName}</h1>
        </div>
    </header>
  );
};

const headerStyle: React.CSSProperties = {
  color: '#ffffff',
  padding: '1rem',
  textAlign: 'left',
  fontSize: '2rem',
  fontFamily: 'Montserrat, sans-serif',
};

export default Header;
