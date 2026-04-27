import os
import hashlib
from dotenv import load_dotenv
from fpdf import FPDF

# 1. 自動解鎖保險箱 (不需要再打密鑰)
load_dotenv(dotenv_path="../.env")
PRIVATE_KEY = os.getenv("SCENT_ID_PRIVATE_KEY")

# 2. 整合引擎：生號碼 + 印標籤 + 報價格
def run_empire_process(values):
    # --- 生號碼 ---
    gene = "".join(f"{int(x):02X}" for x in values)
    salt = PRIVATE_KEY if PRIVATE_KEY else "GENESIS"
    checksum = hashlib.sha256((gene + salt).encode()).hexdigest()[:4].upper()
    sid = f"SID-#{gene}-{checksum}"
    
    print(f"\n✅ 引擎發動成功！")
    print(f"💎 你的專屬 SID: {sid}")

    # --- 印標籤 (PDF) ---
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "Scent-ID Global Standard Label", 0, 1, "C")
    pdf.ln(10)
    pdf.set_font("Arial", "", 12)
    pdf.multi_cell(0, 10, f"Identity Code:\n{sid}\n\nPerceptual Vectors:\n{values}")
    
    output_path = "03_Application/Scent_Label_Auto.pdf"
    pdf.output(output_path)
    
    # --- 報價格 ---
    print(f"📄 認證標籤已生成: {output_path}")
    print(f"💰 預計授權費: 1 BTC / Year")
    print("="*40)

if __name__ == "__main__":
    # 這裡就是你的「按鈕」：改這 9 個數字，按執行就結束了
    sample_data = [255, 128, 64, 32, 16, 8, 4, 2, 1] 
    run_empire_process(sample_data)