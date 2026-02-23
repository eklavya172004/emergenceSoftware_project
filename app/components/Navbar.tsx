'use client'
import Link from 'next/link'
import React, { FC, useState } from 'react'
import NavLink from './NavLink'
import { Bars3Icon, XMarkIcon } from '@heroicons/react/24/solid'
import MenuOverLay from './MenuOverLay'
import Logo from './Logo'

interface NavLink {
  title: string;
  path: string;
}

const navlinks: NavLink[] = [
  {
    title: "About",
    path: "#about",
  },
  {
    title: "Projects",
    path: "#projects",
  },
  {
    title: "Contact",
    path: "#contact",
  },
  {
    title: "Chat",
    path: "/chat",
  }
]

const Navbar: FC = () => {
  const [navbarOpen, setnavbarOpen] = useState<boolean>(false);

  return (
    <nav className='fixed top-0 left-0 right-0 z-10  backdrop-blur-sm'>
      <div className='flex flex-wrap items-center justify-between mx-auto px-4 py-2'>
        <Link href={"/"} className='flex items-center justify-center'>
          <Logo />
        </Link>

        <div className='mobile-menu block md:hidden'>
          {
            !navbarOpen ? (
              <button onClick={() => setnavbarOpen(true)} title="Open menu" className='text-slate-200 items-center px-3 py-2 border rounded border-slate-200 hover:text-white hover:border-white'>
                <Bars3Icon className="h-5 w-5"/>
              </button>
            ) : (
              <button onClick={() => setnavbarOpen(false)} title="Close menu" className='text-slate-200 items-center px-3 py-2 border rounded border-slate-200 hover:text-white hover:border-white'>
                <XMarkIcon className="h-5 w-5"/>
              </button>
            )
          }
        </div>

        <div className='menu  hidden md:block md:w-auto' id='navbar'>
          <ul className='flex p-4 md:p-0 sm:flex-row md:space-x-8 mt-0'>        
            {navlinks.map((link, index) => (
              <li key={index}>
                <NavLink href={link.path} title={link.title} />
              </li>
            ))}
          </ul>
        </div>
      </div>
      {
        navbarOpen ? <MenuOverLay links={navlinks} /> : null
      }
    </nav>
  )
}

export default Navbar
