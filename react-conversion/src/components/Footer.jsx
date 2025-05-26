import React from 'react';

const Footer = () => {
  const currentYear = new Date().getFullYear();
  return (
    <footer className="bg-gray-700 text-white p-4 text-center">
      <p>&copy; {currentYear} Kurry Tran. All rights reserved.</p>
      {/* Replicate 'Last updated' if desired, could be dynamic or static */}
    </footer>
  );
};
export default Footer;
