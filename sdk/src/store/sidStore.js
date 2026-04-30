import { create } from 'zustand'
import { generateSID18, generateDigitalSeal } from '../services/sealService'

const useSIDStore = create((set, get) => ({
  sid: 'SID-0000000000000000',
  seal: null,
  createdAt: null,
  creatorId: 'studio-v1',
  licenseId: null,

  updateSID: async (rgb) => {
    const newSID = await generateSID18(rgb)
    set({ sid: newSID })
  },

  generateSeal: async (rgb, metadata = {}) => {
    const state = get()
    const sealData = await generateDigitalSeal({
      sid: state.sid,
      rgb,
      creatorId: state.creatorId,
      metadata,
    })
    set({
      seal: sealData,
      createdAt: new Date(),
      licenseId: sealData.licenseId,
    })
    return sealData
  },

  setCreatorId: (creatorId) => set({ creatorId }),
  setLicenseId: (licenseId) => set({ licenseId }),
}))

export default useSIDStore
