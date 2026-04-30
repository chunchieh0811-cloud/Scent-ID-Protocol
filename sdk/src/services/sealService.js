import axios from 'axios'

const API_BASE = '/api'

// Generate SID-18 via FastAPI backend
export async function generateSID18(rgb) {
  try {
    const response = await axios.post(`${API_BASE}/generate-sid`, {
      data: `${rgb.join('-')}`,
    })
    return response.data.sid
  } catch (error) {
    console.error('Failed to generate SID-18:', error)
    return generateClientSideSID18(rgb)
  }
}

// Fallback client-side SID-18 generation using SHA-256
function generateClientSideSID18(rgb) {
  const data = `scent-${rgb.join('-')}-${Date.now()}`
  return SHA256(data).substring(0, 18).toUpperCase()
}

// Generate digital seal with SHA-256 fingerprint
export async function generateDigitalSeal({ sid, rgb, creatorId, metadata = {} }) {
  const timestamp = new Date().toISOString()
  const fingerprintData = `${sid}|${rgb.join(',')}|${timestamp}|${creatorId}`
  const fingerprint = SHA256(fingerprintData).substring(0, 32).toUpperCase()

  const licenseId = `LIC-${generateUID()}`

  return {
    sid,
    fingerprint,
    timestamp,
    creatorId,
    licenseId,
    rgb,
    metadata,
    verified: true,
  }
}

// Verify seal integrity
export async function verifySeal(seal) {
  try {
    const response = await axios.post(`${API_BASE}/verify`, seal)
    return response.data.valid
  } catch (error) {
    console.error('Failed to verify seal:', error)
    return false
  }
}

// Get license information
export async function getLicense(licenseId) {
  try {
    const response = await axios.get(`${API_BASE}/license/${licenseId}`)
    return response.data
  } catch (error) {
    console.error('Failed to get license:', error)
    return null
  }
}

// SHA-256 implementation (using Web Crypto API)
export async function SHA256(message) {
  const encoder = new TextEncoder()
  const data = encoder.encode(message)
  const hashBuffer = await crypto.subtle.digest('SHA-256', data)
  const hashArray = Array.from(new Uint8Array(hashBuffer))
  return hashArray.map(b => b.toString(16).padStart(2, '0')).join('')
}

// Generate UID
function generateUID() {
  return Math.random().toString(36).substring(2, 15) + 
         Math.random().toString(36).substring(2, 15)
}
