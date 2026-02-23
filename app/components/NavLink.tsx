import Link from 'next/link'
import React, { FC } from 'react'

interface NavLinkProps {
  href: string;
  title: string;
}

const NavLink: FC<NavLinkProps> = ({ href, title }) => {
  return (
    <Link className='block py-2 pl-3 pr-4 text-[#ADB7BE]  sm:text-xl rounded md:p-0 hover:text-white' 
      href={href}>
      {title}
    </Link>
  )
}

export default NavLink
