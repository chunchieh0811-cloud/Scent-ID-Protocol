#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
L3_20260429_Encoding_Engine_V1.py
Scent-ID OS V31 L3 編碼引擎

功能:
- 256維向量編碼與解碼
- SID-18 格式轉換
- 特徵向量壓縮
- 編碼效能優化

作者: Scent-ID OS V31 L3 編碼層
版本: V1.0
日期: 2026-04-29
"""

import os
import numpy as np
import hashlib
import secrets
from typing import List, Dict, Any, Optional, Tuple
from pathlib import Path
import json

class ScentEncodingEngine:
    """Scent-ID 編碼引擎 - L3 層核心"""

    def __init__(self, vector_dim: int = 256):
        self.vector_dim = vector_dim
        self.sid_length = 18  # SID-18 格式
        self.compression_ratio = 0.75  # 向量壓縮比例

    def generate_feature_vector(self, data: str, salt: Optional[str] = None) -> np.ndarray:
        """從輸入數據生成 256 維特徵向量

        編碼邏輯:
        1. 數據 + 鹽值雜湊
        2. 使用確定性方法生成向量
        3. 正規化到 [0,1] 區間
        """
        if salt:
            combined_data = f"{data}:{salt}"
        else:
            combined_data = data

        # 生成多個雜湊來填充向量
        vector = np.zeros(self.vector_dim)

        for i in range(self.vector_dim):
            # 為每個維度生成不同的雜湊
            dim_data = f"{combined_data}:{i}"
            hash_obj = hashlib.sha256(dim_data.encode('utf-8'))
            hash_bytes = hash_obj.digest()

            # 使用雜湊的前 4 位元組作為浮點數種子
            seed_val = int.from_bytes(hash_bytes[:4], byteorder='big') % (2**32 - 1)
            np.random.seed(seed_val)

            # 生成確定性隨機值
            vector[i] = np.random.rand()

        # 正規化到 [0,1]
        vector = np.clip(vector, 0, 1)

        return vector

    def compress_vector(self, vector: np.ndarray) -> np.ndarray:
        """壓縮向量以減少儲存空間"""
        # 使用 PCA-like 壓縮 (簡化版本)
        compressed_dim = int(self.vector_dim * self.compression_ratio)

        # 簡單的維度減少 (實際應使用更複雜的壓縮演算法)
        compressed = vector[:compressed_dim]

        return compressed

    def vector_to_sid18(self, vector: np.ndarray) -> str:
        """將向量轉換為 SID-18 格式"""
        # 將向量轉換為位元組
        vector_bytes = vector.tobytes()

        # 再次雜湊以獲得固定長度
        hash_obj = hashlib.sha256(vector_bytes)
        hash_hex = hash_obj.hexdigest()

        # 取前 18 字元作為 SID
        sid_18 = hash_hex[:self.sid_length].upper()

        return sid_18

    def sid18_to_vector(self, sid: str) -> np.ndarray:
        """從 SID-18 還原近似向量 (有損壓縮)"""
        if len(sid) != self.sid_length:
            raise ValueError(f"SID 長度必須為 {self.sid_length} 字元")

        # 將 SID 轉換為位元組
        sid_bytes = sid.lower().encode('utf-8')

        # 使用 SID 作為種子重新生成向量
        seed_value = int.from_bytes(sid_bytes[:4], byteorder='big') % (2**32 - 1)
        np.random.seed(seed_value)

        # 生成近似原始向量
        vector = np.random.rand(self.vector_dim)

        # 正規化
        vector = np.clip(vector, 0, 1)

        return vector

    def encode_scent(self, scent_data: str, metadata: Optional[Dict[str, Any]] = None, salt: Optional[str] = None) -> Dict[str, Any]:
        """編碼氣味數據為 Scent-ID

        完整編碼流程:
        1. 生成 256 維特徵向量
        2. 可選壓縮向量
        3. 生成 SID-18
        4. 附加元數據
        """
        # 生成特徵向量
        feature_vector = self.generate_feature_vector(scent_data, salt)

        # 壓縮向量 (用於儲存)
        compressed_vector = self.compress_vector(feature_vector)

        # 生成 SID-18
        sid = self.vector_to_sid18(feature_vector)

        # 編碼結果
        encoded_data = {
            'sid': sid,
            'vector_dim': self.vector_dim,
            'compressed_dim': len(compressed_vector),
            'compression_ratio': self.compression_ratio,
            'algorithm': 'L3-Encoding-V1',
            'timestamp': np.datetime64('now').astype(str),
            'metadata': metadata or {}
        }

        # 儲存壓縮向量 (以 JSON 格式)
        encoded_data['compressed_vector'] = compressed_vector.tolist()

        return encoded_data

    def decode_scent(self, encoded_data: Dict[str, Any]) -> Dict[str, Any]:
        """從編碼數據解碼氣味信息"""
        sid = encoded_data.get('sid')
        if not sid:
            raise ValueError("編碼數據中缺少 SID")

        # 從 SID 還原近似向量
        restored_vector = self.sid18_to_vector(sid)

        # 從壓縮向量恢復 (如果有)
        compressed_vector = encoded_data.get('compressed_vector')
        if compressed_vector:
            compressed_array = np.array(compressed_vector)
            # 簡單的向量重建 (實際應使用反壓縮演算法)
            restored_vector[:len(compressed_array)] = compressed_array

        decoded_data = {
            'sid': sid,
            'restored_vector': restored_vector.tolist(),
            'vector_dim': len(restored_vector),
            'algorithm': encoded_data.get('algorithm', 'Unknown'),
            'timestamp': encoded_data.get('timestamp'),
            'metadata': encoded_data.get('metadata', {})
        }

        return decoded_data

    def validate_encoding(self, original_data: str, encoded_data: Dict[str, Any]) -> Dict[str, Any]:
        """驗證編碼正確性"""
        sid = encoded_data.get('sid')

        # 重新編碼原始數據
        re_encoded = self.encode_scent(original_data)

        # 比較 SID
        sid_match = sid == re_encoded['sid']

        # 計算向量相似度 (餘弦相似度)
        original_vector = self.generate_feature_vector(original_data)
        restored_vector = np.array(encoded_data.get('compressed_vector', []))

        if len(restored_vector) > 0:
            # 填充到完整維度進行比較
            full_restored = np.zeros(self.vector_dim)
            full_restored[:len(restored_vector)] = restored_vector

            # 計算餘弦相似度
            dot_product = np.dot(original_vector, full_restored)
            norm_original = np.linalg.norm(original_vector)
            norm_restored = np.linalg.norm(full_restored)

            if norm_original > 0 and norm_restored > 0:
                similarity = dot_product / (norm_original * norm_restored)
            else:
                similarity = 0.0
        else:
            similarity = 0.0

        validation_result = {
            'sid_match': sid_match,
            'vector_similarity': float(similarity),
            'encoding_valid': sid_match and similarity > 0.8,  # 80% 相似度閾值
            'original_sid': re_encoded['sid'],
            'stored_sid': sid
        }

        return validation_result

def main():
    """測試編碼引擎"""
    engine = ScentEncodingEngine()

    # 測試數據
    test_scent = "玫瑰花香混合茉莉"

    print("=== L3 編碼引擎測試 ===")
    print(f"測試數據: {test_scent}")

    # 編碼
    encoded = engine.encode_scent(test_scent, {"type": "flower", "intensity": 0.8})
    print(f"生成 SID: {encoded['sid']}")
    print(f"向量維度: {encoded['vector_dim']}")
    print(f"壓縮維度: {encoded['compressed_dim']}")

    # 解碼
    decoded = engine.decode_scent(encoded)
    print(f"解碼 SID: {decoded['sid']}")

    # 驗證
    validation = engine.validate_encoding(test_scent, encoded)
    print(f"SID 匹配: {validation['sid_match']}")
    print(f"向量相似度: {validation['vector_similarity']:.4f}")
    print(f"編碼有效: {validation['encoding_valid']}")

if __name__ == '__main__':
    main()