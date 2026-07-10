import os
import win32com.client

def batch_convert_excel_to_pdf():
    # 獲取目前 Python 檔案所在的絕對路徑
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 啟動背景 Excel 主程式
    excel = win32com.client.Dispatch("Excel.Application")
    excel.Visible = False        # 讓 Excel 在背景執行，不彈出視窗
    excel.DisplayAlerts = False  # 關閉警告提示
    
    print(f"【開始掃描資料夾】: {current_dir}\n" + "-"*50)
    
    success_count = 0
    
    try:
        # os.walk 會自動深入遍歷當前資料夾與所有子資料夾
        for root, dirs, files in os.walk(current_dir):
            for file in files:
                # 【修正處】使用 file.lower()，這樣不管大寫 .XLSX 還是小寫 .xlsx 都能完美抓到
                if file.lower().endswith(('.xlsx', '.xls')) and not file.startswith('~$'):
                    excel_path = os.path.join(root, file)
                    
                    # 產生同名的 PDF 檔案路徑
                    pdf_name = os.path.splitext(file)[0] + '.pdf'
                    pdf_path = os.path.join(root, pdf_name)
                    
                    print(f"正在轉換: {file} -> {pdf_name}")
                    
                    try:
                        # 開啟活頁簿
                        wb = excel.Workbooks.Open(excel_path)
                        # 0 代表導出為 PDF 格式
                        wb.ExportAsFixedFormat(0, pdf_path)
                        wb.Close(SaveChanges=False)
                        success_count += 1
                    except Exception as e:
                        print(f"❌ 檔案 {file} 轉換失敗，錯誤訊息: {e}")
                        
        print("-"*50 + f"\n【轉換完成】共成功轉換了 {success_count} 個檔案！")
        
    except Exception as e:
        print(f"執行過程中發生嚴重錯誤: {e}")
    finally:
        # 確保關閉背景的 Excel
        excel.Quit()

if __name__ == "__main__":
    batch_convert_excel_to_pdf()
