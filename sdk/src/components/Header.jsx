import React from 'react'
import { Sparkles, Download, Share2, Save } from 'lucide-react'

export default function Header() {
  return (
    <header className="glass-dark border-b border-scent-accent/20 px-6 py-4">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-lg bg-gradient-to-br from-scent-accent to-scent-secondary p-2">
            <Sparkles className="w-6 h-6 text-scent-darker" />
          </div>
          <div>
            <h1 className="text-2xl font-bold text-white">
              Scent-ID Design Studio
            </h1>
            <p className="text-xs text-scent-accent">
              Interactive Molecular Visualization Platform
            </p>
          </div>
        </div>

        <div className="flex items-center gap-3">
          <button className="px-4 py-2 rounded-lg glass hover:bg-white/10 transition-smooth flex items-center gap-2">
            <Save className="w-4 h-4" />
            <span className="text-sm">Save</span>
          </button>
          <button className="px-4 py-2 rounded-lg glass hover:bg-white/10 transition-smooth flex items-center gap-2">
            <Share2 className="w-4 h-4" />
            <span className="text-sm">Share</span>
          </button>
          <button className="px-4 py-2 rounded-lg glass hover:bg-white/10 transition-smooth flex items-center gap-2">
            <Download className="w-4 h-4" />
            <span className="text-sm">Export</span>
          </button>
        </div>
      </div>
    </header>
  )
}
