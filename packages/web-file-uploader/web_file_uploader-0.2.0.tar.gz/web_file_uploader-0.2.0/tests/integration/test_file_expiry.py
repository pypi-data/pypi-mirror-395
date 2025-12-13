import time
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

import database
import main


@pytest.fixture()
def client(tmp_path, monkeypatch):
    upload_dir = tmp_path / "uploads"
    upload_dir.mkdir()
    db_path = tmp_path / "file_records.db"

    # 初始化獨立的測試資料庫
    database.init_db(db_path)

    def init_db_override():
        return database.init_db(db_path)

    monkeypatch.setattr(main, "UPLOAD_DIR", upload_dir)
    monkeypatch.setattr(main, "init_db", init_db_override)

    # 縮短有效期與清理間隔，加速測試
    main.config.expire_seconds = 2
    main.config.cleanup_interval_seconds = 1

    with TestClient(main.app) as client:
        yield client, upload_dir

    # 測試結束關閉資料庫
    if database.db:
        database.db.close()


def test_upload_and_download_before_expiry(client):
    client, _ = client
    files = {"file": ("hello.txt", b"hello", "text/plain")}
    resp = client.post("/upload", files=files)
    assert resp.status_code == 200
    data = resp.json()
    download_url = data["download_url"]

    # 到期前可下載
    download_resp = client.get(download_url)
    assert download_resp.status_code == 200
    assert download_resp.content == b"hello"


def test_download_after_expiry_returns_404_and_cleans(client):
    client, _ = client
    files = {"file": ("bye.txt", b"bye", "text/plain")}
    resp = client.post("/upload", files=files)
    assert resp.status_code == 200
    data = resp.json()
    download_url = data["download_url"]

    # 取得 uuid 以檢查紀錄
    parts = download_url.split("/")
    file_uuid = parts[2]

    # 等待超過有效期
    time.sleep(3)

    expired_resp = client.get(download_url)
    assert expired_resp.status_code == 404

    db = database.get_db()
    record = db.get_by_uuid(file_uuid)
    # 紀錄應已清除且檔案不存在
    assert record is None or not Path(data["download_url"].replace("/download/", "", 1)).exists()
