import React, { useState } from 'react'
import * as Slider from '@radix-ui/react-slider'
import { ChevronDown } from 'lucide-react'

function ColorSection({ title, values, onChange, labels, maxValues, step = 1 }) {
  return (
    <div className="glass rounded-xl p-4">
      <h3 className="text-sm font-semibold text-scent-accent mb-4">{title}</h3>
      <div className="space-y-4">
        {values.map((value, idx) => (
          <div key={idx}>
            <div className="flex items-center justify-between mb-2">
              <label className="text-xs text-gray-400">{labels[idx]}</label>
              <span className="text-sm font-mono text-white">
                {value}{title === 'CMYK' ? '%' : title === 'HSV' && idx === 1 ? '%' : title === 'HSV' && idx === 2 ? '%' : ''}
              </span>
            </div>
            <Slider.Root
              value={[value]}
              onValueChange={(v) => {
                const newValues = [...values]
                newValues[idx] = v[0]
                onChange(newValues)
              }}
              max={maxValues[idx]}
              step={step}
              className="w-full h-1 bg-white/10 rounded-full relative flex items-center cursor-pointer"
            >
              <Slider.Track className="relative flex-grow h-1 bg-white/10 rounded-full">
                <Slider.Range className="absolute h-1 bg-gradient-to-r from-scent-accent to-scent-secondary rounded-full" />
              </Slider.Track>
              <Slider.Thumb className="w-4 h-4 bg-white rounded-full shadow-lg shadow-scent-accent/50 hover:shadow-xl transition-all" />
            </Slider.Root>
          </div>
        ))}
      </div>
    </div>
  )
}

function PreviewBox({ rgb, cmyk, alpha }) {
  const color = `rgba(${rgb.join(',')}, ${alpha / 255})`
  return (
    <div className="glass rounded-xl p-4">
      <h3 className="text-sm font-semibold text-scent-accent mb-3">Preview</h3>
      <div className="space-y-3">
        <div
          className="w-full h-32 rounded-lg border border-white/20 shadow-lg"
          style={{ backgroundColor: color }}
        />
        <div className="grid grid-cols-2 gap-2 text-xs">
          <div className="bg-black/40 rounded p-2">
            <p className="text-gray-400">RGB</p>
            <p className="font-mono text-white">#{rgb.map(v => v.toString(16).padStart(2, '0')).join('').toUpperCase()}</p>
          </div>
          <div className="bg-black/40 rounded p-2">
            <p className="text-gray-400">Alpha</p>
            <p className="font-mono text-white">{Math.round((alpha / 255) * 100)}%</p>
          </div>
        </div>
      </div>
    </div>
  )
}

function SIDDisplay({ sid }) {
  const [copied, setCopied] = useState(false)

  const handleCopy = () => {
    navigator.clipboard.writeText(sid)
    setCopied(true)
    setTimeout(() => setCopied(false), 2000)
  }

  return (
    <div className="glass rounded-xl p-4">
      <h3 className="text-sm font-semibold text-scent-accent mb-3">SID-18</h3>
      <div
        onClick={handleCopy}
        className="w-full px-3 py-3 bg-black/40 border border-scent-accent/30 rounded-lg font-mono text-sm text-white hover:border-scent-accent/60 cursor-pointer transition-colors flex items-center justify-between"
      >
        <span>{sid}</span>
        <span className="text-xs text-gray-500">
          {copied ? '✓ Copied' : 'Copy'}
        </span>
      </div>
    </div>
  )
}

export default function ControlPanel({
  rgb, cmyk, hsv, alpha,
  onRGBChange, onCMYKChange, onHSVChange, onAlphaChange,
  sid, onGenerateSeal
}) {
  const [expandedSection, setExpandedSection] = useState('rgb')

  const sections = [
    {
      id: 'rgb',
      title: 'RGB',
      component: (
        <ColorSection
          title="RGB"
          values={rgb}
          onChange={onRGBChange}
          labels={['Red', 'Green', 'Blue']}
          maxValues={[255, 255, 255]}
        />
      ),
    },
    {
      id: 'cmyk',
      title: 'CMYK',
      component: (
        <ColorSection
          title="CMYK"
          values={cmyk}
          onChange={onCMYKChange}
          labels={['Cyan', 'Magenta', 'Yellow', 'Black']}
          maxValues={[100, 100, 100, 100]}
        />
      ),
    },
    {
      id: 'hsv',
      title: 'HSV',
      component: (
        <ColorSection
          title="HSV"
          values={hsv}
          onChange={onHSVChange}
          labels={['Hue', 'Saturation', 'Value']}
          maxValues={[360, 100, 100]}
        />
      ),
    },
  ]

  return (
    <div className="space-y-4">
      {/* Color Mode Tabs */}
      <div className="glass rounded-xl p-1 flex gap-2">
        {sections.map((section) => (
          <button
            key={section.id}
            onClick={() => setExpandedSection(section.id)}
            className={`flex-1 py-2 rounded-lg text-xs font-semibold transition-all ${
              expandedSection === section.id
                ? 'bg-scent-accent/20 text-scent-accent border border-scent-accent/50'
                : 'text-gray-400 hover:text-white'
            }`}
          >
            {section.title}
          </button>
        ))}
      </div>

      {/* Active Section */}
      {sections.find(s => s.id === expandedSection)?.component}

      {/* Alpha/Transparency */}
      <div className="glass rounded-xl p-4">
        <h3 className="text-sm font-semibold text-scent-accent mb-4">Transparency</h3>
        <div>
          <div className="flex items-center justify-between mb-2">
            <label className="text-xs text-gray-400">Alpha Channel</label>
            <span className="text-sm font-mono text-white">{alpha} / 255</span>
          </div>
          <Slider.Root
            value={[alpha]}
            onValueChange={(v) => onAlphaChange(v[0])}
            max={255}
            step={1}
            className="w-full h-1 bg-white/10 rounded-full relative flex items-center"
          >
            <Slider.Track className="relative flex-grow h-1 bg-white/10 rounded-full">
              <Slider.Range className="absolute h-1 bg-gradient-to-r from-scent-accent to-scent-secondary rounded-full" />
            </Slider.Track>
            <Slider.Thumb className="w-4 h-4 bg-white rounded-full shadow-lg shadow-scent-accent/50" />
          </Slider.Root>
        </div>
      </div>

      {/* Preview */}
      <PreviewBox rgb={rgb} cmyk={cmyk} alpha={alpha} />

      {/* SID Display */}
      <SIDDisplay sid={sid} />

      {/* Generate Seal Button */}
      <button
        onClick={onGenerateSeal}
        className="w-full px-4 py-3 rounded-xl bg-gradient-to-r from-scent-accent to-scent-secondary text-scent-darker font-semibold hover:shadow-lg hover:shadow-scent-accent/50 transition-all active:scale-95"
      >
        🔐 Generate Digital Seal
      </button>

      {/* Info */}
      <div className="glass rounded-xl p-3">
        <p className="text-xs text-gray-400 leading-relaxed">
          Generate cryptographically signed digital seals for your scent designs. Each seal includes SHA-256 fingerprint, timestamp, and license information.
        </p>
      </div>
    </div>
  )
}
