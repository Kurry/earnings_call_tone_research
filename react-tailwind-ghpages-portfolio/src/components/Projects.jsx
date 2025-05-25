import React from 'react';
import ProjectCard from './ProjectCard.jsx';

const placeholderProjects = [
  {
    id: 1,
    title: 'Portfolio Website V1',
    description: 'A personal portfolio site built with React and Tailwind CSS, showcasing various projects and skills. Features a responsive design.',
    imageUrl: 'https://placekitten.com/400/250', // Example placeholder
    projectUrl: '#',
  },
  {
    id: 2,
    title: 'E-commerce Dashboard',
    description: 'A concept for an e-commerce admin dashboard using modern UI principles. Includes charts and data tables.',
    imageUrl: 'https://placekitten.com/401/250', // Example placeholder
    projectUrl: '#',
  },
  {
    id: 3,
    title: 'Task Management App',
    description: 'A simple task management application to help organize daily to-dos. Built with a focus on clean UI/UX.',
    imageUrl: 'https://placekitten.com/400/251', // Example placeholder
    projectUrl: '#',
  },
];

function Projects() {
  return (
    <section id="projects" className="bg-gray-50 py-16 px-4">
      <div className="container mx-auto">
        <h2 className="text-3xl font-bold text-gray-800 mb-12 text-center">My Projects</h2>
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
          {placeholderProjects.map(project => (
            <ProjectCard
              key={project.id}
              title={project.title}
              description={project.description}
              imageUrl={project.imageUrl}
              projectUrl={project.projectUrl}
            />
          ))}
        </div>
      </div>
    </section>
  );
}

export default Projects;
