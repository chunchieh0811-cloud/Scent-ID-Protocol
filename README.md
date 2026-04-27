# Scent-ID Global: The Universal Protocol for Digital Olfaction

**"Scent-ID is not merely a scent technology platform. It is the identity, interoperability, and economic layer for the global machine-olfaction ecosystem."**

A blockchain-native, AI-powered global standard for scent identity, interoperability, and monetization.

---

## 0. Mission Statement
Just as images became pixels, music became digital audio, and text became Unicode, scent is now becoming programmable. **Scent-ID gives smell a universal digital identity.** Scent-ID Global is an open, interoperable protocol designed to identify, encode, verify, and monetize scent across digital and physical environments. It serves as the foundational identity and interoperability layer for the emerging global scent economy.

---

## 1. Core Technology: The 256-Dimensional Scent Matrix
At the heart of Scent-ID lies a proprietary **256-dimensional olfactory embedding framework** that transforms complex molecular and sensory characteristics into vectorized machine-readable representations.

### 🧬 256 Genesis Nodes & Molecular Anchoring
- **CAS Registry Anchoring**: Each scent is mapped into a structured latent space anchored by a curated library of 256 chemically significant compounds, identified via their unique **CAS Registry Numbers**.
- **Vectorized Representation**: Scents occupy unique coordinates in a high-dimensional olfactory space, determined by molecular mass, polarity, volatility, and perceptual response.
- **Aetherbit Encoding Engine**: Converts molecular composition and evaporation kinetics into a normalized vector representation, enabling robust retrieval and generative modeling.

---

## 2. SID-18: Human-Readable Scent Identity
Every scent is assigned a unique **SID-18**, an 18-character hexadecimal identifier designed for branding and commercial labeling.

| Segment | Name | Description |
| :--- | :--- | :--- |
| **[1–6]** | **Foundation Code** | Core molecular signature. |
| **[7–12]** | **Temporal Code** | Volatility and evaporation dynamics. |
| **[13–18]** | **Integrity Code** | Cryptographic verification, anti-counterfeit obfuscation. |

---

## 3. The Scent Palette: Nine Foundational Channels
To make scent composition as intuitive as visual design, Scent-ID compresses high-dimensional space into nine primary sensory channels (**R-O-Y-G-B-I-V-W-K**).

| Channel | Molecular Basis | Code | Functional Role |
| :--- | :--- | :--- | :--- |
| **Red (R)** | Spicy / Phenolic | CH-01 | Heat, impact, intensity |
| **Orange (O)** | Citrus / Terpenic | CH-02 | Brightness, acidity, lift |
| **Yellow (Y)** | Floral / Esteric | CH-03 | Sweetness, floral character |
| **Green (G)** | Herbal / Green Aldehydic | CH-04 | Freshness, botanical tone |
| **Blue (B)** | Marine / Aquatic Ketonic | CH-05 | Coolness, humidity, clarity |
| **Indigo (I)** | Musk / Macrocyclic Lactonic | CH-06 | Skin affinity, softness, depth |
| **Violet (V)** | Woody / Smoky Sesquiterpenic | CH-07 | Structure, dryness, body |
| **White (W)** | Diffusion / High Volatility | CH-08 | Projection, transparency |
| **Black (K)** | Intensity / Sulfuric Saturation| CH-09 | Density, penetration, persistence |

---

## 4. Cross-Modal AI & File Formats
### 🤖 Scent-LLM
Built on Aetherbit AI Agent Architecture, supporting:
- **Text-to-Scent / Image-to-Scent / Video-to-Scent**: Automatic SID generation from multimodal input.
- **Video-to-Scent Watermarking**: Embedded digital watermarks for media-linked scent assets.

### 📄 .sict File Format
The **.sict** (Scent-ID Composition Template) is the universal exchange format for scent palettes, allowing perfumers and AI to swap programmable scent data seamlessly.

---

## 5. Hardware Abstraction Layer (HAL)
The HAL ensures accurate scent reproduction across different devices:
- **256-level digital nozzle precision.**
- **Physical spray compensation algorithms.**
- **Spatial Coverage**: Optimization for environments up to **1,000 m³**.

---

## 6. Blockchain Sovereignty & Treasury Architecture
### 🛡️ Genesis Hash
The foundational 256-anchor molecular reference matrix is cryptographically hashed and anchored on the **Base Network** as the immutable root of truth.

### 💰 Dual-Treasury Architecture
- **W1 — Sovereign Treasury (0x490A...)**: Governs licensing revenue, certification fees, and royalty streams.
- **W2 — Verification Treasury (0x82Fa...)**: Processes real-time validation, API metering, and settlement.

---

## 7. Monetization & Licensing Model
Based on the **Kelly Criterion**: "Open Adoption, Imperial Taxation."

| Service | Customer | Pricing Model |
| :--- | :--- | :--- |
| **SID Commercial Issuance** | Brands | Annual Licensing (1 BTC / Year) |
| **On-chain Registration** | Manufacturers | 0.001 ETH per SID |
| **HAL Certification** | Hardware Makers | Per-device Royalty |
| **Verification API** | Platforms | Metered Pay-per-call |
| **Scent-LLM Generation** | Developers | Usage-based Inference Fees |

---

## 🔗 Official Resources
- **GitHub**: [Scent-ID Global](https://github.com/chunchieh0811-cloud/Scent-ID-Protocol)
- **LinkedIn**: Jay Huang, Founder of Scent-ID Protocol
- **Media Asset**: `v2_watermarked_scent_demo.mp4`

**Powered by Aetherbit AI Agent Architecture**
*(Planning · Memory · Tool Use · Perception)*

---

## Local Operations (Empire Restore)

Three-layer working architecture:

- `01_Constitution`: constitutional and master archive source documents
- `02_Protocol`: protocol scripts and automation
- `03_Application`: generated application artifacts (including locked PDFs)

Generate locked protocol PDF from `01_Constitution`:

```bash
pip install -r requirements.txt
python 02_Protocol/build_locked_pdf.py
```

Expected output:

- `03_Application/ScentID_Master_Archive_LOCKED.pdf`

### Quick Verification (Commander)

Run one command to verify structure + PDF pipeline:

```powershell
.\verify.ps1
```

Checks performed:

- `01_Constitution`, `02_Protocol`, `03_Application` all exist
- `.env` presence is reported (warning only, compatible with USB key workflow)
- `02_Protocol/build_locked_pdf.py` executes successfully
- `03_Application/ScentID_Master_Archive_LOCKED.pdf` is produced

### CI Status

GitHub Actions workflow:

- `Verify Empire Restore` (`.github/workflows/verify.yml`)

Badge:

`https://github.com/chunchieh0811-cloud/Scent-ID-Protocol/actions/workflows/verify.yml/badge.svg`
