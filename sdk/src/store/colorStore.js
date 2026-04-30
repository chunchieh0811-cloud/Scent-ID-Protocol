import { create } from 'zustand'

const useColorStore = create((set) => ({
  rgb: [255, 180, 210],
  cmyk: [0, 29, 18, 0],
  hsv: [330, 29, 100],
  alpha: 255,

  setRGB: (rgb) => set({
    rgb,
    cmyk: rgbToCmyk(rgb),
    hsv: rgbToHsv(rgb),
  }),

  setCMYK: (cmyk) => set({
    cmyk,
    rgb: cmykToRgb(cmyk),
    hsv: cmykToHsv(cmyk),
  }),

  setHSV: (hsv) => set({
    hsv,
    rgb: hsvToRgb(hsv),
    cmyk: hsvToCmyk(hsv),
  }),

  setAlpha: (alpha) => set({ alpha }),
}))

// Color conversion utilities
function rgbToCmyk([r, g, b]) {
  const c = 1 - r / 255
  const m = 1 - g / 255
  const y = 1 - b / 255
  const k = Math.min(c, m, y)
  return [
    Math.round(((c - k) / (1 - k)) * 100) || 0,
    Math.round(((m - k) / (1 - k)) * 100) || 0,
    Math.round(((y - k) / (1 - k)) * 100) || 0,
    Math.round(k * 100),
  ]
}

function cmykToRgb([c, m, y, k]) {
  const r = 255 * (1 - c / 100) * (1 - k / 100)
  const g = 255 * (1 - m / 100) * (1 - k / 100)
  const b = 255 * (1 - y / 100) * (1 - k / 100)
  return [Math.round(r), Math.round(g), Math.round(b)]
}

function rgbToHsv([r, g, b]) {
  r /= 255
  g /= 255
  b /= 255
  const max = Math.max(r, g, b)
  const min = Math.min(r, g, b)
  const delta = max - min
  let h = 0
  let s = 0
  const v = max

  if (delta !== 0) {
    s = delta / max
    if (max === r) h = (((g - b) / delta + 6) % 6) * 60
    else if (max === g) h = (((b - r) / delta + 2) * 60)
    else h = (((r - g) / delta + 4) * 60)
  }

  return [Math.round(h), Math.round(s * 100), Math.round(v * 100)]
}

function hsvToRgb([h, s, v]) {
  s /= 100
  v /= 100
  const c = v * s
  const x = c * (1 - (((h / 60) % 2) - 1) >= 0 ? ((h / 60) % 2) - 1 : 1 - ((h / 60) % 2))
  const m = v - c
  let r, g, b

  if (h < 60) [r, g, b] = [c, x, 0]
  else if (h < 120) [r, g, b] = [x, c, 0]
  else if (h < 180) [r, g, b] = [0, c, x]
  else if (h < 240) [r, g, b] = [0, x, c]
  else if (h < 300) [r, g, b] = [x, 0, c]
  else [r, g, b] = [c, 0, x]

  return [
    Math.round((r + m) * 255),
    Math.round((g + m) * 255),
    Math.round((b + m) * 255),
  ]
}

function cmykToHsv(cmyk) {
  return rgbToHsv(cmykToRgb(cmyk))
}

function hsvToCmyk(hsv) {
  return rgbToCmyk(hsvToRgb(hsv))
}

export default useColorStore
