import React from 'react';
import { Link } from 'react-router-dom';

const Header = () => {
  return (
    <header className="bg-gray-800 text-white p-4">
      <nav className="container mx-auto flex justify-between">
        <Link to="/" className="text-xl font-bold">Earnings Call Research</Link>
        <ul className="flex space-x-4">
          <li><Link to="/" className="hover:text-gray-300">Home</Link></li>
          <li><Link to="/methodology" className="hover:text-gray-300">Methodology</Link></li>
          <li><Link to="/results" className="hover:text-gray-300">Results</Link></li>
          <li><Link to="/technical" className="hover:text-gray-300">Technical</Link></li>
        </ul>
      </nav>
    </header>
  );
};
export default Header;
