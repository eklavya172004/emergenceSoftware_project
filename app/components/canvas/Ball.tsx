'use client'
import React, { Suspense, useRef, useState, FC } from "react";
import { Canvas, useFrame, ThreeEvent } from "@react-three/fiber";
import {
  Decal,
  Float,
  OrbitControls,
  Preload,
  useTexture,
} from "@react-three/drei";
import CanvasLoader from "../Loader";
import { Mesh } from "three";

interface BallProps {
  imgUrl: string;
}

const Ball: FC<BallProps> = ({ imgUrl }) => {
  const [decal] = useTexture([imgUrl]);
  const meshRef = useRef<Mesh>(null);
  const [hovered, setHovered] = useState<boolean>(false);

  useFrame((state, delta) => {
    if (meshRef.current) {
      if (hovered) {
        meshRef.current.rotation.x += delta * 2;
        meshRef.current.rotation.y += delta * 1.5;
      } else {
        meshRef.current.rotation.x *= 0.95;
        meshRef.current.rotation.y *= 0.95;
      }
    }
  });

  const handlePointerOver = (e: ThreeEvent<PointerEvent>): void => {
    e.stopPropagation();
    setHovered(true);
  };

  const handlePointerOut = (e: ThreeEvent<PointerEvent>): void => {
    e.stopPropagation();
    setHovered(false);
  };

  return (
    <Float speed={1.75} rotationIntensity={1} floatIntensity={2}>
      <ambientLight intensity={0.25} />
      <directionalLight position={[0, 0, 0.05]} />
      <mesh 
        ref={meshRef}
        castShadow 
        receiveShadow 
        scale={hovered ? 3 : 2.75}
        onPointerOver={handlePointerOver}
        onPointerOut={handlePointerOut}
      >
        <icosahedronGeometry args={[1, 1]} />
        <meshStandardMaterial
          color='#fff8eb'
          polygonOffset
          polygonOffsetFactor={-5}
          flatShading
        />
        <Decal
          position={[0, 0, 1]}
          rotation={[2 * Math.PI, 0, 6.25]}
          scale={1}
          map={decal}
        />
      </mesh>
    </Float>
  );
};

interface BallCanvasProps {
  icon: string;
}

const BallCanvas: FC<BallCanvasProps> = ({ icon }) => {
  return (
    <Canvas
      frameloop='always'
      dpr={[1, 2]}
      gl={{ preserveDrawingBuffer: true }}
    >
      <Suspense fallback={<CanvasLoader />}>
        <OrbitControls 
          enableZoom={false} 
          enablePan={false}
          enableRotate={false}
        />
        <Ball imgUrl={icon} />
      </Suspense>
      <Preload all />
    </Canvas>
  );
};

export default BallCanvas;
