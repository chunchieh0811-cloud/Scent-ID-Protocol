# Scent-ID OS V31 公開通訊規範

## 概述
Scent-ID OS V31 提供標準化的跨系統通訊協定，確保不同實作間的互通性。

## 基本資料結構

### Scent-ID 格式
```
SID 文件標頭:
- 魔術位元組: SID\x00\x01 (6 bytes)
- 版本號: 1 byte (目前為 0x01)
- 資料長度: 4 bytes (大端序)
- 校驗和: 4 bytes (CRC32)
- 資料內容: 可變長度
```

### 通訊協定
- **傳輸層**: HTTP/2 + TLS 1.3
- **資料格式**: JSON + MessagePack
- **編碼**: UTF-8
- **壓縮**: LZ4 (可選)

## API 端點

### 核心端點
- `POST /scent/encode` - 編碼 scent 資料
- `GET /scent/decode/{id}` - 解碼 scent 資料
- `POST /scent/verify` - 驗證 scent 完整性
- `GET /scent/metadata/{id}` - 獲取 scent 元資料

### 管理端點
- `POST /admin/register` - 註冊新節點
- `GET /admin/status` - 獲取系統狀態
- `POST /admin/sync` - 同步資料

## 安全要求

### 認證
- 所有 API 呼叫必須使用 JWT token
- Token 有效期: 24 小時
- 支援雙因素認證

### 加密
- 傳輸層: TLS 1.3 強制
- 資料加密: AES-256-GCM
- 金鑰交換: ECDH

## 錯誤處理

### 標準錯誤碼
- `400` - 請求格式錯誤
- `401` - 未認證
- `403` - 權限不足
- `404` - 資源不存在
- `429` - 請求過於頻繁
- `500` - 伺服器內部錯誤

### 錯誤回應格式
```json
{
  "error": {
    "code": "INVALID_REQUEST",
    "message": "請求參數無效",
    "details": {
      "field": "scent_id",
      "reason": "格式錯誤"
    }
  }
}
```

## 版本控制
- API 版本通過 URL 路徑指定: `/v1/scent/encode`
- 支援版本: v1 (目前), v2 (開發中)
- 向後相容性保證: 2 個主要版本

## 效能要求
- API 回應時間: < 100ms (P95)
- 並發處理: 1000+ RPS
- 可用性: 99.9% SLA