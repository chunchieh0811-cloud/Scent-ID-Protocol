import React, { useState, useCallback } from 'react'
import { Canvas } from '@react-three/fiber'
import DomeVisualization from './components/DomeVisualization'
import ControlPanel from './components/ControlPanel'
import DigitalSeal from './components/DigitalSeal'
import Header from './components/Header'
import useColorStore from './store/colorStore'
import useSIDStore from './store/sidStore'

export default function App() {
  const [selectedMolecule, setSelectedMolecule] = useState(0)
  const [showSeal, setShowSeal] = useState(false)
  const {
    rgb, cmyk, hsv, alpha,
    setRGB, setCMYK, setHSV, setAlpha
  } = useColorStore()
  const { sid, updateSID, seal } = useSIDStore()

  const handleGenerateSeal = useCallback(() => {
    setShowSeal(true)
  }, [])

  const handleColorChange = useCallback((rgb) => {
    setRGB(rgb)
    updateSID(rgb)
  }, [setRGB, updateSID])

  return (
    <div className="w-full h-screen bg-scent-darker flex flex-col">
      <Header />

      <div className="flex-1 flex gap-4 p-4 overflow-hidden">
        {/* 3D Canvas Area */}
        <div className="flex-1 glass rounded-2xl overflow-hidden">
          <Canvas
            camera={{ position: [0, 0, 12], fov: 50 }}
            className="w-full h-full"
          >
            <ambientLight intensity={0.6} />
            <pointLight position={[10, 10, 10]} intensity={1.5} />
            <pointLight position={[-10, -10, 10]} intensity={0.8} color="#00ff88" />
            <DomeVisualization
              moleculeIndex={selectedMolecule}
              rgb={rgb}
              alpha={alpha}
              onMoleculeSelect={setSelectedMolecule}
            />
          </Canvas>
        </div>

        {/* Control Panel */}
        <div className="w-80 flex flex-col gap-4 overflow-y-auto pr-2">
          <ControlPanel
            rgb={rgb}
            cmyk={cmyk}
            hsv={hsv}
            alpha={alpha}
            sid={sid}
            onRGBChange={handleColorChange}
            onCMYKChange={setCMYK}
            onHSVChange={setHSV}
            onAlphaChange={setAlpha}
            onGenerateSeal={handleGenerateSeal}
          />
        </div>
      </div>

      {/* Digital Seal Modal */}
      {showSeal && (
        <DigitalSeal
          sid={sid}
          seal={seal}
          rgb={rgb}
          cmyk={cmyk}
          onClose={() => setShowSeal(false)}
        />
      )}
    </div>
  )
}
