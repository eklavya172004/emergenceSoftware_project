'use client'
import React, { FC } from 'react'
import NavLink from './NavLink'

interface Link {
  path: string;
  title: string;
}

interface MenuOverLayProps {
  links: Link[];
}

const MenuOverLay: FC<MenuOverLayProps> = ({ links }) => {
  return (
    <div>
      <ul className='flex flex-col py-4 items-center'>
        {links.map((link, index) => (
          <li key={index}>
            <NavLink href={link.path} title={link.title} />
          </li>
        ))}
      </ul>
    </div>
  )
}

export default MenuOverLay
