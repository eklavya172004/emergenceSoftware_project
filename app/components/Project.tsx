'use client'
import React, { FC, useState } from 'react'
import { projects } from '../constants'
import ProjectCard from './ProjectCard'
import ProjectTag from './ProjectTag'
import { styles } from '../data/style'

interface ProjectType {
  id: number;
  title: string;
  description: string;
  tags: string[];
  image: string;
  source_code_link: string;
  preview: string;
}

const Project: FC = () => {
  const [tag, setTag] = useState<string>("All");

  const filterProjects = (selectedTag: string): void => {
    setTag(selectedTag);
  }
  
  const taggedProjects = (projects as ProjectType[]).filter((project) => {
    if (tag === "All") return true;
    return project.tags.includes(tag);
  });

  return (
    <div id="projects">
      <h2 className='text-amber-50  text-[32px] font-bold mt-24 mb-12'>
        <h2 className={styles.sectionHeadText}>
          My Projects
        </h2>
      </h2>
      
      <div className='text-white flex flex-row justify-center items-center gap-2 mb-5 py-6'>
        <ProjectTag onClick={filterProjects} name="All" isSelected={tag === "All"} />
        <ProjectTag onClick={filterProjects} name="Frontend" isSelected={tag === "Frontend"} />
        <ProjectTag onClick={filterProjects} name="Fullstack" isSelected={tag === "Fullstack"} />
      </div>

      <div className='grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-8 md:gap-12'>
        {
          taggedProjects.map((project) => (
            <ProjectCard 
              key={project.id} 
              title={project.title} 
              description={project.description} 
              imgURL={project.image} 
              sourceCode={project.source_code_link} 
              preview={project.preview}
            />
          ))
        }
      </div>
    </div>
  )
}

export default Project
