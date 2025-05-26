import React from 'react';

function Hero() {
  return (
    <section id="hero" className="bg-slate-800 text-gray-100 py-20 px-4 text-center">
      <div className="container mx-auto">
        <h1 className="text-5xl font-bold mb-4">Welcome to My Awesome Portfolio</h1>
        <p className="text-xl mb-8">Discover my projects and skills.</p>
        <a
          href="#projects"
          className="bg-sky-500 hover:bg-sky-600 text-white font-bold py-3 px-6 rounded-lg text-lg"
        >
          View Projects
        </a>
      </div>
    </section>
  );
}

export default Hero;
