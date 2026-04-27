from fpdf import FPDF
import os

# 1. 設定標籤產線
class ScentLabel(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 16)
        self.cell(0, 10, 'Scent-ID Global Standard Label', 0, 1, 'C')
        self.ln(5)

# 2. 模擬抓取剛才生成的數據
def create_pdf_label(sid, values):
    pdf = ScentLabel()
    pdf.add_page()
    
    # 標籤邊框
    pdf.rect(10, 10, 190, 100)
    
    # 核心資訊
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, f"Identity Code: {sid}", 0, 1)
    
    pdf.set_font('Arial', '', 10)
    pdf.multi_cell(0, 10, f"Sensory Profile (9-Vectors): \n{values}")
    
    pdf.ln(10)
    pdf.set_font('Arial', 'I', 8)
    pdf.cell(0, 10, "Verified by Scent-ID Global Protocol V2.0", 0, 1, 'R')
    
    # 存檔至 03_Application
    output_path = "03_Application/Scent_Label_Sample.pdf"
    pdf.output(output_path)
    print(f"✅ 標籤已產出：{output_path}")

# 執行產線
if __name__ == "__main__":
    current_sid = "SID-#FF8040201008040201-9C3E" # 這是你截圖中的結果
    current_values = "R:255, O:128, Y:64, G:32, B:16, I:8, V:4, W:2, K:1"
    create_pdf_label(current_sid, current_values)