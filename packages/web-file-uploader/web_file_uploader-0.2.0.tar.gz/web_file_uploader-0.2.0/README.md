# Web File Uploader

一個使用 FastAPI 建構的檔案上傳與限時下載服務，下載路徑含 UUID 前綴、到期自動清除。

## 安裝 uv

如果尚未安裝 uv，請先安裝：

```bash
# 使用 pip 安裝 uv
pip install uv

# 或使用官方安裝腳本
curl -LsSf https://astral.sh/uv/install.sh | sh
```

## 開發和除錯

### 使用虛擬環境開發

1. 安裝依賴到現有的虛擬環境：
   ```bash
   cd web-file-uploader
   & ..\venv\Scripts\Activate.ps1
   # 若 uv 在 Windows 碰到 editable 安裝問題，改用 pip 並關閉隔離
   python -m pip install -e .[dev] --no-build-isolation --config-settings editable_mode=compat
   # 或 uv：uv pip install -e .[dev] --no-build-isolation --config-settings editable_mode=compat
   ```

2. 啟動開發伺服器（支援自動重新載入）：
   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

### 使用 uvx 部署

在專案目錄中執行：

```bash
uvx --from . web-file-uploader
```

這將安裝依賴並啟動 FastAPI 伺服器在 http://localhost:8000

## API 端點（符合 file-expiry 計畫）

- `GET /`: 歡迎訊息和 API 文檔鏈接
- `POST /upload`: 上傳檔案，伺服器統一設定有效期，建立紀錄並回傳下載 URL：`/download/{uuid}/{filename}`
- `GET /download/{uuid}/{filename}`: 依 UUID+檔名驗證，未過期且檔案存在才回傳，否則 404 並清理紀錄/檔案
- `GET /files`: 列出未過期檔案（含下載 URL、到期時間）
- `DELETE /files/{filename}`: 刪除指定檔案

## 設定與行為

- 預設有效期：60 秒，可由 `--expire-seconds` 或環境變數 `EXPIRE_SECONDS` 調整（範圍 10–86400，超界會 clamp）
- 清理排程：預設每 300 秒執行一次，可用 `--cleanup-interval-seconds` 或 `CLEANUP_INTERVAL_SECONDS`（範圍 30–3600）
- 即時清理：下載時若發現過期或檔案缺失即刪除紀錄/檔案
- 持久化：SQLite（自動建立 `file_records.db`），重啟後仍可判斷到期

## 測試

- 執行整合測試：
  ```bash
  python -m pytest tests/integration/test_file_expiry.py -q
  # 或全部測試
  python -m pytest -q
  ```

## API 文檔

啟動伺服器後，訪問 `http://localhost:8000/docs` 查看完整的互動式 API 文檔。
