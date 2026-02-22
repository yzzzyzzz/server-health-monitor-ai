import shutil
import os
import requests  # 記得要 pip install requests
import logging
from datetime import datetime
from typing import Dict, Tuple, Optional

# 設定日誌
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('monitor.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def send_line_notify(message: str, retry: int = 3) -> bool:
    """
    這部分對應職缺要求的「整合第三方 LINE」功能
    從環境變數讀取 Token，避免硬編碼
    """
    token = os.getenv("LINE_NOTIFY_TOKEN", "YOUR_LINE_NOTIFY_TOKEN")
    
    if token == "YOUR_LINE_NOTIFY_TOKEN":
        logger.warning("請設定環境變數 LINE_NOTIFY_TOKEN")
        return False
    
    url = "https://notify-api.line.me/api/notify"
    headers = {"Authorization": "Bearer " + token}
    data = {"message": message}
    
    for attempt in range(retry):
        try:
            response = requests.post(url, headers=headers, data=data, timeout=10)
            if response.status_code == 200:
                logger.info("LINE 通知發送成功")
                return True
            else:
                logger.warning(f"LINE 通知發送失敗，狀態碼: {response.status_code}, 回應: {response.text}")
                if attempt < retry - 1:
                    continue
        except requests.exceptions.Timeout:
            logger.error(f"LINE 通知請求超時 (嘗試 {attempt + 1}/{retry})")
        except requests.exceptions.RequestException as e:
            logger.error(f"LINE 通知發送失敗: {e} (嘗試 {attempt + 1}/{retry})")
        except Exception as e:
            logger.error(f"未預期的錯誤: {e}")
    
    return False

def check_disk_usage(path: str = "/") -> Dict[str, float]:
    """
    檢查磁碟使用情況，返回詳細資訊
    """
    try:
        total, used, free = shutil.disk_usage(path)
        percent_used = (used / total) * 100
        
        # 轉換為 GB
        total_gb = total / (1024**3)
        used_gb = used / (1024**3)
        free_gb = free / (1024**3)
        
        return {
            "percent_used": percent_used,
            "total_gb": total_gb,
            "used_gb": used_gb,
            "free_gb": free_gb,
            "path": path
        }
    except Exception as e:
        logger.error(f"檢查磁碟使用率失敗 ({path}): {e}")
        return {
            "percent_used": 0,
            "total_gb": 0,
            "used_gb": 0,
            "free_gb": 0,
            "path": path,
            "error": str(e)
        }

def simulate_ai_diagnosis(usage_percent: float, free_gb: float) -> str:
    """
    根據磁碟使用情況提供 AI 診斷建議
    """
    suggestions = []
    
    if usage_percent >= 95:
        suggestions.append("⚠️ 緊急：磁碟空間嚴重不足！")
        suggestions.append("1. 立即清理大型檔案和日誌")
        suggestions.append("2. 執行 'docker system prune -a --volumes' 清理所有未使用的 Docker 資源")
        suggestions.append("3. 檢查並刪除舊的備份檔案")
    elif usage_percent >= 90:
        suggestions.append("🔴 警告：磁碟空間即將用盡！")
        suggestions.append("1. 執行 'docker system prune' 清理過期鏡像和容器")
        suggestions.append("2. 清理系統日誌：'journalctl --vacuum-time=7d'")
        suggestions.append("3. 檢查 /tmp 和 /var/tmp 目錄")
    elif usage_percent >= 80:
        suggestions.append("🟡 提醒：磁碟使用率偏高")
        suggestions.append("1. 執行 'docker system prune' 清理過期鏡像")
        suggestions.append("2. 檢查並清理應用程式日誌")
        suggestions.append("3. 考慮擴充磁碟容量")
    
    if free_gb < 5:
        suggestions.append(f"⚠️ 剩餘空間僅 {free_gb:.2f} GB，建議立即清理")
    
    if suggestions:
        return "\n🤖 AI 修復建議：\n" + "\n".join(suggestions)
    return ""

def format_size(size_gb: float) -> str:
    """格式化檔案大小顯示"""
    if size_gb >= 1024:
        return f"{size_gb/1024:.2f} TB"
    return f"{size_gb:.2f} GB"

def main():
    """
    主程式：監控磁碟使用率並發送通知
    """
    # 從環境變數讀取配置，或使用預設值
    THRESHOLD = float(os.getenv("DISK_USAGE_THRESHOLD", "80"))
    MONITOR_PATH = os.getenv("MONITOR_PATH", "/")
    
    logger.info(f"開始檢查磁碟使用率 (路徑: {MONITOR_PATH}, 閾值: {THRESHOLD}%)")
    
    # 1. 檢查磁碟
    disk_info = check_disk_usage(MONITOR_PATH)
    
    if "error" in disk_info:
        logger.error("無法取得磁碟資訊，程式結束")
        return
    
    usage = disk_info["percent_used"]
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # 顯示詳細資訊
    status_msg = (
        f"[{timestamp}] 磁碟監控報告\n"
        f"路徑: {disk_info['path']}\n"
        f"使用率: {usage:.2f}%\n"
        f"總容量: {format_size(disk_info['total_gb'])}\n"
        f"已使用: {format_size(disk_info['used_gb'])}\n"
        f"剩餘空間: {format_size(disk_info['free_gb'])}"
    )
    
    logger.info(f"當前磁碟使用率: {usage:.2f}%")
    print(status_msg)
    
    # 2. 判斷是否超過閾值
    if usage > THRESHOLD:
        alert_msg = (
            f"【伺服器警告】\n"
            f"磁碟使用率已達 {usage:.2f}%，超過標準 {THRESHOLD}%！\n\n"
            f"{status_msg}"
        )
        
        # 3. 取得 AI 診斷建議
        advice = simulate_ai_diagnosis(usage, disk_info['free_gb'])
        
        # 4. 發送通知與 AI 建議
        full_report = alert_msg + advice
        print("\n" + "="*50)
        print(full_report)
        print("="*50)
        
        send_line_notify(full_report)
    else:
        logger.info("系統狀態正常")
        print("\n✅ 系統狀態正常")

if __name__ == "__main__":
    main()