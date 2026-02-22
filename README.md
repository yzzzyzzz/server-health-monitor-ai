# 磁碟監控腳本

自動監控伺服器磁碟使用率，當超過閾值時發送 LINE Notify 通知。

## 功能特色

✅ **環境變數配置** - Token 和設定透過環境變數管理，避免硬編碼  
✅ **詳細日誌記錄** - 自動記錄到 `monitor.log` 檔案  
✅ **重試機制** - LINE 通知發送失敗時自動重試  
✅ **詳細磁碟資訊** - 顯示總容量、已用、剩餘空間  
✅ **智能 AI 診斷** - 根據不同使用率提供對應的修復建議  
✅ **時間戳記** - 所有訊息包含時間資訊  
✅ **錯誤處理** - 完善的異常處理和狀態檢查  

## 安裝需求

Python 3.7+

### 安裝依賴套件

```bash
pip install -r requirements.txt
```

或單獨安裝：

```bash
pip install requests
```

## 設定方式

1. 複製環境變數範例檔案：
```bash
cp .env.example .env
```

2. 編輯 `.env` 檔案，填入你的 LINE Notify Token：
```
LINE_NOTIFY_TOKEN=你的實際Token
DISK_USAGE_THRESHOLD=80
MONITOR_PATH=/
```

3. 載入環境變數（Windows PowerShell）：
```powershell
# 讀取 .env 檔案並設定環境變數
Get-Content .env | ForEach-Object {
    if ($_ -match '^([^=]+)=(.*)$') {
        [Environment]::SetEnvironmentVariable($matches[1], $matches[2], "Process")
    }
}
```

或使用 `python-dotenv`：
```bash
pip install python-dotenv
```

然後在程式碼開頭加入：
```python
from dotenv import load_dotenv
load_dotenv()
```

## 使用方法

直接執行：
```bash
python monitor.py
```

或設定為定時任務（cron）：
```bash
# 每小時檢查一次
0 * * * * cd /path/to/script && python monitor.py
```

## 輸出範例

### 正常狀態
```
[2026-02-22 10:30:00] 磁碟監控報告
路徑: /
使用率: 65.23%
總容量: 500.00 GB
已使用: 326.15 GB
剩餘空間: 173.85 GB

✅ 系統狀態正常
```

### 警告狀態
```
[2026-02-22 10:30:00] 磁碟監控報告
路徑: /
使用率: 85.50%
總容量: 500.00 GB
已使用: 427.50 GB
剩餘空間: 72.50 GB

==================================================
【伺服器警告】
磁碟使用率已達 85.50%，超過標準 80%！

[2026-02-22 10:30:00] 磁碟監控報告
路徑: /
使用率: 85.50%
總容量: 500.00 GB
已使用: 427.50 GB
剩餘空間: 72.50 GB

🤖 AI 修復建議：
🟡 提醒：磁碟使用率偏高
1. 執行 'docker system prune' 清理過期鏡像
2. 檢查並清理應用程式日誌
3. 考慮擴充磁碟容量
==================================================
```

## 日誌檔案

所有執行記錄會自動儲存到 `monitor.log` 檔案中。

## 安全注意事項

⚠️ **重要**：請勿將包含真實 Token 的 `.env` 檔案提交到 Git！

- ✅ `.env.example` 是範例檔案，可以安全提交
- ❌ `.env` 檔案已加入 `.gitignore`，不會被提交
- 🔒 請妥善保管你的 LINE Notify Token

## 授權

本專案採用 MIT 授權。

## 貢獻

歡迎提交 Issue 或 Pull Request！

## 改進項目

- ✅ Token 從環境變數讀取，避免硬編碼
- ✅ 添加完整的日誌記錄功能
- ✅ 改進錯誤處理和 HTTP 響應檢查
- ✅ 支援環境變數配置（閾值、路徑）
- ✅ 返回更詳細的磁碟資訊（總容量、已用、剩餘）
- ✅ 添加時間戳記
- ✅ 改進 AI 診斷功能，根據不同情況給出對應建議
- ✅ 添加重試機制（預設 3 次）
- ✅ 添加請求超時設定（10 秒）
