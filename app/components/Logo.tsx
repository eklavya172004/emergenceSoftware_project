'use client';

import React, { FC } from 'react';

const Logo: FC = () => {
  return (
    <svg
      width="50"
      height="50"
      viewBox="0 0 50 50"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
      className="hover:scale-110 transition-transform duration-300"
    >
      <defs>
        <linearGradient id="logoGradient" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stopColor="#3B82F6" />
          <stop offset="50%" stopColor="#A855F7" />
          <stop offset="100%" stopColor="#EC4899" />
        </linearGradient>
      </defs>

      {/* Background Circle */}
      <circle cx="25" cy="25" r="24" stroke="url(#logoGradient)" strokeWidth="2" fill="none" />

      {/* Inner Circle */}
      <circle cx="25" cy="25" r="20" fill="rgba(18, 18, 18, 0.8)" />

      {/* Letter "E" */}
      <text
        x="16"
        y="32"
        fontSize="20"
        fontWeight="700"
        fontFamily="Arial, sans-serif"
        fill="url(#logoGradient)"
      >
        E
      </text>

      {/* Letter "N" */}
      <text
        x="28"
        y="32"
        fontSize="20"
        fontWeight="700"
        fontFamily="Arial, sans-serif"
        fill="url(#logoGradient)"
      >
        N
      </text>

      {/* Accent line */}
      <line x1="18" y1="38" x2="32" y2="38" stroke="url(#logoGradient)" strokeWidth="1.5" strokeLinecap="round" />
    </svg>
  );
};

export default Logo;
