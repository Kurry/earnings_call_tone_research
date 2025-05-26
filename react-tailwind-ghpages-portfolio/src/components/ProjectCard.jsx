import React from 'react';

function ProjectCard({ title, description, imageUrl, projectUrl }) {
  return (
    <div className="bg-gray-100 rounded-lg shadow-lg overflow-hidden transform hover:scale-105 transition-transform duration-300">
      {imageUrl ? (
        <img className="w-full h-48 object-cover" src={imageUrl} alt={title || 'Project image'} />
      ) : (
        <div className="w-full h-48 bg-gray-300 flex items-center justify-center">
          <span className="text-gray-500">Placeholder Image</span>
        </div>
      )}
      <div className="p-6">
        <h3 className="text-2xl font-semibold text-gray-800 mb-2">{title || 'Project Title Placeholder'}</h3>
        <p className="text-gray-700 mb-4">{description || 'Project description placeholder detailing the features and technologies used.'}</p>
        {projectUrl && (
          <a
            href={projectUrl}
            target="_blank"
            rel="noopener noreferrer"
            className="inline-block bg-sky-500 hover:bg-sky-600 text-white font-semibold py-2 px-4 rounded"
          >
            View Project
          </a>
        )}
      </div>
    </div>
  );
}

export default ProjectCard;
