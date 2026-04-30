import React, { useState, useEffect } from 'react'
import { X, CheckCircle, Download, Share2, Lock } from 'lucide-react'
import useSIDStore from '../store/sidStore'

export default function DigitalSeal({ sid, rgb, cmyk, onClose }) {
  const [sealData, setSealData] = useState(null)
  const [loading, setLoading] = useState(true)
  const { generateSeal } = useSIDStore()

  useEffect(() => {
    generateSeal(rgb, { cmyk }).then(setSealData).finally(() => setLoading(false))
  }, [rgb, cmyk, generateSeal])

  if (loading || !sealData) {
    return (
      <div className="fixed inset-0 bg-black/50 backdrop-blur-md flex items-center justify-center z-50">
        <div className="bg-scent-darker border border-scent-accent/50 rounded-2xl p-8 max-w-md w-full">
          <div className="animate-spin w-8 h-8 border-2 border-scent-accent border-t-transparent rounded-full mx-auto" />
          <p className="text-center text-gray-400 mt-4">Generating digital seal...</p>
        </div>
      </div>
    )
  }

  const hexColor = rgb.map(v => v.toString(16).padStart(2, '0')).join('').toUpperCase()

  return (
    <div className="fixed inset-0 bg-black/70 backdrop-blur-md flex items-center justify-center z-50 p-4">
      <div className="glass rounded-2xl max-w-2xl w-full max-h-[90vh] overflow-y-auto">
        <div className="sticky top-0 glass-dark border-b border-scent-accent/30 flex items-center justify-between p-6">
          <div className="flex items-center gap-3">
            <Lock className="w-5 h-5 text-scent-accent" />
            <h2 className="text-2xl font-bold">Digital Seal</h2>
          </div>
          <button
            onClick={onClose}
            className="p-2 hover:bg-white/10 rounded-lg transition-colors"
          >
            <X className="w-6 h-6" />
          </button>
        </div>

        <div className="p-8 space-y-8">
          {/* Verification Status */}
          <div className="flex items-center gap-4">
            <div className="w-12 h-12 rounded-full bg-green-500/20 border border-green-500/50 flex items-center justify-center">
              <CheckCircle className="w-6 h-6 text-green-400" />
            </div>
            <div>
              <p className="font-semibold text-white">Cryptographically Verified</p>
              <p className="text-sm text-gray-400">This design has been securely sealed and registered</p>
            </div>
          </div>

          {/* Seal Details Grid */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {/* SID-18 */}
            <div className="bg-black/40 rounded-xl p-4 border border-scent-accent/30">
              <p className="text-xs text-gray-400 mb-2">SID-18</p>
              <p className="font-mono text-lg text-scent-accent mb-3 break-all">{sealData.sid}</p>
              <button className="text-xs text-gray-400 hover:text-white transition-colors">
                📋 Copy
              </button>
            </div>

            {/* License ID */}
            <div className="bg-black/40 rounded-xl p-4 border border-scent-secondary/30">
              <p className="text-xs text-gray-400 mb-2">License ID</p>
              <p className="font-mono text-lg text-scent-secondary mb-3 break-all">{sealData.licenseId}</p>
              <button className="text-xs text-gray-400 hover:text-white transition-colors">
                📋 Copy
              </button>
            </div>

            {/* Fingerprint */}
            <div className="bg-black/40 rounded-xl p-4 border border-white/10 md:col-span-2">
              <p className="text-xs text-gray-400 mb-2">SHA-256 Fingerprint</p>
              <p className="font-mono text-xs text-gray-300 break-all mb-3 select-all">
                {sealData.fingerprint}
              </p>
              <button className="text-xs text-gray-400 hover:text-white transition-colors">
                📋 Copy
              </button>
            </div>

            {/* Timestamp */}
            <div className="bg-black/40 rounded-xl p-4 border border-white/10">
              <p className="text-xs text-gray-400 mb-2">Timestamp</p>
              <p className="text-sm text-white">{new Date(sealData.timestamp).toLocaleString()}</p>
            </div>

            {/* Creator ID */}
            <div className="bg-black/40 rounded-xl p-4 border border-white/10">
              <p className="text-xs text-gray-400 mb-2">Creator</p>
              <p className="text-sm text-white">{sealData.creatorId}</p>
            </div>
          </div>

          {/* Color Information */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="bg-black/40 rounded-xl p-4 border border-white/10">
              <p className="text-xs text-gray-400 mb-2">RGB</p>
              <div
                className="w-full h-20 rounded-lg mb-3 border border-white/10"
                style={{ backgroundColor: `rgb(${rgb.join(',')})` }}
              />
              <p className="font-mono text-sm text-white">#{hexColor}</p>
            </div>

            <div className="bg-black/40 rounded-xl p-4 border border-white/10">
              <p className="text-xs text-gray-400 mb-2">CMYK</p>
              <div className="space-y-1 text-sm">
                <p><span className="text-gray-500">C:</span> {cmyk[0]}%</p>
                <p><span className="text-gray-500">M:</span> {cmyk[1]}%</p>
                <p><span className="text-gray-500">Y:</span> {cmyk[2]}%</p>
                <p><span className="text-gray-500">K:</span> {cmyk[3]}%</p>
              </div>
            </div>

            <div className="bg-black/40 rounded-xl p-4 border border-white/10">
              <p className="text-xs text-gray-400 mb-2">Metadata</p>
              <div className="space-y-2 text-xs">
                <p className="text-gray-300">
                  <span className="text-gray-500">Type:</span> Scent Design
                </p>
                <p className="text-gray-300">
                  <span className="text-gray-500">Platform:</span> v1.0
                </p>
                <p className="text-gray-300">
                  <span className="text-gray-500">Status:</span> <span className="text-green-400">Verified</span>
                </p>
              </div>
            </div>
          </div>

          {/* Action Buttons */}
          <div className="flex gap-3 pt-4">
            <button className="flex-1 px-4 py-3 rounded-lg glass hover:bg-white/10 transition-colors flex items-center justify-center gap-2">
              <Download className="w-4 h-4" />
              <span>Download Seal</span>
            </button>
            <button className="flex-1 px-4 py-3 rounded-lg bg-gradient-to-r from-scent-accent to-scent-secondary text-scent-darker font-semibold hover:shadow-lg transition-all flex items-center justify-center gap-2">
              <Share2 className="w-4 h-4" />
              <span>Share Design</span>
            </button>
          </div>

          {/* Terms */}
          <p className="text-xs text-gray-500 text-center leading-relaxed">
            This digital seal certifies the authenticity and creation timestamp of your scent design.
            The seal is immutable and can be verified on the blockchain network.
          </p>
        </div>
      </div>
    </div>
  )
}
