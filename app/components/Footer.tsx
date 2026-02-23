import React, { FC } from 'react'
import Logo from './Logo'

const Footer: FC = () => {
  return (
    <footer className='footer border border-r-transparent border-l-transparent text-white border-t-[#33353F]'>
      <div className='container flex justify-between items-center p-12 '>
        <Logo />
        <p className='text-slate-600'>© 2025 Eklavya Nath. All rights reserved.</p>
      </div>
    </footer>
  )
}

export default Footer
