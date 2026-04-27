import os
import hashlib
from dotenv import load_dotenv
try:
    from fpdf import FPDF
except ImportError:
    print("❌ 偵測到未安裝 FPDF，正在自動修復中...請稍後重新執行。")
    os.system('pip install fpdf')

# 1. 自動定位保險箱 (向上找兩層確保安全)
load_dotenv(dotenv_path="../.env")
PRIVATE_KEY = os.getenv("SCENT_ID_PRIVATE_KEY", "GENESIS_KEY_000")

# 2. 自動確保「應用層」資料夾存在
os.makedirs("03_Application", exist_ok=True)

def run_one_click_empire(values):
    # --- 生成 SID ---
    gene = "".join(f"{int(x):02X}" for x in values)
    checksum = hashlib.sha256((gene + PRIVATE_KEY).encode()).hexdigest()[:4].upper()
    sid = f"SID-#{gene}-{checksum}"
    
    print("="*40)
    print(f"✅ 身份識別碼已鎖定: {sid}")

    # --- 生成 PDF 標籤 ---
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, 'Scent-ID Global Standard', 0, 1, 'C')
    pdf.ln(10)
    pdf.set_font("Arial", "", 12)
    pdf.cell(0, 10, f"ID: {sid}", 0, 1)
    pdf.cell(0, 10, f"Vectors: {values}", 0, 1)
    
    save_path = "03_Application/Scent_Label_Latest.pdf"
    pdf.output(save_path)
    
    print(f"📄 標籤已存入: {save_path}")
    print(f"💰 授權狀態: 已掛勾錢母 {PRIVATE_KEY[:6]}...")
    print("="*40)

if __name__ == "__main__":
    # 指揮官只需改這裡：
    my_values = [255, 128, 64, 32, 16, 8, 4, 2, 1]
    run_one_click_empire(my_values)