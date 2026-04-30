# Scent-ID Interactive Design Studio

生產級的交互式氣味設計平台，具有 3D 可視化、數位簽章和 SaaS 就緒功能。

## 功能

### 🎨 3D 可視化
- **分子星座渲染**: 使用 React Three Fiber 和 Three.js
- **即時色彩映射**: RGB/CMYK/HSV 顏色空間支援
- **交互式軌道控制**: 滑鼠拖動和縮放

### 🎛️ 高級控制面板
- **RGB 滑塊**: 0-255 精度
- **CMYK 滑塊**: 0-100% 精度
- **HSV 控制**: 色調、飽和度、值調整
- **透明度控制**: 256 級 Alpha 通道

### 🔐 數位簽章系統
- **SID-18 生成**: 實時唯一識別碼
- **SHA-256 指紋**: 加密驗證
- **授權管理**: 時戳、建立者 ID、授權 ID
- **驗證徽章**: 可信度指示

### 🚀 SaaS 整備
- 完整的 FastAPI 後端集成
- RESTful API 端點
- 即時 SID 生成
- 授權追蹤
- 可導出和可分享設計

## 安裝

### 前置要求
- Node.js 18+
- Python 3.8+ (用於後端)

### 設定步驟

1. **安裝依賴**
```bash
npm install
```

2. **建立環境配置**
```bash
cp .env.example .env.local
```

3. **修改 `.env.local`**
```env
VITE_API_URL=http://127.0.0.1:8000
VITE_CREATOR_ID=your-studio-id
```

4. **啟動開發服務器**
```bash
npm run dev
```

應用將在 http://localhost:3000 可用

## 開發

### 專案結構
```
src/
├── components/          # React 組件
│   ├── Header.jsx
│   ├── DomeVisualization.jsx
│   ├── ControlPanel.jsx
│   ├── DigitalSeal.jsx
│   └── index.js
├── store/              # Zustand 狀態管理
│   ├── colorStore.js
│   ├── sidStore.js
│   └── index.js
├── services/           # API 和工具服務
│   └── sealService.js
├── styles/             # 全局樣式
│   └── globals.css
├── App.jsx             # 主應用組件
└── main.jsx            # 進入點
```

### 色彩空間轉換
應用支援實時 RGB ↔ CMYK ↔ HSV 轉換：
- **RGB**: 紅綠藍色彩空間 (0-255)
- **CMYK**: 青品黃黑色彩空間 (0-100%)
- **HSV**: 色調飽和度值色彩空間 (H: 0-360°, S/V: 0-100%)

### API 整合
應用透過以下端點與 FastAPI 後端通訊：

- `POST /generate` - 生成數位簽章
- `POST /verify` - 驗證簽章
- `GET /license/{license_id}` - 獲取授權資訊
- `POST /generate-sid` - 生成 SID-18
- `POST /encode-scent` - 編碼氣味數據

## 生成

### 生成生產版本
```bash
npm run build
```

生產資源將在 `dist/` 目錄中生成。

### 性能優化
- 代碼分割
- 懶加載組件
- 資源最小化
- Gzip 壓縮

## 部署

### Docker 部署
```dockerfile
FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build
EXPOSE 3000
CMD ["npm", "run", "preview"]
```

### 環境變數 (生產)
```env
VITE_API_URL=https://api.scentid.com
VITE_CREATOR_ID=official-studio
VITE_SUBSCRIPTION_TIER=enterprise
VITE_LICENSE_KEY=your-license-key
```

## SaaS 貨幣化

### 計畫層級
1. **Free** - 基本設計工具
2. **Professional** - 無限制設計 + 數位簽章
3. **Enterprise** - 自定義品牌 + API 存取 + 優先支援

### 功能鎖定
```javascript
const features = {
  free: ['design', 'export-png'],
  professional: ['design', 'export-png', 'digital-seal', 'share'],
  enterprise: ['design', 'export-*', 'digital-seal', 'share', 'api-access']
}
```

## 許可

此專案是 Scent-ID OS V31 的一部分，依據 Scent-ID 開發者許可協議進行。

## 支援

如需幫助，請聯絡：
- 技術支援: support@scentid.com
- 開發者文檔: https://docs.scentid.com
