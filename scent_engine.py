import hashlib

def generate_scent_id(recipe_dict):
    """
    Scent-ID 1.0 核心演算法
    第一性原理：將物理配方轉化為唯一數位味號
    """
    # 1. 數據標準化：排序配方確保唯一性
    raw_data = str(sorted(recipe_dict.items())).encode()
    
    # 2. 加密映射：生成 12 位唯一識別碼 (SHA-256)
    scent_hash = hashlib.sha256(raw_data).hexdigest()[:12].upper()
    
    return f"SID-{scent_hash}"

# 系統自我檢查模組
if __name__ == "__main__":
    # 範例：50% 玫瑰基底 (S-001) + 50% 檀香基底 (S-045)
    sample_recipe = {"S-001": 0.5, "S-045": 0.5}
    test_id = generate_scent_id(sample_recipe)
    print(f"Verified Scent-ID: {test_id}")
