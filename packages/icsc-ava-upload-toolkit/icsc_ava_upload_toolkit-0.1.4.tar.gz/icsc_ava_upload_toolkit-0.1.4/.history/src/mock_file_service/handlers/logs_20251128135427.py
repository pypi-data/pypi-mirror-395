"""
日誌管理 API
模擬 Node.js AVA File Service 的日誌端點
"""

import logging
from pathlib import Path

from fastapi import APIRouter, File, UploadFile, Body
from fastapi.responses import FileResponse, JSONResponse

from ..config import MockConfig

logger = logging.getLogger(__name__)
router = APIRouter(tags=["Logs"])


@router.get("/list-logs")
async def list_logs():
    """
    列出日誌檔案
    
    對應 Node.js 端點: GET /list-logs
    """
    try:
        storage_dir = MockConfig.ensure_storage_dirs()
        logs_dir = storage_dir / "logs"
        
        if not logs_dir.exists():
            return {"success": True, "logs": []}
        
        logs = []
        for f in logs_dir.iterdir():
            if f.is_file():
                stat = f.stat()
                logs.append({
                    "name": f.name,
                    "size": stat.st_size,
                    "created": stat.st_ctime,
                    "modified": stat.st_mtime
                })
        
        return {"success": True, "logs": logs}
        
    except Exception as e:
        logger.error(f"List logs error: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={"success": False, "error": str(e)}
        )


@router.post("/upload-log")
async def upload_log(file: UploadFile = File(...)):
    """
    上傳日誌檔案
    
    對應 Node.js 端點: POST /upload-log
    """
    try:
        storage_dir = MockConfig.ensure_storage_dirs()
        logs_dir = storage_dir / "logs"
        logs_dir.mkdir(parents=True, exist_ok=True)
        
        filename = file.filename or "unnamed_log.log"
        target_path = logs_dir / filename
        
        content = await file.read()
        with open(target_path, "wb") as f:
            f.write(content)
        
        logger.info(f"Log file uploaded: {filename}")
        
        return {
            "success": True,
            "file": {
                "name": filename,
                "size": len(content)
            }
        }
        
    except Exception as e:
        logger.error(f"Upload log error: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={"success": False, "error": str(e)}
        )


@router.post("/download-log")
async def download_log(filename: str = Body(..., embed=True)):
    """
    下載日誌檔案
    
    對應 Node.js 端點: POST /download-log
    """
    try:
        storage_dir = MockConfig.ensure_storage_dirs()
        file_path = storage_dir / "logs" / filename
        
        if not file_path.exists():
            return JSONResponse(
                status_code=404,
                content={"success": False, "error": "Log file not found"}
            )
        
        logger.info(f"Log file download: {filename}")
        
        return FileResponse(
            path=file_path,
            filename=filename,
            media_type="text/plain"
        )
        
    except Exception as e:
        logger.error(f"Download log error: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={"success": False, "error": str(e)}
        )
