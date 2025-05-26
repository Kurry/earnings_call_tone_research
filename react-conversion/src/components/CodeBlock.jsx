import React from 'react';

// Basic placeholder. For actual syntax highlighting, a library like react-syntax-highlighter would be used.
const CodeBlock = ({ language, children }) => {
  return (
    <pre className="bg-gray-100 p-4 rounded-md overflow-x-auto">
      <code className={`language-${language}`}>
        {children}
      </code>
    </pre>
  );
};
export default CodeBlock;
