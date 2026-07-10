import os
import win32com.client

def batch_convert_excel_to_pdf():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 啟動背景 Excel 主程式
    excel = win32com.client.Dispatch("Excel.Application")
    
    # === 【效能優化四核心組合包】 ===
    excel.Visible = False         # 1. 隱藏視窗
    excel.DisplayAlerts = False   # 2. 關閉警告彈窗
    excel.ScreenUpdating = False  # 3. 徹底禁止螢幕更新（加速核心）
    excel.EnableEvents = False    # 4. 禁用 Excel 事件（防止檔案內建的巨集干擾自動執行）
    
    print(f"【開始高速掃描與轉換】: {current_dir}\n" + "-"*50)
    
    success_count = 0
    
    try:
        for root, dirs, files in os.walk(current_dir):
            for file in files:
                if file.lower().endswith(('.xlsx', '.xls')) and not file.startswith('~$'):
                    excel_path = os.path.join(root, file)
                    pdf_name = os.path.splitext(file)[0] + '.pdf'
                    pdf_path = os.path.join(root, pdf_name)
                    
                    print(f"正在轉換: {file} -> {pdf_name}")
                    
                    try:
                        wb = excel.Workbooks.Open(excel_path)
                        wb.ExportAsFixedFormat(0, pdf_path)
                        wb.Close(SaveChanges=False)
                        success_count += 1
                    except Exception as e:
                        print(f"❌ 檔案 {file} 轉換失敗: {e}")
                        
        print("-"*50 + f"\n【轉換完成】共成功轉換了 {success_count} 個檔案！")
        
    except Exception as e:
        print(f"執行過程中發生嚴重錯誤: {e}")
    finally:
        # 結束後務必恢復設定，並關閉 Excel 處理程序
        try:
            excel.ScreenUpdating = True
            excel.EnableEvents = True
        except:
            pass
        excel.Quit()

if __name__ == "__main__":
    batch_convert_excel_to_pdf()
