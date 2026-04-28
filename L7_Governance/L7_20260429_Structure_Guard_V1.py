#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
L7_20260429_Structure_Guard_V1.py
Scent-ID OS V31 架構守護者 - 結構驗證與安全掃描

功能:
- 檔案命名規範驗證
- 敏感資訊掃描
- SID 魔術位元組檢查
- 架構完整性驗證

作者: Scent-ID OS V31 治理層
版本: V1.0
日期: 2026-04-29
"""

import os
import re
import json
import hashlib
from pathlib import Path
from typing import List, Tuple, Dict, Any

class StructureGuard:
    """架構守護者主類"""

    def __init__(self, root_path: str = None):
        self.root_path = Path(root_path) if root_path else Path.cwd()
        self.sid_magic_bytes = b'SID\x00\x01'  # Scent-ID 魔術位元組
        self.sensitive_patterns = [
            r'\b\d{4}[\s\-]?\d{4}[\s\-]?\d{4}[\s\-]?\d{4}\b',  # 信用卡號
            r'\b\d{3}[\s\-]?\d{3}[\s\-]?\d{4}\b',  # SSN
            r'password\s*[:=]\s*\w+',  # 密碼
            r'api[_-]?key\s*[:=]\s*\w+',  # API 金鑰
            r'secret[_-]?key\s*[:=]\s*\w+',  # 秘密金鑰
        ]

    def check_file_naming(self, file_path: Path) -> Tuple[bool, str]:
        """檢查檔案命名是否符合規範"""
        filename = file_path.name

        # 跳過特殊檔案
        if filename in ['.clinerules', '.gitignore', 'README.md']:
            return True, "Special file allowed"

        # 檢查命名格式: [L#]_[日期]_[描述]_V[版本]
        pattern = r'^L[1-7]_\d{8}_[A-Za-z_]+_V\d+$'
        if not re.match(pattern, filename):
            return False, f"Invalid naming format: {filename}"

        return True, "Valid naming format"

    def check_sensitive_info(self, file_path: Path) -> Tuple[bool, List[str]]:
        """檢查檔案是否包含敏感資訊"""
        if file_path.suffix.lower() not in ['.py', '.txt', '.md', '.json']:
            return True, []

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except (UnicodeDecodeError, OSError):
            return True, []  # 跳過無法讀取的檔案

        violations = []
        for pattern in self.sensitive_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            if matches:
                violations.extend(matches[:3])  # 只記錄前3個匹配

        return len(violations) == 0, violations

    def check_sid_magic_bytes(self, file_path: Path) -> Tuple[bool, str]:
        """檢查 SID 檔案的魔術位元組"""
        if file_path.suffix.lower() != '.sid':
            return True, "Not a SID file"

        try:
            with open(file_path, 'rb') as f:
                header = f.read(6)
                if header == self.sid_magic_bytes:
                    return True, "Valid SID magic bytes"
                else:
                    return False, f"Invalid SID magic bytes: {header.hex()}"
        except OSError:
            return False, "Cannot read SID file"

    def validate_architecture(self) -> Tuple[bool, List[str]]:
        """驗證整體架構完整性"""
        errors = []

        # 檢查 L1-L7 目錄是否存在
        for i in range(1, 8):
            layer_dir = self.root_path / f"L{i}_Perception" if i == 1 else \
                       self.root_path / f"L{i}_Signal" if i == 2 else \
                       self.root_path / f"L{i}_Encoding" if i == 3 else \
                       self.root_path / f"L{i}_Security" if i == 4 else \
                       self.root_path / f"L{i}_Interoperability" if i == 5 else \
                       self.root_path / f"L{i}_Economy" if i == 6 else \
                       self.root_path / f"L{i}_Governance"

            if not layer_dir.exists():
                errors.append(f"Missing layer directory: {layer_dir.name}")

        # 檢查生態資源目錄
        ecosystem_dirs = ['docs', 'sdk', 'schemas', 'examples', 'references']
        for dir_name in ecosystem_dirs:
            if not (self.root_path / dir_name).exists():
                errors.append(f"Missing ecosystem directory: {dir_name}")

        # 檢查 .clinerules 檔案
        if not (self.root_path / '.clinerules').exists():
            errors.append("Missing .clinerules file")

        return len(errors) == 0, errors

    def scan_directory(self, scan_path: Path = None) -> Dict[str, Any]:
        """掃描目錄並返回報告"""
        scan_path = scan_path or self.root_path

        report = {
            'total_files': 0,
            'naming_violations': [],
            'sensitive_violations': [],
            'sid_violations': [],
            'architecture_valid': False,
            'architecture_errors': []
        }

        # 驗證架構
        arch_valid, arch_errors = self.validate_architecture()
        report['architecture_valid'] = arch_valid
        report['architecture_errors'] = arch_errors

        # 掃描檔案
        for file_path in scan_path.rglob('*'):
            if file_path.is_file():
                report['total_files'] += 1

                # 檢查命名
                naming_ok, naming_msg = self.check_file_naming(file_path)
                if not naming_ok:
                    report['naming_violations'].append({
                        'file': str(file_path.relative_to(scan_path)),
                        'error': naming_msg
                    })

                # 檢查敏感資訊
                sensitive_ok, sensitive_matches = self.check_sensitive_info(file_path)
                if not sensitive_ok:
                    report['sensitive_violations'].append({
                        'file': str(file_path.relative_to(scan_path)),
                        'matches': sensitive_matches
                    })

                # 檢查 SID 檔案
                sid_ok, sid_msg = self.check_sid_magic_bytes(file_path)
                if not sid_ok:
                    report['sid_violations'].append({
                        'file': str(file_path.relative_to(scan_path)),
                        'error': sid_msg
                    })

        return report

def main():
    """主函數"""
    import sys

    guard = StructureGuard()

    if len(sys.argv) > 1 and sys.argv[1] == '--report':
        # 生成報告
        report = guard.scan_directory()
        print(json.dumps(report, indent=2, ensure_ascii=False))
    else:
        # 快速驗證
        arch_valid, arch_errors = guard.validate_architecture()
        if arch_valid:
            print("Architecture validation passed")
        else:
            print("Architecture validation failed:")
            for error in arch_errors:
                print(f"  {error}")
            sys.exit(1)

if __name__ == '__main__':
    main()