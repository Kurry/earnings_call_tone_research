import React from 'react';

function Header() {
  return (
    <header className="bg-slate-900 text-gray-100 p-4 shadow-md">
      <nav className="container mx-auto flex justify-between items-center">
        <a href="#hero" className="text-2xl font-bold hover:text-sky-400">MyPortfolio</a>
        <ul className="flex space-x-4">
          <li><a href="#hero" className="hover:text-sky-400">Home</a></li>
          <li><a href="#about" className="hover:text-sky-400">About</a></li>
          <li><a href="#projects" className="hover:text-sky-400">Projects</a></li>
        </ul>
      </nav>
    </header>
  );
}

export default Header;
