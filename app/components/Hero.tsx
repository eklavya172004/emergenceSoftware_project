'use client'
import Image from 'next/image'
import Link from 'next/link'
import React, { FC } from 'react'
import { TypeAnimation } from 'react-type-animation';
 
const Hero: FC = () => {
  return (
    <section className="">
      <div className='grid grid-cols-1 sm:grid-cols-12'> 
        <div className='col-span-7 place-self-center text-center sm:text-left'>

          <h1 className='text-white sm:text-5xl  mb-4 text-4xl lg:text-6xl font-extrabold'>
            <span className='text-transparent bg-clip-text bg-gradient-to-r  from-blue-500 via-purple-500 to-pink-500 '>
              Hello, I am{" "}
            </span>  
            <br />
            <TypeAnimation
              sequence={[
                'Eklavya Nath',
                1000,
                'Web Developer',
                1000,
                'Problem Solver',
                1000,
                'Generative Ai',
                1000
              ]}
              wrapper="span"
              speed={50}
              repeat={Infinity}
            /> 
          </h1>
          <p className='text-[#ADB7BE] sm:text-lg  text-base lg:text-xl mb-6'>
            Building intelligent web applications with cutting-edge technologies. Full-stack developer passionate about AI integration, scalable architectures, and solving complex problems with code.
          </p>
          <div>
            <Link
              href="/"
              className="px-6 inline-block py-3 w-full sm:w-fit rounded-full mr-4 bg-gradient-to-br from-blue-500 via-purple-500 to-pink-500  text-white"
            >
              Hire Me
            </Link>
            <a
              href="/resume1.pdf"
              download="Eklavya_Nath_Resume.pdf"
              className="px-1 inline-block py-1 w-full sm:w-fit   rounded-full bg-gradient-to-br from-blue-500 via-purple-500 to-pink-500  text-white mt-3"
            >
              <span className="block bg-[#121212] hover:bg-slate-800 rounded-full px-5 py-2">
                Download CV
              </span>
            </a>
          </div>
        </div>

        <div className='col-span-5 place-self-center mt-4 lg:mt-0 '>
          <div className="rounded-full bg-[#181818] w-[250px] h-[250px] lg:w-[400px] lg:h-[400px] relative">
            <Image src="/images/hero-image-01.png" className="absolute transform -translate-x-1/2 -translate-y-1/2 top-1/2 left-1/2" alt='hero-image' width={400} height={400}/>
          </div>
        </div>
      </div>
    </section>
  )
}

export default Hero
