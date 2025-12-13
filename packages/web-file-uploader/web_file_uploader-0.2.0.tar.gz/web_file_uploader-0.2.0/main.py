from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import FileResponse
from contextlib import asynccontextmanager
import os
import shutil
import asyncio
import logging
from pathlib import Path
from datetime import datetime

from database import get_db, init_db, FileDatabase
from schemas import UploadResponse

# 設定 logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# 設定參數（由啟動時設定）
class Config:
    expire_seconds: int = 60  # 預設 60 秒
    cleanup_interval_seconds: int = 300  # 預設 5 分鐘
    
config = Config()

# 創建上傳目錄
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)
FILE_NOT_FOUND = "File not found"


def _delete_expired_record(db, record):
    """刪除單一過期紀錄與檔案"""
    file_path = Path(record.path)
    if file_path.exists():
        try:
            file_path.unlink()
            logger.info(f"Deleted expired file: {file_path}")
        except Exception as e:
            logger.error(f"Failed to delete file {file_path}: {e}")
    db.delete_by_uuid(record.uuid)


async def cleanup_expired_files():
    """背景任務：定期清除過期檔案"""
    while True:
        try:
            await asyncio.sleep(config.cleanup_interval_seconds)
            logger.info("Running scheduled cleanup...")
            db = get_db()
            expired_records = db.get_expired_records()
            
            for record in expired_records:
                _delete_expired_record(db, record)
            
            if expired_records:
                logger.info(f"Cleanup completed: removed {len(expired_records)} expired files")
        except asyncio.CancelledError:
            logger.info("Cleanup task cancelled")
            raise  # 重新拋出以正確結束任務
        except Exception as e:
            logger.error(f"Cleanup task error: {e}")
            # 不重試，等下一輪排程


@asynccontextmanager
async def lifespan(app: FastAPI):
    """應用程式生命週期管理"""
    # 啟動時初始化資料庫
    init_db()
    logger.info(f"Server started with expire_seconds={config.expire_seconds}, cleanup_interval={config.cleanup_interval_seconds}")
    
    # 啟動背景清除任務
    cleanup_task = asyncio.create_task(cleanup_expired_files())
    
    yield
    
    # 關閉時取消背景任務
    cleanup_task.cancel()
    try:
        await cleanup_task
    except asyncio.CancelledError:
        pass  # 預期的取消，不需重新拋出
    logger.info("Server shutdown complete")


app = FastAPI(
    title="Web File Uploader",
    description="A file uploader with expiry and secure download URLs",
    lifespan=lifespan
)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Web File Uploader API", "docs": "/docs"}

@app.post("/upload", response_model=UploadResponse)
async def upload_file(file: UploadFile = File(...)):
    """
    上傳單一檔案
    
    回傳包含 UUID 的安全下載連結，檔案在設定的有效期後自動刪除。
    """
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file provided")

    # 檢查檔案類型（可選）
    allowed_extensions = {'.txt', '.pdf', '.jpg', '.jpeg', '.png', '.gif', '.zip', '.docx', '.doc', '.ppt', '.pptx'}
    file_extension = Path(file.filename).suffix.lower()

    if file_extension not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail=f"File type not allowed. Allowed types: {', '.join(allowed_extensions)}"
        )

    # 儲存檔案
    file_path = UPLOAD_DIR / file.filename
    try:
        with file_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save file: {str(e)}")

    # 建立資料庫紀錄
    db = get_db()
    record = db.create_record(
        filename=file.filename,
        path=str(file_path),
        expire_seconds=config.expire_seconds
    )

    return UploadResponse(
        message="File uploaded successfully",
        filename=file.filename,
        size=file_path.stat().st_size,
        download_url=f"/download/{record.uuid}/{file.filename}",
    )

@app.get("/files")
def list_files():
    """
    列出已上傳且未過期的檔案
    """
    db = get_db()
    records = db.get_all_records()
    now = datetime.now()
    
    files = []
    for record in records:
        if record.expires_at > now:  # 只顯示未過期的
            file_path = Path(record.path)
            if file_path.exists():
                files.append({
                    "filename": record.filename,
                    "size": file_path.stat().st_size,
                    "download_url": f"/download/{record.uuid}/{record.filename}",
                    "expires_at": record.expires_at.isoformat(),
                    "created_at": record.created_at.isoformat()
                })

    return {"files": files}


def cleanup_record_and_file(db: FileDatabase, record, file_path: Path):
    """清理紀錄與檔案的輔助函式"""
    if file_path.exists():
        try:
            file_path.unlink()
            logger.info(f"Deleted file: {file_path}")
        except Exception as e:
            logger.error(f"Failed to delete file {file_path}: {e}")
    db.delete_by_uuid(record.uuid)


@app.get("/download/{file_uuid}/{filename}")
async def download_file(file_uuid: str, filename: str):
    """
    下載指定檔案
    
    透過 UUID 和檔名驗證下載請求，若過期或不存在則返回 404。
    """
    db = get_db()
    record = db.get_by_uuid(file_uuid)
    
    # 紀錄不存在
    if record is None:
        raise HTTPException(status_code=404, detail=FILE_NOT_FOUND)
    
    # 檔名不匹配
    if record.filename != filename:
        raise HTTPException(status_code=404, detail=FILE_NOT_FOUND)
    
    file_path = Path(record.path)
    
    # 檢查是否過期
    if db.is_expired(record):
        logger.info(f"File expired: {file_uuid}/{filename}")
        cleanup_record_and_file(db, record, file_path)
        raise HTTPException(status_code=404, detail="File has expired")
    
    # 檢查檔案是否存在
    if not file_path.exists():
        logger.warning(f"File missing but record exists: {file_uuid}/{filename}")
        db.delete_by_uuid(file_uuid)
        raise HTTPException(status_code=404, detail=FILE_NOT_FOUND)

    return FileResponse(
        path=file_path,
        filename=filename,
        media_type='application/octet-stream'
    )

@app.delete("/files/{filename}")
def delete_file(filename: str):
    """
    刪除指定檔案
    """
    file_path = UPLOAD_DIR / filename
    if not file_path.exists():
        raise HTTPException(status_code=404, detail=FILE_NOT_FOUND)

    try:
        file_path.unlink()
        return {"message": f"File {filename} deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete file: {str(e)}")

def clamp(value: int, min_val: int, max_val: int) -> int:
    """將值限制在指定範圍內"""
    return max(min_val, min(value, max_val))


def main():
    import argparse
    import uvicorn

    parser = argparse.ArgumentParser(description="Web File Uploader FastAPI Server")
    parser.add_argument("--host", default="0.0.0.0", help="Host to bind the server to (default: 0.0.0.0)")
    parser.add_argument("--port", type=int, default=8000, help="Port to bind the server to (default: 8000)")
    parser.add_argument(
        "--expire-seconds",
        type=int,
        default=int(os.environ.get("EXPIRE_SECONDS", 60)),
        help="File expiry time in seconds (default: 60, range: 10-86400)"
    )
    parser.add_argument(
        "--cleanup-interval-seconds",
        type=int,
        default=int(os.environ.get("CLEANUP_INTERVAL_SECONDS", 300)),
        help="Cleanup interval in seconds (default: 300, range: 30-3600)"
    )

    args = parser.parse_args()
    
    # 驗證並 clamp 參數範圍
    config.expire_seconds = clamp(args.expire_seconds, 10, 86400)
    config.cleanup_interval_seconds = clamp(args.cleanup_interval_seconds, 30, 3600)
    
    if args.expire_seconds != config.expire_seconds:
        logger.warning(f"expire_seconds clamped from {args.expire_seconds} to {config.expire_seconds}")
    if args.cleanup_interval_seconds != config.cleanup_interval_seconds:
        logger.warning(f"cleanup_interval_seconds clamped from {args.cleanup_interval_seconds} to {config.cleanup_interval_seconds}")

    uvicorn.run(app, host=args.host, port=args.port)

if __name__ == "__main__":
    main()
