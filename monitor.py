import shutil
import os

def check_disk_usage(path="/"):
    # 取得磁碟使用量
    total, used, free = shutil.disk_usage(path)
    percent_used = (used / total) * 100
    return percent_used

def simulate_ai_diagnosis(error_msg):
    # 這裡模擬串接 ChatGPT API 的邏輯
    # 在 GitHub README 中可以說明：這是預留串接 OpenAI API 的接口
    return f"AI 建議修復方案：偵測到 '{error_msg}'，請檢查日誌並清理舊的 Docker 鏡像。"

def main():
    # 1. 檢查磁碟 (對應你履歷中的磁碟管理能力 [cite: 83])
    usage = check_disk_usage()
    print(f"當前磁碟使用率: {usage:.2f}%")

    # 2. 判斷是否異常 (定義 SOP 邏輯 )
    THRESHOLD = 80
    if usage > THRESHOLD:
        print("【告警】磁碟空間不足！")
        # 3. 觸發 AI 診斷 (展現 AI 協作開發能力)
        advice = simulate_ai_diagnosis("Disk usage exceeded threshold")
        print(advice)
    else:
        print("系統狀態正常。")

if __name__ == "__main__":
    main()