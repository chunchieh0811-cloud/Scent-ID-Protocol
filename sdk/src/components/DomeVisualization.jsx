import React, { useRef } from 'react'
import { useFrame } from '@react-three/fiber'
import { OrbitControls, Stars, Html, Line } from '@react-three/drei'

const MOLECULE_DATA = [
  {
    id: 'floral-aurora',
    name: 'Floral Aurora',
    family: 'Floral',
    nodes: [
      [-2, 0, 0],
      [0, 1.2, 0],
      [2, 0, 0],
      [0, -1.5, 1.2],
      [-2.5, -1, -0.8],
    ],
    bonds: [
      [[-2, 0, 0], [0, 1.2, 0]],
      [[0, 1.2, 0], [2, 0, 0]],
      [[0, 1.2, 0], [0, -1.5, 1.2]],
      [[0, 1.2, 0], [-2.5, -1, -0.8]],
    ],
  },
  {
    id: 'oceanic-pulse',
    name: 'Oceanic Pulse',
    family: 'Marine',
    nodes: [
      [-1.8, 0.5, 0],
      [0, 0, 0],
      [1.8, 0.8, 0],
      [0, -1.8, -1.2],
      [2.6, -0.8, 1],
      [-2.4, -1.2, 0.6],
    ],
    bonds: [
      [[-1.8, 0.5, 0], [0, 0, 0]],
      [[0, 0, 0], [1.8, 0.8, 0]],
      [[0, 0, 0], [0, -1.8, -1.2]],
      [[1.8, 0.8, 0], [2.6, -0.8, 1]],
      [[0, 0, 0], [-2.4, -1.2, 0.6]],
    ],
  },
  {
    id: 'woody-harmony',
    name: 'Woody Harmony',
    family: 'Woody',
    nodes: [
      [-2.2, 0, 0],
      [-0.8, 1.6, 0.4],
      [0, 0, 0],
      [2, 0.8, -0.5],
      [1.2, -1.8, 1.2],
      [-1, -1.5, -1],
    ],
    bonds: [
      [[-2.2, 0, 0], [0, 0, 0]],
      [[-0.8, 1.6, 0.4], [0, 0, 0]],
      [[0, 0, 0], [2, 0.8, -0.5]],
      [[0, 0, 0], [1.2, -1.8, 1.2]],
      [[0, 0, 0], [-1, -1.5, -1]],
    ],
  },
]

function Molecule({ data, color, selected, onSelect }) {
  const groupRef = useRef()

  useFrame(() => {
    if (groupRef.current) {
      groupRef.current.rotation.y += 0.002
      if (selected) {
        groupRef.current.rotation.x += 0.001
      }
    }
  })

  return (
    <group
      ref={groupRef}
      onClick={() => onSelect(MOLECULE_DATA.indexOf(data))}
      style={{ cursor: 'pointer' }}
    >
      {/* Bonds */}
      {data.bonds.map((bond, i) => (
        <Line
          key={`bond-${i}`}
          points={bond}
          lineWidth={selected ? 2 : 1}
          color={color}
          transparent
          opacity={0.8}
        />
      ))}

      {/* Nodes */}
      {data.nodes.map((pos, i) => (
        <mesh key={`node-${i}`} position={pos}>
          <sphereGeometry args={[selected ? 0.4 : 0.25, 32, 32]} />
          <meshStandardMaterial
            color={color}
            emissive={color}
            emissiveIntensity={selected ? 1.2 : 0.6}
            metalness={0.8}
            roughness={0.2}
          />
        </mesh>
      ))}

      {/* Label */}
      {selected && (
        <Html position={[0, 3, 0]} center>
          <div className="bg-black/80 backdrop-blur-md text-scent-accent px-4 py-2 rounded-lg text-sm font-semibold whitespace-nowrap">
            {data.name}
          </div>
        </Html>
      )}
    </group>
  )
}

export default function DomeVisualization({ moleculeIndex = 0, rgb, alpha, onMoleculeSelect }) {
  const color = `rgb(${rgb.join(',')})`

  return (
    <>
      <Stars radius={100} depth={50} count={5000} factor={4} />
      
      {/* Background gradient lighting */}
      <mesh position={[0, 0, -20]} scale={[100, 100, 1]}>
        <planeGeometry />
        <meshBasicMaterial color="#050710" />
      </mesh>

      {/* Rotating dome container */}
      {MOLECULE_DATA.map((molecule, idx) => (
        <Molecule
          key={molecule.id}
          data={molecule}
          color={color}
          selected={idx === moleculeIndex}
          onSelect={onMoleculeSelect}
        />
      ))}

      {/* Orbital grid */}
      <OrbitControls
        enablePan={false}
        enableZoom={true}
        enableRotate={true}
        autoRotate={true}
        autoRotateSpeed={0.5}
      />
    </>
  )
}
