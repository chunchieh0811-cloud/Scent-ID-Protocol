# ============================================================================
# Scent-ID OS v0.1 → Modular Architecture Migration Script
# ============================================================================
# 目的: 將 v0.1 平面結構轉換為多層應用架構
# 版本: 1.0
# 日期: 2026-04-29
# ============================================================================

param(
    [switch]$DryRun = $false,
    [switch]$Backup = $true,
    [switch]$Verbose = $false
)

$ErrorActionPreference = "Stop"
$timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
$projectRoot = Get-Location
$logFile = Join-Path $projectRoot "migration_${timestamp}.log"
$backupDir = Join-Path $projectRoot "backup_${timestamp}"

# ============================================================================
# 日誌函數
# ============================================================================
function Write-Log {
    param([string]$Message, [string]$Level = "INFO")
    $logMsg = "[$([DateTime]::Now.ToString('HH:mm:ss'))] [$Level] $Message"
    Add-Content -Path $logFile -Value $logMsg
    if ($Verbose -or $Level -in @("WARN", "ERROR")) {
        Write-Host $logMsg -ForegroundColor $(
            switch($Level) {
                "ERROR" { "Red" }
                "WARN"  { "Yellow" }
                "OK"    { "Green" }
                default { "White" }
            }
        )
    }
}

function New-Header {
    param([string]$Text)
    $line = "=" * 70
    $msg = "`n$line`n  $Text`n$line"
    Write-Log $msg
}

# ============================================================================
# 初始化
# ============================================================================
Write-Log "開始 Scent-ID 結構遷移" "OK"
Write-Log "工作目錄: $projectRoot"
Write-Log "模式: $(if($DryRun) {'DRY RUN'} else {'EXECUTION'})"

# 建立日誌檔案
New-Item -Path $logFile -Force | Out-Null

# ============================================================================
# 備份現有結構
# ============================================================================
if ($Backup -and -not $DryRun) {
    New-Header "建立備份"
    try {
        New-Item -ItemType Directory -Path $backupDir -Force | Out-Null
        Write-Log "備份目錄: $backupDir"
        
        @('sdk', 'scent_id_v0.1.py', 'package.json', 'vite.config.js') | ForEach-Object {
            if (Test-Path (Join-Path $projectRoot $_)) {
                Copy-Item -Path (Join-Path $projectRoot $_) -Destination $backupDir -Recurse -Force
                Write-Log "已備份: $_" "OK"
            }
        }
    }
    catch {
        Write-Log "備份失敗: $_" "ERROR"
        exit 1
    }
}

# ============================================================================
# 步驟 1: 建立新目錄結構
# ============================================================================
New-Header "建立新目錄結構"

$dirsToCreate = @(
    'app',
    'app/frontend',
    'app/backend',
    'app/backend/api',
    'app/backend/engines',
    'app/backend/models',
    'app/shared',
    'app/shared/models',
    'app/shared/types',
    'web',
    'web/public',
    'web/src',
    'web/docs'
)

foreach ($dir in $dirsToCreate) {
    $dirPath = Join-Path $projectRoot $dir
    if (-not (Test-Path $dirPath)) {
        if (-not $DryRun) {
            New-Item -ItemType Directory -Path $dirPath -Force | Out-Null
        }
        Write-Log "建立目錄: $dir" "OK"
    }
    else {
        Write-Log "已存在: $dir" "WARN"
    }
}

# ============================================================================
# 步驟 2: 移動 SDK → app/frontend
# ============================================================================
New-Header "遷移 SDK → app/frontend"

$sdkPath = Join-Path $projectRoot "sdk"
$appFrontendPath = Join-Path $projectRoot "app/frontend"

if (Test-Path $sdkPath) {
    if (-not $DryRun) {
        # 複製 SDK 內容到 app/frontend
        Get-ChildItem -Path $sdkPath -Force | ForEach-Object {
            Copy-Item -Path $_.FullName -Destination $appFrontendPath -Recurse -Force
            Write-Log "複製: sdk/$($_.Name) → app/frontend/$($_.Name)" "OK"
        }
    }
    else {
        Write-Log "[DRY RUN] 將複製 sdk → app/frontend" "WARN"
    }
}

# ============================================================================
# 步驟 3: 移動 scent_id_v0.1.py → app/backend/main.py
# ============================================================================
New-Header "遷移 scent_id_v0.1.py → app/backend/main.py"

$oldMainPath = Join-Path $projectRoot "scent_id_v0.1.py"
$newMainPath = Join-Path $projectRoot "app/backend/main.py"

if (Test-Path $oldMainPath) {
    if (-not $DryRun) {
        Copy-Item -Path $oldMainPath -Destination $newMainPath -Force
        Write-Log "複製: scent_id_v0.1.py → app/backend/main.py" "OK"
    }
    else {
        Write-Log "[DRY RUN] 將複製 scent_id_v0.1.py → app/backend/main.py" "WARN"
    }
}

# ============================================================================
# 步驟 4: 複製 L3 編碼引擎到 app/backend/engines
# ============================================================================
New-Header "複製 L3 編碼引擎"

$l3SourcePath = Join-Path $projectRoot "L3_Encoding/L3_20260429_Encoding_Engine_V1.py"
$l3DestPath = Join-Path $projectRoot "app/backend/engines/encoding_engine.py"

if (Test-Path $l3SourcePath) {
    if (-not $DryRun) {
        Copy-Item -Path $l3SourcePath -Destination $l3DestPath -Force
        Write-Log "複製: L3_Encoding/L3_20260429_Encoding_Engine_V1.py → app/backend/engines/encoding_engine.py" "OK"
    }
    else {
        Write-Log "[DRY RUN] 將複製 L3 編碼引擎" "WARN"
    }
}

# ============================================================================
# 步驟 5: 建立共用模型檔案
# ============================================================================
New-Header "建立共用模型結構"

if (-not $DryRun) {
    @{
        'app/backend/__init__.py' = ""
        'app/backend/api/__init__.py' = ""
        'app/backend/models/__init__.py' = ""
        'app/backend/engines/__init__.py' = ""
        'app/shared/__init__.py' = ""
        'app/shared/models/__init__.py' = ""
    }.GetEnumerator() | ForEach-Object {
        $filePath = Join-Path $projectRoot $_.Key
        if (-not (Test-Path $filePath)) {
            New-Item -Path $filePath -Force | Out-Null
            Write-Log "建立: $($_.Key)" "OK"
        }
    }
}

# ============================================================================
# 步驟 6: 建立 web 的初始結構
# ============================================================================
New-Header "建立 web 目錄結構"

if (-not $DryRun) {
    @{
        'web/README.md' = "# Scent-ID Official Website & SaaS Landing Pages`n`nPublic-facing website, documentation, and marketing materials.`n"
        'web/package.json' = "{`n  `"name`": `"scentid-web`",`n  `"version`": `"1.0.0`",`n  `"description`": `"Scent-ID Official Web Presence`"`n}"
    }.GetEnumerator() | ForEach-Object {
        $filePath = Join-Path $projectRoot $_.Key
        if (-not (Test-Path $filePath)) {
            Set-Content -Path $filePath -Value $_.Value -Force
            Write-Log "建立: $($_.Key)" "OK"
        }
    }
}

# ============================================================================
# 步驟 7: 建立遷移後的根目錄 main.py
# ============================================================================
New-Header "建立根目錄啟動腳本"

$rootMainPath = Join-Path $projectRoot "main.py"
$rootMainContent = @"
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Scent-ID OS v0.1 - Modular Architecture Entry Point

This script serves as the entry point for the modular Scent-ID architecture.
It delegates to app/backend/main.py and manages the application lifecycle.

版本: v0.1
日期: 2026-04-29
"""

import sys
import os
from pathlib import Path

# 設定 Python 路徑
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / 'app/backend'))

# 匯入應用
from app.backend.main import ScentIDOS, create_fastapi_app, run_cli_mode

if __name__ == '__main__':
    # 委派給原始主程式
    import sys
    sys.argv[0] = str(project_root / 'app/backend/main.py')
    
    if len(sys.argv) > 1:
        run_cli_mode()
    else:
        app = create_fastapi_app()
        import uvicorn
        uvicorn.run(app, host='127.0.0.1', port=8000)
"@

if (-not $DryRun) {
    Set-Content -Path $rootMainPath -Value $rootMainContent -Force
    Write-Log "建立: main.py (根目錄啟動腳本)" "OK"
}

# ============================================================================
# 步驟 8: 建立遷移指南
# ============================================================================
New-Header "建立遷移指南"

$migrationGuidePath = Join-Path $projectRoot "MIGRATION_GUIDE.md"
$migrationGuideContent = @"
# Scent-ID v0.1 → Modular Architecture Migration

## 概述
此遷移將平面 Scent-ID v0.1 結構轉換為模塊化應用架構，同時保留所有 L1-L7 層。

## 新結構

### 應用層 (\`app/\`)
\`\`\`
app/
├── frontend/        # React 3D 設計工作室 (來自 sdk/)
├── backend/         # FastAPI 後端服務 (來自 scent_id_v0.1.py)
│   ├── main.py      # 主應用進入點
│   ├── api/         # API 路由
│   ├── models/      # 數據模型 (Pydantic)
│   └── engines/     # L3 編碼引擎副本
└── shared/          # 前後端共用類型
    ├── models/      # 共用 Pydantic 模型
    └── types/       # TypeScript/Python 共用定義
\`\`\`

### Web 層 (\`web/\`)
- 官方營銷網站
- SaaS 登陸頁面
- 公開文檔

### L 層 (不變)
- L1_Perception/ - 氣味採集
- L2_Signal/ - 信號處理
- L3_Encoding/ - SID 編碼 (原始位置保留)
- L4_Security/ - 加密與驗證
- L5_Interoperability/ - SIDX 協議
- L6_Economy/ - 授權與計費
- L7_Governance/ - 治理與合規

## 檔案映射

| 舊位置 | 新位置 |
|------|------|
| \`sdk/\` | \`app/frontend/\` |
| \`scent_id_v0.1.py\` | \`app/backend/main.py\` |
| \`L3_Encoding/L3_20260429_Encoding_Engine_V1.py\` | \`app/backend/engines/encoding_engine.py\` (副本) |

## 進行中的遷移

### 後端入口
- 新入口: \`app/backend/main.py\`
- 根目錄 \`main.py\` 委派給新入口
- L3 編碼引擎導入路徑: \`from app.backend.engines.encoding_engine import ScentEncodingEngine\`

### 前端開發
- 工作目錄: \`app/frontend/\`
- 啟動開發伺服器: \`npm run dev\`
- API 代理: \`http://127.0.0.1:8000\`

## 推薦命令

### 後端
\`\`\`bash
cd d:\\Aetherbit\\ScentID
python main.py --serve        # 啟動 FastAPI 伺服器
python main.py --diagnostics  # 運行診斷
python main.py --validate     # 驗證架構
\`\`\`

### 前端
\`\`\`bash
cd d:\\Aetherbit\\ScentID\\app\\frontend
npm install
npm run dev
\`\`\`

## 備份位置
遷移備份已儲存至: \`backup_${timestamp}/\`

## 後續步驟

1. **更新所有導入**
   - 檢查 \`app/backend/main.py\` 中的 L 層導入
   - 確保相對路徑正確解析

2. **測試應用**
   - 後端: \`python app/backend/main.py --test-sid\`
   - 前端: \`cd app/frontend && npm run dev\`

3. **Git 管理**
   - 檢查: \`git status\`
   - 驗證備份在 \`.gitignore\` 中
   - 提交: \`git add -A && git commit -m "[Migration] Modular architecture setup v0.1"\`

4. **持續改進**
   - 根據需要將 L 層邏輯封裝到 \`app/backend/engines/\`
   - 在 \`app/shared/models/\` 中定義共用類型

---
遷移完成於: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')
"@

if (-not $DryRun) {
    Set-Content -Path $migrationGuidePath -Value $migrationGuideContent -Force
    Write-Log "建立: MIGRATION_GUIDE.md" "OK"
}
else {
    Write-Log "[DRY RUN] 將建立 MIGRATION_GUIDE.md" "WARN"
}

# ============================================================================
# 完成報告
# ============================================================================
New-Header "遷移完成"

$summary = @"
Scent-ID 結構遷移報告
======================

遷移時間戳: $timestamp
執行模式: $(if($DryRun) {'DRY RUN'} else {'EXECUTION'})
備份位置: $backupDir

新結構:
  ✓ app/frontend/        (React 3D 設計工作室)
  ✓ app/backend/         (FastAPI 服務)
  ✓ app/shared/          (共用模型)
  ✓ web/                 (營銷網站)
  ✓ L1-L7 層級           (保持原位)

關鍵檔案:
  ✓ app/backend/main.py  (原 scent_id_v0.1.py)
  ✓ main.py              (根目錄委派指令)
  ✓ MIGRATION_GUIDE.md   (遷移文檔)

後續:
  1. 檢查 app/backend/main.py 的導入
  2. 驗證 L 層路徑解析
  3. 測試後端: python main.py --serve
  4. 測試前端: cd app/frontend && npm run dev

日誌檔案: $logFile
"@

Write-Log $summary
Write-Host "`n$summary" -ForegroundColor Green

# ============================================================================
# 驗證檢查
# ============================================================================
New-Header "驗證檢查"

$checks = @(
    @{ Path = 'app'; Type = 'Directory' },
    @{ Path = 'app/frontend'; Type = 'Directory' },
    @{ Path = 'app/backend'; Type = 'Directory' },
    @{ Path = 'app/shared'; Type = 'Directory' },
    @{ Path = 'web'; Type = 'Directory' },
    @{ Path = 'app/backend/main.py'; Type = 'File' },
    @{ Path = 'main.py'; Type = 'File' }
)

$allValid = $true
foreach ($check in $checks) {
    $fullPath = Join-Path $projectRoot $check.Path
    $exists = Test-Path $fullPath -PathType $check.Type
    $symbol = if ($exists) { "✓" } else { "✗" }
    $status = if ($exists) { "OK" } else { "MISSING" }
    Write-Log "$symbol $($check.Path) ($($check.Type))" $status
    if (-not $exists) { $allValid = $false }
}

if ($allValid) {
    Write-Log "✓ 所有檢查通過" "OK"
    exit 0
}
else {
    Write-Log "✗ 某些項目缺失 - 檢查日誌" "ERROR"
    exit 1
}
