"""
資源檔案管理 API
模擬 Node.js AVA File Service 的資源檔案端點
"""

import re
import logging
from pathlib import Path
from typing import Optional

from fastapi import APIRouter, File, Form, UploadFile, HTTPException, Body
from fastapi.responses import FileResponse, JSONResponse

from ..config import MockConfig

logger = logging.getLogger(__name__)
router = APIRouter(tags=["Resource Files"])


def sanitize_filename(filename: str) -> str:
    """清理檔名中的危險字元"""
    return re.sub(r'[/\\?%*:|"<>]', "_", filename)


@router.post("/upload/{resource_type}")
async def upload_resource_file(
    resource_type: str,
    file: UploadFile = File(...)
):
    """
    上傳資源檔案
    
    對應 Node.js 端點: POST /upload/:resource_type
    resource_type: crawler 或 doc
    """
    # 驗證資源類型
    if resource_type not in ["crawler", "doc"]:
        return JSONResponse(
            status_code=400,
            content={"success": False, "error": f"Invalid resource type: {resource_type}"}
        )
    
    try:
        storage_dir = MockConfig.ensure_storage_dirs()
        
        safe_filename = sanitize_filename(file.filename or "unnamed_file")
        target_dir = storage_dir / resource_type
        target_dir.mkdir(parents=True, exist_ok=True)
        
        target_path = target_dir / safe_filename
        
        content = await file.read()
        
        if len(content) > MockConfig.MAX_FILE_SIZE:
            return JSONResponse(
                status_code=400,
                content={"success": False, "error": "File size exceeds 1GB limit"}
            )
        
        with open(target_path, "wb") as f:
            f.write(content)
        
        logger.info(f"Resource file uploaded: {resource_type}/{safe_filename}")
        
        return {
            "success": True,
            "file": {
                "name": safe_filename,
                "path": f"{resource_type}/{safe_filename}",
                "size": len(content)
            }
        }
        
    except Exception as e:
        logger.error(f"Upload resource error: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={"success": False, "error": str(e)}
        )


@router.post("/download/{resource_type}")
async def download_resource_file(
    resource_type: str,
    filename: str = Body(..., embed=True)
):
    """
    下載資源檔案
    
    對應 Node.js 端點: POST /download/:resource_type
    """
    if resource_type not in ["crawler", "doc"]:
        raise HTTPException(status_code=400, detail=f"Invalid resource type: {resource_type}")
    
    try:
        storage_dir = MockConfig.ensure_storage_dirs()
        
        safe_filename = sanitize_filename(filename)
        file_path = storage_dir / resource_type / safe_filename
        
        if not file_path.exists():
            raise HTTPException(status_code=404, detail="File not found")
        
        logger.info(f"Resource file download: {resource_type}/{safe_filename}")
        
        return FileResponse(
            path=file_path,
            filename=safe_filename,
            media_type="application/octet-stream"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Download resource error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/delete/{resource_type}")
async def delete_resource_file(
    resource_type: str,
    filename: str = Body(..., embed=True)
):
    """
    刪除資源檔案
    
    對應 Node.js 端點: POST /delete/:resource_type
    """
    if resource_type not in ["crawler", "doc"]:
        return JSONResponse(
            status_code=400,
            content={"success": False, "error": f"Invalid resource type: {resource_type}"}
        )
    
    try:
        storage_dir = MockConfig.ensure_storage_dirs()
        
        safe_filename = sanitize_filename(filename)
        file_path = storage_dir / resource_type / safe_filename
        
        if not file_path.exists():
            return {"success": True, "message": "File not found, nothing to delete"}
        
        file_path.unlink()
        
        logger.info(f"Resource file deleted: {resource_type}/{safe_filename}")
        
        return {"success": True, "deleted": safe_filename}
        
    except Exception as e:
        logger.error(f"Delete resource error: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={"success": False, "error": str(e)}
        )
