import os, hashlib, sys
from fpdf import FPDF

# --- [自動化核心：鎖定三層結構] ---
# 無論你在哪裡執行，它都會自動定位到 Scent_ID_OS 根目錄
PROTOCOL_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(PROTOCOL_DIR)
os.chdir(BASE_DIR)

# 定義標準三層路徑
DIR_01 = os.path.join(BASE_DIR, "01_Constitution")
DIR_02 = os.path.join(BASE_DIR, "02_Protocol")
DIR_03 = os.path.join(BASE_DIR, "03_Application")

# 確保資料夾存在（強迫症友善，絕對整齊）
for d in [DIR_01, DIR_02, DIR_03]:
    os.makedirs(d, exist_ok=True)

class ScentID_Master_Cert(FPDF):
    def header(self):
        # 恢復圖號 7 的高級感：深色科技邊框
        self.set_line_width(1.5)
        self.rect(5, 5, 200, 287)
        self.set_fill_color(26, 32, 44)
        self.rect(10, 10, 190, 45, 'F')
        self.set_text_color(255, 255, 255)
        self.set_font("Arial", "B", 24)
        self.cell(0, 25, "SCENT-ID GLOBAL PROTOCOL", 0, 1, 'C')
        self.set_font("Arial", "I", 11)
        self.cell(0, -5, "Universal Identity & Asset Verification", 0, 1, 'C')

def main():
    print("="*50)
    print("💎 Scent-ID 帝國核心：正在執行『三層歸位』生成程序...")
    
    # 執行資產生成邏輯
    sid = f"SID-#{hashlib.sha256(b'JAY_EMPIRE').hexdigest()[:16].upper()}"
    
    pdf = ScentID_Master_Cert()
    pdf.add_page()
    pdf.ln(30)
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, f"Identity Code: {sid}", 0, 1)
    
    # 宣告憲法價值 (中英對照)
    pdf.ln(10)
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "Imperial Declaration / 帝國宣告:", 0, 1)
    declarations = [
        "1. Scent is Information. (氣味即信息)",
        "2. Infrastructure of the New Era. (新時代的基礎設施)",
        "3. Absolute Ownership. (絕對所有權)"
    ]
    pdf.set_font("Arial", "", 12)
    for line in declarations:
        pdf.cell(0, 9, f" - {line}", 0, 1)

    # --- [關鍵：噴射到 03_Application] ---
    output_path = os.path.join(DIR_03, "Scent_Final_Certificate.pdf")
    pdf.output(output_path)
    
    print(f"✅ 生成完畢！")
    print(f"📂 憲法保存在：01_Constitution")
    print(f"📄 證書已噴入：03_Application")
    print("="*50)

if __name__ == "__main__":
    main()