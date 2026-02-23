'use client'
import React, { FC, CSSProperties } from 'react';
import { Html, useProgress } from '@react-three/drei';

const Loader: FC = () => {
  const { progress } = useProgress();

  const pStyle: CSSProperties = {
    fontSize: 14,
    color: '#f1f1f1',
    fontWeight: 800,
    marginTop: 40
  };

  return (
    <Html>
      <span className="canvas-load"></span>
      <p style={pStyle}>
        {progress.toFixed(2)}%
      </p>
    </Html>
  );
};

export default Loader;
