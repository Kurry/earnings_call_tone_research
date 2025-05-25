import React from 'react';

function Footer() {
  return (
    <footer className="bg-slate-900 text-gray-300 py-8 px-4 text-center">
      <div className="container mx-auto">
        <p>&copy; {new Date().getFullYear()} Your Name Here. Built with React & Tailwind CSS.</p>
        <p className="mt-2">
          <a href="https://github.com/yourusername" target="_blank" rel="noopener noreferrer" className="hover:text-sky-400">
            GitHub
          </a>
          {/* Add more social links if desired */}
        </p>
      </div>
    </footer>
  );
}

export default Footer;
