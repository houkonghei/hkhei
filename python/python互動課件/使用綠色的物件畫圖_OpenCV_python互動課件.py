import cv2
import numpy as np

def main():
    # 1. 開啟視訊鏡頭
    cap = cv2.VideoCapture(0)

    # 預設追蹤顏色範圍 (以「鮮綠色」物體為例)
    # HSV 範圍：H (色相 0-179), S (飽和度 0-255), V (明度 0-255)
    lower_color = np.array([35, 80, 80])
    upper_color = np.array([85, 255, 255])

    # 畫筆顏色選單 (BGR 格式)
    colors = [
        (255, 0, 0),     # 藍色
        (0, 255, 0),     # 綠色
        (0, 0, 255),     # 紅色
        (0, 255, 255)    # 黃色
    ]
    color_index = 0
    brush_thickness = 6

    # 畫布與前一幀點位初始化
    canvas = None
    prev_point = None

    print("=== 魔法空氣畫板啟動 ===")
    print("請拿著綠色物品在鏡頭前移動繪圖。按 'q' 退出程式。")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # 鏡像翻轉畫面，讓操作更直覺
        frame = cv2.flip(frame, 1)
        h, w, _ = frame.shape

        # 動態建立與鏡頭同尺寸的黑色畫布
        if canvas is None:
            canvas = np.zeros_like(frame)

        # 2. 顏色轉換與遮罩處理
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, lower_color, upper_color)

        # 降噪：腐蝕與膨脹處理
        mask = cv2.erode(mask, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)

        # 3. 尋找目標物體輪廓
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        curr_point = None

        if contours:
            # 取得面積最大的輪廓
            c = max(contours, key=cv2.contourArea)
            if cv2.contourArea(c) > 500:  # 過濾太小的雜訊
                ((x, y), radius) = cv2.minEnclosingCircle(c)
                M = cv2.moments(c)
                
                if M["m00"] != 0:
                    # 計算中心點（質心）
                    center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
                    curr_point = center

                    # 標註當前追蹤到的目標物體
                    cv2.circle(frame, (int(x), int(y)), int(radius), (255, 255, 255), 2)
                    cv2.circle(frame, center, 5, (0, 0, 0), -1)

                    # 4. 互動邏輯：判斷中心點是否觸碰頂部虛擬按鈕區域 (Y < 60)
                    if center[1] < 60:
                        prev_point = None  # 進入選單區時中斷畫線
                        
                        if 10 <= center[0] <= 110:       # 清除按鈕
                            canvas = np.zeros_like(frame)
                        elif 130 <= center[0] <= 210:    # 藍色
                            color_index = 0
                        elif 230 <= center[0] <= 310:    # 綠色
                            color_index = 1
                        elif 330 <= center[0] <= 410:    # 紅色
                            color_index = 2
                        elif 430 <= center[0] <= 510:    # 黃色
                            color_index = 3
                    else:
                        # 在畫布區域移動時繪製連續線段
                        if prev_point is not None:
                            cv2.line(canvas, prev_point, curr_point, colors[color_index], brush_thickness)

        prev_point = curr_point

        # 5. 將畫布筆劃疊加至攝影機即時畫面
        frame = cv2.add(frame, canvas)

        # 6. 繪製頂部虛擬 UI 按鈕
        # 清除畫布按鈕
        cv2.rectangle(frame, (10, 10), (110, 60), (200, 200, 200), -1)
        cv2.putText(frame, "CLEAR", (25, 42), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)

        # 色彩選擇按鈕
        btn_colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (0, 255, 255)]
        btn_labels = ["BLUE", "GREEN", "RED", "YELLOW"]
        btn_x_starts = [130, 230, 330, 430]

        for idx in range(4):
            x1 = btn_x_starts[idx]
            cv2.rectangle(frame, (x1, 10), (x1 + 80, 60), btn_colors[idx], -1)
            # 當前選取的顏色加粗外框
            if idx == color_index:
                cv2.rectangle(frame, (x1, 10), (x1 + 80, 60), (255, 255, 255), 3)
            
            text_color = (0, 0, 0) if idx == 3 else (255, 255, 255)
            cv2.putText(frame, btn_labels[idx], (x1 + 10, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.45, text_color, 2)

        # 顯示最終畫面
        cv2.imshow("Air Canvas - Interactive OpenCV", frame)

        # 按鍵控制
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('c'):
            canvas = np.zeros_like(frame)

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()