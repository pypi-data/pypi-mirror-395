from pydantic import BaseModel


class UploadResponse(BaseModel):
    message: str
    filename: str
    size: int
    download_url: str
