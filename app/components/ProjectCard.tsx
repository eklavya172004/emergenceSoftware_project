import React, { FC, CSSProperties } from 'react'
import Image from 'next/image'
import { StaticImageData } from 'next/image'
import { CodeBracketIcon, EyeIcon } from '@heroicons/react/24/outline'
import Link from 'next/link'

interface ProjectCardProps {
  imgURL: string | StaticImageData;
  title: string;
  description: string;
  sourceCode: string;
  preview: string;
}

const ProjectCard: FC<ProjectCardProps> = ({ imgURL, title, description, sourceCode, preview }) => {
  const bgStyle: CSSProperties = {
    backgroundImage: typeof imgURL === 'string' ? `url(${imgURL})` : 'none'
  };

  return (
    <div>
      <div style={bgStyle} className='group h-52 md:h-72 bg-cover relative rounded-t-xl'>
        <div className='overlay items-center justify-center absolute top-0 left-0 w-full h-full bg-[#181818] opacity-0 hidden group-hover:flex group-hover:opacity-80 transition-all duration-500'>
          <Link href={sourceCode} target='_blank' className='h-14 mr-4  w-14 border-2 relative rounded-full border-[#ABD7BE] hover:border-white group/link'>
            <CodeBracketIcon className='h-10 w-10 text-[#ABD7BE]  cursor-pointer absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 group-hover/link:text-white' />
          </Link>

          <Link href={preview} target='_blank' className='h-14 w-14 border-2 relative rounded-full border-[#ABD7BE] hover:border-white group/link'>
            <EyeIcon className='h-10 w-10 text-[#ABD7BE]  cursor-pointer absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 group-hover/link:text-white' />
          </Link>
        </div>
      </div>

      <div className='text-white rounded-b-xl  bg-[#181818] py-6 px-4'>
        <h5 className='text-xl font-semibold mb-2' >{title}</h5>
        <p className='text-[#ADB7BE]'>{description}</p>
      </div>
    </div>
  )
}

export default ProjectCard
