"""
SQLite 持久化層 - 管理檔案上傳紀錄與到期資訊
"""
import sqlite3
import uuid
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional
from dataclasses import dataclass
import threading
import logging

logger = logging.getLogger(__name__)

DATABASE_PATH = Path("file_records.db")


@dataclass
class FileRecord:
    """檔案紀錄資料結構"""
    id: int
    uuid: str
    filename: str
    path: str
    expires_at: datetime
    created_at: datetime


class FileDatabase:
    """檔案紀錄資料庫管理"""
    
    _local = threading.local()
    
    def __init__(self, db_path: Path = DATABASE_PATH):
        self.db_path = db_path
        self._init_db()
    
    def _get_connection(self) -> sqlite3.Connection:
        """取得當前執行緒的資料庫連線（thread-local）"""
        if not hasattr(self._local, 'connection') or self._local.connection is None:
            self._local.connection = sqlite3.connect(
                str(self.db_path),
                check_same_thread=False
            )
            self._local.connection.row_factory = sqlite3.Row
        return self._local.connection
    
    def _init_db(self):
        """初始化資料庫 schema"""
        conn = self._get_connection()
        conn.execute("""
            CREATE TABLE IF NOT EXISTS file_records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                uuid TEXT UNIQUE NOT NULL,
                filename TEXT NOT NULL,
                path TEXT NOT NULL,
                expires_at TIMESTAMP NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.execute("""
            CREATE INDEX IF NOT EXISTS idx_uuid ON file_records(uuid)
        """)
        conn.execute("""
            CREATE INDEX IF NOT EXISTS idx_expires_at ON file_records(expires_at)
        """)
        conn.commit()
        logger.info(f"Database initialized at {self.db_path}")
    
    def create_record(
        self,
        filename: str,
        path: str,
        expire_seconds: int
    ) -> FileRecord:
        """
        建立新的檔案紀錄
        
        Args:
            filename: 原始檔名
            path: 檔案儲存路徑
            expire_seconds: 有效期秒數
            
        Returns:
            FileRecord: 建立的紀錄
        """
        file_uuid = str(uuid.uuid4())
        now = datetime.now()
        expires_at = now + timedelta(seconds=expire_seconds)
        
        conn = self._get_connection()
        cursor = conn.execute(
            """
            INSERT INTO file_records (uuid, filename, path, expires_at, created_at)
            VALUES (?, ?, ?, ?, ?)
            """,
            (file_uuid, filename, path, expires_at.isoformat(), now.isoformat())
        )
        conn.commit()
        
        record = FileRecord(
            id=cursor.lastrowid,
            uuid=file_uuid,
            filename=filename,
            path=path,
            expires_at=expires_at,
            created_at=now
        )
        logger.info(f"Created record: uuid={file_uuid}, filename={filename}, expires_at={expires_at}")
        return record
    
    def get_by_uuid(self, file_uuid: str) -> Optional[FileRecord]:
        """
        根據 UUID 取得紀錄
        
        Args:
            file_uuid: 檔案 UUID
            
        Returns:
            FileRecord 或 None
        """
        conn = self._get_connection()
        row = conn.execute(
            "SELECT * FROM file_records WHERE uuid = ?",
            (file_uuid,)
        ).fetchone()
        
        if row is None:
            return None
        
        return FileRecord(
            id=row['id'],
            uuid=row['uuid'],
            filename=row['filename'],
            path=row['path'],
            expires_at=datetime.fromisoformat(row['expires_at']),
            created_at=datetime.fromisoformat(row['created_at'])
        )
    
    def delete_by_uuid(self, file_uuid: str) -> bool:
        """
        根據 UUID 刪除紀錄
        
        Args:
            file_uuid: 檔案 UUID
            
        Returns:
            是否成功刪除
        """
        conn = self._get_connection()
        cursor = conn.execute(
            "DELETE FROM file_records WHERE uuid = ?",
            (file_uuid,)
        )
        conn.commit()
        deleted = cursor.rowcount > 0
        if deleted:
            logger.info(f"Deleted record: uuid={file_uuid}")
        return deleted
    
    def get_expired_records(self) -> list[FileRecord]:
        """
        取得所有已過期的紀錄
        
        Returns:
            過期紀錄列表
        """
        conn = self._get_connection()
        now = datetime.now().isoformat()
        rows = conn.execute(
            "SELECT * FROM file_records WHERE expires_at <= ?",
            (now,)
        ).fetchall()
        
        return [
            FileRecord(
                id=row['id'],
                uuid=row['uuid'],
                filename=row['filename'],
                path=row['path'],
                expires_at=datetime.fromisoformat(row['expires_at']),
                created_at=datetime.fromisoformat(row['created_at'])
            )
            for row in rows
        ]
    
    def delete_expired_records(self) -> int:
        """
        刪除所有已過期的紀錄
        
        Returns:
            刪除的紀錄數量
        """
        conn = self._get_connection()
        now = datetime.now().isoformat()
        cursor = conn.execute(
            "DELETE FROM file_records WHERE expires_at <= ?",
            (now,)
        )
        conn.commit()
        count = cursor.rowcount
        if count > 0:
            logger.info(f"Deleted {count} expired records")
        return count
    
    def is_expired(self, record: FileRecord) -> bool:
        """檢查紀錄是否已過期"""
        return datetime.now() > record.expires_at
    
    def get_all_records(self) -> list[FileRecord]:
        """取得所有紀錄（用於列表顯示）"""
        conn = self._get_connection()
        rows = conn.execute("SELECT * FROM file_records ORDER BY created_at DESC").fetchall()
        
        return [
            FileRecord(
                id=row['id'],
                uuid=row['uuid'],
                filename=row['filename'],
                path=row['path'],
                expires_at=datetime.fromisoformat(row['expires_at']),
                created_at=datetime.fromisoformat(row['created_at'])
            )
            for row in rows
        ]
    
    def close(self):
        """關閉資料庫連線"""
        if hasattr(self._local, 'connection') and self._local.connection:
            self._local.connection.close()
            self._local.connection = None


# 全域資料庫實例
db: Optional[FileDatabase] = None


def get_db() -> FileDatabase:
    """取得資料庫實例"""
    global db
    if db is None:
        db = FileDatabase()
    return db


def init_db(db_path: Optional[Path] = None):
    """初始化資料庫"""
    global db
    if db_path:
        db = FileDatabase(db_path)
    else:
        db = FileDatabase()
    return db
