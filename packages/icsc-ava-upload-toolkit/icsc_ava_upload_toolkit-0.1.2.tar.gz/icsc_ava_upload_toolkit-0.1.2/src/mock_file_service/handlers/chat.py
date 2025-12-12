"""
聊天檔案管理 API
模擬 Node.js AVA File Service 的 /chat/* 端點
"""

import re
import logging
from pathlib import Path
from typing import Optional

import aiofiles
from fastapi import APIRouter, File, Form, UploadFile, HTTPException
from fastapi.responses import FileResponse, JSONResponse

from ..config import MockConfig

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/chat", tags=["Chat Files"])


def sanitize_filename(filename: str) -> str:
    """清理檔名中的危險字元（與 Node.js 版本一致）"""
    return re.sub(r'[/\\?%*:|"<>]', "_", filename)


@router.post("/upload")
async def upload_chat_file(
    file: UploadFile = File(...),
    userId: str = Form(...),
    conversationId: str = Form(...)
):
    """
    上傳聊天檔案
    
    對應 Node.js 端點: POST /chat/upload
    """
    try:
        # 確保儲存目錄存在
        storage_dir = MockConfig.ensure_storage_dirs()
        
        # 清理檔名
        safe_filename = sanitize_filename(file.filename or "unnamed_file")
        
        # 建立目標目錄
        target_dir = storage_dir / "chat" / userId / conversationId
        target_dir.mkdir(parents=True, exist_ok=True)
        
        # 儲存檔案
        target_path = target_dir / safe_filename
        
        content = await file.read()
        
        # 檢查檔案大小
        if len(content) > MockConfig.MAX_FILE_SIZE:
            return JSONResponse(
                status_code=400,
                content={"success": False, "error": "File size exceeds 1GB limit"}
            )
        
        async with aiofiles.open(target_path, "wb") as f:
            await f.write(content)
        
        # 回傳路徑格式與 Node.js 版本一致
        file_path = f"chat/download/{userId}/{conversationId}/{safe_filename}"
        
        logger.info(f"File uploaded: {file_path}")
        
        return {
            "success": True,
            "files": {
                safe_filename: {
                    "status": True,
                    "msg": "File uploaded successfully",
                    "path": file_path
                }
            }
        }
        
    except Exception as e:
        logger.error(f"Upload error: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={"success": False, "error": str(e)}
        )


@router.get("/download/{userId}/{conversationId}/{filename}")
async def download_chat_file(
    userId: str,
    conversationId: str,
    filename: str,
    preview: Optional[bool] = False
):
    """
    下載聊天檔案
    
    對應 Node.js 端點: GET /chat/download/:userId/:conversationId/:filename
    """
    try:
        storage_dir = MockConfig.ensure_storage_dirs()
        
        # 清理檔名防止路徑注入
        safe_filename = sanitize_filename(filename)
        
        # 建立檔案路徑
        file_path = storage_dir / "chat" / userId / conversationId / safe_filename
        
        # 安全性檢查：確保路徑在允許的目錄內
        try:
            file_path = file_path.resolve()
            storage_dir_resolved = storage_dir.resolve()
            if not str(file_path).startswith(str(storage_dir_resolved)):
                raise HTTPException(
                    status_code=400,
                    detail="Invalid path. Potential directory traversal attack detected."
                )
        except Exception:
            raise HTTPException(status_code=400, detail="Invalid path")
        
        # 檢查檔案是否存在
        if not file_path.exists():
            raise HTTPException(status_code=404, detail="File not found")
        
        # 決定 Content-Disposition
        if preview and safe_filename.lower().endswith(".pdf"):
            media_type = "application/pdf"
            disposition = "inline"
        else:
            media_type = "application/octet-stream"
            disposition = "attachment"
        
        logger.info(f"File download: {file_path}")
        
        return FileResponse(
            path=file_path,
            filename=safe_filename,
            media_type=media_type,
            headers={"Content-Disposition": f'{disposition}; filename="{safe_filename}"'}
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Download error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/files/{userId}/{conversationId}")
async def list_chat_files(userId: str, conversationId: str):
    """
    列出聊天檔案
    
    對應 Node.js 端點: GET /chat/files/:userId/:conversationId
    """
    try:
        storage_dir = MockConfig.ensure_storage_dirs()
        target_dir = storage_dir / "chat" / userId / conversationId
        
        if not target_dir.exists():
            return {"success": True, "files": []}
        
        files = []
        for f in target_dir.iterdir():
            if f.is_file():
                stat = f.stat()
                files.append({
                    "name": f.name,
                    "size": stat.st_size,
                    "created": stat.st_ctime,
                    "modified": stat.st_mtime
                })
        
        return {"success": True, "files": files}
        
    except Exception as e:
        logger.error(f"List files error: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={"success": False, "error": str(e)}
        )


@router.delete("/files/{userId}/{conversationId}")
async def delete_chat_files(userId: str, conversationId: str):
    """
    刪除聊天檔案
    
    對應 Node.js 端點: DELETE /chat/files/:userId/:conversationId
    """
    try:
        storage_dir = MockConfig.ensure_storage_dirs()
        target_dir = storage_dir / "chat" / userId / conversationId
        
        if not target_dir.exists():
            return {"success": True, "message": "Directory not found, nothing to delete"}
        
        # 刪除目錄中的所有檔案
        deleted_count = 0
        for f in target_dir.iterdir():
            if f.is_file():
                f.unlink()
                deleted_count += 1
        
        # 嘗試刪除空目錄
        try:
            target_dir.rmdir()
        except OSError:
            pass  # 目錄不為空或其他原因
        
        logger.info(f"Deleted {deleted_count} files from {target_dir}")
        
        return {"success": True, "deleted_count": deleted_count}
        
    except Exception as e:
        logger.error(f"Delete files error: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={"success": False, "error": str(e)}
        )
