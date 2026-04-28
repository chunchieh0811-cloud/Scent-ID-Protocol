#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
L7_20260429_Auto_Map_V2.py
Scent-ID OS V31 自動化索引與分類系統

功能:
- 自動檔案分類到正確層次
- 架構驗證與修復
- 每日維護任務
- 檔案命名驗證

作者: Scent-ID OS V31 治理層
版本: V2.0
日期: 2026-04-29
"""

import os
import re
import sys
import json
import shutil
import argparse
from pathlib import Path
from datetime import datetime
from typing import List, Tuple, Dict, Any

class AutoMap:
    """自動化索引與分類系統"""

    def __init__(self, root_path: str = None):
        self.root_path = Path(root_path) if root_path else Path.cwd()
        self.layer_keywords = {
            1: ['perception', 'sensor', 'input', 'raw', 'data'],  # L1_Perception
            2: ['signal', 'process', 'transform', 'normalize', 'filter'],  # L2_Signal
            3: ['encoding', 'compress', 'encrypt', 'format', 'codec'],  # L3_Encoding
            4: ['security', 'auth', 'encrypt', 'protect', 'guard'],  # L4_Security
            5: ['interop', 'protocol', 'comm', 'interface', 'api'],  # L5_Interoperability
            6: ['economy', 'value', 'token', 'reward', 'market'],  # L6_Economy
            7: ['governance', 'rule', 'policy', 'admin', 'control']  # L7_Governance
        }

    def get_layer_from_content(self, file_path: Path) -> int:
        """根據檔案內容判斷所屬層次"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read().lower()
        except (UnicodeDecodeError, OSError):
            # 無法讀取的檔案，根據副檔名判斷
            ext = file_path.suffix.lower()
            if ext in ['.sid', '.key', '.pem']:
                return 4  # 安全層
            elif ext in ['.py', '.js', '.java']:
                return 5  # 互通層
            else:
                return 1  # 預設感知層

        # 根據關鍵字匹配
        max_matches = 0
        best_layer = 1

        for layer, keywords in self.layer_keywords.items():
            matches = sum(1 for keyword in keywords if keyword in content)
            if matches > max_matches:
                max_matches = matches
                best_layer = layer

        return best_layer

    def get_correct_path(self, file_path: Path, layer: int) -> Path:
        """獲取檔案的正確路徑"""
        layer_names = {
            1: 'L1_Perception',
            2: 'L2_Signal',
            3: 'L3_Encoding',
            4: 'L4_Security',
            5: 'L5_Interoperability',
            6: 'L6_Economy',
            7: 'L7_Governance'
        }

        layer_dir = self.root_path / layer_names[layer]
        return layer_dir / file_path.name

    def auto_classify_files(self) -> Dict[str, List[str]]:
        """自動分類檔案到正確層次"""
        results = {'moved': [], 'skipped': []}

        # 掃描根目錄的檔案（不包含子目錄）
        for item in self.root_path.iterdir():
            if item.is_file() and item.name not in ['.clinerules', '.gitignore']:
                layer = self.get_layer_from_content(item)
                correct_path = self.get_correct_path(item, layer)

                if item != correct_path:
                    # 確保目標目錄存在
                    correct_path.parent.mkdir(parents=True, exist_ok=True)

                    try:
                        shutil.move(str(item), str(correct_path))
                        results['moved'].append(f"{item.name} -> {correct_path.relative_to(self.root_path)}")
                    except Exception as e:
                        results['skipped'].append(f"{item.name}: {str(e)}")
                else:
                    results['skipped'].append(f"{item.name}: already in correct location")

        return results

    def validate_architecture(self) -> Tuple[bool, List[str]]:
        """驗證架構完整性"""
        errors = []

        # 檢查 L1-L7 目錄
        layer_names = [f"L{i}_{name}" for i, name in enumerate([
            'Perception', 'Signal', 'Encoding', 'Security',
            'Interoperability', 'Economy', 'Governance'
        ], 1)]

        for layer_name in layer_names:
            if not (self.root_path / layer_name).exists():
                errors.append(f"Missing layer directory: {layer_name}")

        # 檢查生態資源目錄
        ecosystem_dirs = ['docs', 'sdk', 'schemas', 'examples', 'references']
        for dir_name in ecosystem_dirs:
            if not (self.root_path / dir_name).exists():
                errors.append(f"Missing ecosystem directory: {dir_name}")

        # 檢查關鍵檔案
        if not (self.root_path / '.clinerules').exists():
            errors.append("Missing .clinerules file")

        return len(errors) == 0, errors

    def validate_file_naming(self) -> Tuple[bool, List[str]]:
        """驗證檔案命名規範"""
        errors = []

        for file_path in self.root_path.rglob('*'):
            if file_path.is_file():
                # 跳過 .git 目錄和 Legacy_Archive 目錄中的檔案
                if '.git' in file_path.parts or 'Legacy_Archive' in file_path.parts:
                    continue

                filename = file_path.name

                # 跳過特殊檔案
                if filename in ['.clinerules', '.gitignore', 'README.md']:
                    continue

                # 檢查命名格式 (不包括副檔名)
                name_without_ext = filename.rsplit('.', 1)[0] if '.' in filename else filename
                pattern = r'^L[1-7]_\d{8}_[A-Za-z_]+_V\d+$'
                if not re.match(pattern, name_without_ext):
                    errors.append(f"Invalid naming: {file_path.relative_to(self.root_path)}")

        return len(errors) == 0, errors

    def daily_maintenance(self) -> Dict[str, Any]:
        """每日維護任務"""
        report = {
            'timestamp': datetime.now().isoformat(),
            'classification': None,
            'validation': None,
            'cleanup': []
        }

        # 自動分類
        report['classification'] = self.auto_classify_files()

        # 驗證架構
        arch_ok, arch_errors = self.validate_architecture()
        report['validation'] = {'passed': arch_ok, 'errors': arch_errors}

        # 清理空目錄
        for dir_path in self.root_path.rglob('*'):
            if dir_path.is_dir() and not any(dir_path.iterdir()):
                try:
                    dir_path.rmdir()
                    report['cleanup'].append(f"Removed empty directory: {dir_path.relative_to(self.root_path)}")
                except OSError:
                    pass

        return report

def main():
    """主函數"""
    parser = argparse.ArgumentParser(description='Scent-ID OS V31 Auto Map System')
    parser.add_argument('--auto-classify', action='store_true', help='Auto classify files')
    parser.add_argument('--validate', action='store_true', help='Validate architecture')
    parser.add_argument('--validate-naming', action='store_true', help='Validate file naming')
    parser.add_argument('--daily', action='store_true', help='Run daily maintenance')
    parser.add_argument('--test-all', action='store_true', help='Run all tests')

    args = parser.parse_args()
    auto_map = AutoMap()

    if args.auto_classify:
        results = auto_map.auto_classify_files()
        print(f"Files moved: {len(results['moved'])}")
        print(f"Files skipped: {len(results['skipped'])}")

    elif args.validate:
        arch_ok, arch_errors = auto_map.validate_architecture()
        if arch_ok:
            print("Architecture validation passed")
        else:
            print("Architecture validation failed:")
            for error in arch_errors:
                print(f"   {error}")
        sys.exit(0 if arch_ok else 1)

    elif args.validate_naming:
        naming_ok, naming_errors = auto_map.validate_file_naming()
        if naming_ok:
            print("Naming validation passed")
        else:
            print("Naming validation failed:")
            for error in naming_errors:
                print(f"   {error}")
        sys.exit(0 if naming_ok else 1)

    elif args.daily:
        report = auto_map.daily_maintenance()
        print(json.dumps(report, indent=2, ensure_ascii=False))

    elif args.test_all:
        print("Running all tests...")

        # 架構驗證
        arch_ok, arch_errors = auto_map.validate_architecture()
        print(f"Architecture: {'PASS' if arch_ok else 'FAIL'}")
        if not arch_ok:
            for error in arch_errors:
                print(f"  {error}")

        # 命名驗證
        naming_ok, naming_errors = auto_map.validate_file_naming()
        print(f"Naming: {'PASS' if naming_ok else 'FAIL'}")
        if not naming_ok:
            for error in naming_errors:
                print(f"  {error}")

        # 自動分類測試
        results = auto_map.auto_classify_files()
        print(f"Classification: {len(results['moved'])} moved, {len(results['skipped'])} skipped")

        sys.exit(0 if arch_ok and naming_ok else 1)

    else:
        parser.print_help()

if __name__ == '__main__':
    main()