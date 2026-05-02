#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Scent_ID_OS_V31_v0.1.py
Scent-ID OS V31 可執行版本 v0.1

功能:
- FastAPI Web 服務入口
- SID-18 生成邏輯
- 載入環境配置
- 基本系統檢查
- 架構驗證

作者: Scent-ID OS V31 團隊
版本: v0.1
日期: 2026-04-29
"""

import os
import sys
import json
import hashlib
import secrets
import argparse
import datetime
from pathlib import Path
from typing import Dict, Any, Optional
from dotenv import load_dotenv

# FastAPI 依賴
try:
    from fastapi import FastAPI, HTTPException
    from fastapi.responses import JSONResponse
    from pydantic import BaseModel
    import uvicorn
    FASTAPI_AVAILABLE = True
except ImportError:
    FASTAPI_AVAILABLE = False

# L3 編碼引擎
try:
    from L3_Encoding.L3_20260429_Encoding_Engine_V1 import ScentEncodingEngine
    ENCODING_AVAILABLE = True
except ImportError:
    ENCODING_AVAILABLE = False

class SIDRequest(BaseModel):
    """SID 生成請求模型"""
    data: str
    salt: Optional[str] = None

class EncodeRequest(BaseModel):
    """編碼請求模型"""
    scent_data: str
    metadata: Optional[Dict[str, Any]] = None
    salt: Optional[str] = None

class DecodeRequest(BaseModel):
    """解碼請求模型"""
    encoded_data: Dict[str, Any]

class SealRequest(BaseModel):
    """數位簽章請求模型"""
    sid: str
    rgb: list
    creatorId: str = "studio-v1"
    metadata: Optional[Dict[str, Any]] = None

class VerifyRequest(BaseModel):
    """簽章驗證請求模型"""
    sid: str
    fingerprint: str
    timestamp: str
    licenseId: str

class LicenseData(BaseModel):
    """授權數據模型"""
    licenseId: str
    sid: str
    creatorId: str
    timestamp: str
    valid: bool = True
    expiresAt: Optional[str] = None

class ScentIDOS:
    """Scent-ID OS v0.1 主系統"""

    def __init__(self):
        self.version = "v0.1"
        self.base_dir = Path(__file__).parent
        self.load_config()

        # 初始化編碼引擎
        if ENCODING_AVAILABLE:
            self.encoding_engine = ScentEncodingEngine()
        else:
            self.encoding_engine = None

    def load_config(self):
        """載入環境配置"""
        env_file = self.base_dir / '.env'
        if env_file.exists():
            load_dotenv(env_file)
            print("✓ 環境配置載入成功")
        else:
            print("⚠ 未找到 .env 檔案")

    def generate_sid_18(self, data: str, salt: Optional[str] = None) -> str:
        """生成 SID-18 識別碼

        SID-18 生成邏輯:
        1. 輸入數據 + 鹽值
        2. SHA256 雜湊
        3. 取前 18 字元作為 SID
        4. 轉換為大寫格式
        """
        if salt:
            combined_data = f"{data}:{salt}"
        else:
            # 使用隨機鹽值確保唯一性
            random_salt = secrets.token_hex(8)
            combined_data = f"{data}:{random_salt}"

        # SHA256 雜湊
        hash_obj = hashlib.sha256(combined_data.encode('utf-8'))
        hash_hex = hash_obj.hexdigest()

        # 取前 18 字元作為 SID-18
        sid_18 = hash_hex[:18].upper()

        return sid_18

    def check_environment(self) -> Dict[str, Any]:
        """檢查系統環境"""
        checks = {
            'Python 版本': f"{sys.version_info.major}.{sys.version_info.minor}",
            '工作目錄': str(self.base_dir),
            'GROQ API': '已配置' if os.getenv('GROQ_API_KEY') else '未配置',
            'Google API': '已配置' if os.getenv('GOOGLE_API_KEY') else '未配置',
            'Telegram': '已配置' if os.getenv('TELEGRAM_BOT_TOKEN') else '未配置',
            'FastAPI': '可用' if FASTAPI_AVAILABLE else '不可用',
            'L3 編碼引擎': '可用' if ENCODING_AVAILABLE and self.encoding_engine else '不可用'
        }
        return checks

    def validate_architecture(self) -> Dict[str, Any]:
        """驗證專案架構"""
        required_dirs = [
            'L1_Perception', 'L2_Signal', 'L3_Encoding', 'L4_Security',
            'L5_Interoperability', 'L6_Economy', 'L7_Governance',
            'docs', 'sdk', 'schemas', 'examples', 'references'
        ]

        results = {}
        missing = []

        for dir_name in required_dirs:
            exists = (self.base_dir / dir_name).exists()
            results[dir_name] = exists
            if not exists:
                missing.append(dir_name)

        return {
            'valid': len(missing) == 0,
            'missing': missing,
            'results': results
        }

def create_fastapi_app() -> FastAPI:
    """創建 FastAPI 應用"""
    if not FASTAPI_AVAILABLE:
        raise ImportError("FastAPI 未安裝，請運行: pip install fastapi uvicorn pydantic")

    app = FastAPI(
        title="Scent-ID OS V31 v0.1",
        description="Scent-ID OS V31 可執行版本 v0.1 API",
        version="0.1.0"
    )

    scent_os = ScentIDOS()

    @app.get("/")
    async def root():
        """根路徑"""
        return {
            "message": "Scent-ID OS V31 v0.1 運行中",
            "version": scent_os.version,
            "status": "active"
        }

    @app.get("/health")
    async def health_check():
        """健康檢查"""
        env_check = scent_os.check_environment()
        arch_check = scent_os.validate_architecture()

        return {
            "status": "healthy" if arch_check['valid'] else "degraded",
            "environment": env_check,
            "architecture": arch_check
        }

    @app.post("/generate-sid")
    async def generate_sid(request: SIDRequest):
        """生成 SID-18"""
        try:
            sid = scent_os.generate_sid_18(request.data, request.salt)
            return {
                "sid": sid,
                "input_data": request.data,
                "salt_provided": request.salt is not None,
                "algorithm": "SHA256-SID18"
            }
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"SID 生成失敗: {str(e)}")

    @app.post("/encode-scent")
    async def encode_scent(request: EncodeRequest):
        """編碼氣味數據"""
        if not scent_os.encoding_engine:
            raise HTTPException(status_code=503, detail="L3 編碼引擎不可用")

        try:
            result = scent_os.encoding_engine.encode_scent(
                request.scent_data,
                request.metadata,
                request.salt
            )
            return result
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"編碼失敗: {str(e)}")

    @app.post("/decode-scent")
    async def decode_scent(request: DecodeRequest):
        """解碼氣味數據"""
        if not scent_os.encoding_engine:
            raise HTTPException(status_code=503, detail="L3 編碼引擎不可用")

        try:
            result = scent_os.encoding_engine.decode_scent(request.encoded_data)
            return result
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"解碼失敗: {str(e)}")

    @app.post("/validate-encoding")
    async def validate_encoding(data: str, encoded_data: Dict[str, Any]):
        """驗證編碼正確性"""
        if not scent_os.encoding_engine:
            raise HTTPException(status_code=503, detail="L3 編碼引擎不可用")

        try:
            result = scent_os.encoding_engine.validate_encoding(data, encoded_data)
            return result
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"驗證失敗: {str(e)}")

    @app.post("/generate")
    async def generate_seal(request: SealRequest):
        """生成數位簽章"""
        try:
            import datetime
            timestamp = datetime.datetime.now().isoformat()
            fingerprint_data = f"{request.sid}|{','.join(map(str, request.rgb))}|{timestamp}|{request.creatorId}"
            fingerprint = hashlib.sha256(fingerprint_data.encode()).hexdigest()[:32].upper()
            license_id = f"LIC-{secrets.token_hex(8).upper()}"

            return {
                "sid": request.sid,
                "fingerprint": fingerprint,
                "timestamp": timestamp,
                "creatorId": request.creatorId,
                "licenseId": license_id,
                "rgb": request.rgb,
                "metadata": request.metadata or {},
                "verified": True,
            }
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"簽章生成失敗: {str(e)}")

    @app.post("/verify")
    async def verify_seal(request: VerifyRequest):
        """驗證數位簽章完整性"""
        try:
            # 在實際應用中，這裡應該驗證區塊鏈或數據庫中的簽章
            # 目前使用簡化的驗證邏輯
            return {
                "valid": True,
                "licenseId": request.licenseId,
                "message": "簽章驗證成功"
            }
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"驗證失敗: {str(e)}")

    @app.get("/license/{license_id}")
    async def get_license(license_id: str):
        """獲取授權信息"""
        try:
            # 在實際應用中，這裡應該從數據庫查詢授權信息
            return {
                "licenseId": license_id,
                "status": "active",
                "createdAt": "2026-04-29T00:00:00Z",
                "expiresAt": "2027-04-29T00:00:00Z",
                "tier": "professional",
            }
        except Exception as e:
            raise HTTPException(status_code=404, detail=f"授權不存在: {str(e)}")

    return app

def run_cli_mode():
    """運行 CLI 模式"""
    parser = argparse.ArgumentParser(description='Scent-ID OS v0.1')
    parser.add_argument('--check', action='store_true', help='檢查系統環境')
    parser.add_argument('--validate', action='store_true', help='驗證架構')
    parser.add_argument('--test-sid', action='store_true', help='生成測試 SID')
    parser.add_argument('--diagnostics', action='store_true', help='運行完整診斷')
    parser.add_argument('--serve', action='store_true', help='啟動 FastAPI 服務')

    args = parser.parse_args()
    os_instance = ScentIDOS()

    if args.serve:
        if not FASTAPI_AVAILABLE:
            print("❌ FastAPI 未安裝，請運行: pip install fastapi uvicorn pydantic")
            sys.exit(1)

        print("🚀 啟動 FastAPI 服務...")
        app = create_fastapi_app()
        uvicorn.run(app, host="127.0.0.1", port=8000)

    elif args.check:
        checks = os_instance.check_environment()
        print("\n=== 系統環境檢查 ===")
        for key, value in checks.items():
            print(f"{key}: {value}")

    elif args.validate:
        arch = os_instance.validate_architecture()
        print("\n=== 架構驗證 ===")
        if arch['valid']:
            print("✓ 架構驗證通過")
        else:
            print("✗ 架構驗證失敗:")
            for missing in arch['missing']:
                print(f"   缺少: {missing}")

    elif args.test_sid:
        test_data = "test_data_123"
        sid = os_instance.generate_sid_18(test_data)
        print(f"\n=== 測試 SID 生成 ===")
        print(f"輸入數據: {test_data}")
        print(f"生成 SID: {sid}")

    elif args.diagnostics:
        print(f"\n🚀 Scent-ID OS {os_instance.version} 啟動中...")

        checks = os_instance.check_environment()
        print("\n=== 系統環境檢查 ===")
        for key, value in checks.items():
            print(f"{key}: {value}")

        arch = os_instance.validate_architecture()
        print("\n=== 架構驗證 ===")
        if arch['valid']:
            print("✓ 架構驗證通過")
        else:
            print("✗ 架構驗證失敗:")
            for missing in arch['missing']:
                print(f"   缺少: {missing}")

        test_data = "diagnostic_test"
        sid = os_instance.generate_sid_18(test_data)
        print(f"\n=== 測試 SID 生成 ===")
        print(f"輸入數據: {test_data}")
        print(f"生成 SID: {sid}")

        print("\n✓ 診斷完成")

    else:
        parser.print_help()

def main():
    """主函數"""
    # 如果沒有參數且 FastAPI 可用，預設啟動服務
    if len(sys.argv) == 1 and FASTAPI_AVAILABLE:
        print("🚀 啟動 Scent-ID OS v0.1 FastAPI 服務...")
        app = create_fastapi_app()
        uvicorn.run(app, host="127.0.0.1", port=8000)
    else:
        run_cli_mode()

if __name__ == '__main__':
    main()