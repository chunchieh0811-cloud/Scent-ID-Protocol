# Scent-ID Protocol (SID) v1.0
**The Global Digital Standard for Olfactory Perception and Standardization**

## 🧬 Core Technical Architecture (核心技術架構)
- **256-Dimensional Chemical Coordinates (S-001 to S-256)**: The world's first digital olfactory modeling standard for precise sensory space definition.
- **SHA-256 Encrypted Indexing**: Ensures the uniqueness, immutability, and digital traceability of every Scent-ID.
- **Dynamic Physics Parameters**: Integration of ultrasonic atomization frequency and air diffusion algorithms for cross-device scent reproduction.

### 📂 Data Naming & Structure Standard (數據命名與結構標準)
為了確保全球氣味數據的一致性與自動化讀取，所有 Scent-ID 檔案必須遵循以下規範：

1. **檔案命名規則**：`SID-[BRAND_CODE]-[MODEL].json`
   - 品牌代碼：2-3 位大寫字母 (例如: Chanel 為 CH)。
   - 檔案路徑：必須存放於 `/database/` 資料夾下。

2. **JSON 內部書寫準則**：
   - **Key 值**：一律使用英文小寫與下底線 (Snake Case)，如 `sid_index`, `brand`, `coordinates`。
   - **座標格式**：`"S-[001-256]": [0-100]`，定義 256 維化學空間座標。
   - **版本控制**：需標註 `version` 以追蹤氣味配方的疊代狀態。

## 💰 Global Commercial Terms & Licensing
The **Scent-ID Foundation** governs the issuance, certification, and physical layer parameter licensing of digital olfactory identities.

### 1. Unique SID Issuance (Identity Layer)
- **Fee**: **$50 USD** / per ID (One-time administrative fee)
- **Description**: For every unique 256-dimensional coordinate set (single or blended), a permanent, encrypted Unique Scent ID (SID) is issued.

### 2. Scent-ID Certification (Trust Layer)
- **Fee**: **$1,500 USD** / Annum
- **Description**: Licensing for the "Scent-ID Certified" label and official QR code usage. Includes access to the global cloud verification database and technical synchronization.

### 3. Dynamic Physics Modulating (Engineering Layer)
- **Fee**: Project-based Quotation (Custom API Integration)
- **Core Parameters**:
  - **Vibration Frequency**: Precision ultrasonic modulation for molecular dispersion.
  - **Persistence Control**: Time-decay algorithms for olfactory duration management.
  - **Spatial Volumetric Range**: Coverage optimization for environments up to 1,000 m³.
