"""
後台檔案管理 API
模擬 Node.js AVA File Service 的後台端點
"""

import re
import logging
from pathlib import Path
from typing import List

import aiofiles
from fastapi import APIRouter, File, UploadFile, Body
from fastapi.responses import JSONResponse

from ..config import MockConfig

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/backend", tags=["Backend Files"])


def sanitize_filename(filename: str) -> str:
    """清理檔名中的危險字元"""
    return re.sub(r'[/\\?%*:|"<>]', "_", filename)


@router.post("/uploadFilesLlmApi")
async def upload_llm_api_files(files: List[UploadFile] = File(...)):
    """
    上傳 LLM API 檔案
    
    對應 Node.js 端點: POST /backend/uploadFilesLlmApi
    """
    try:
        storage_dir = MockConfig.ensure_storage_dirs()
        llm_dir = storage_dir / "llm_api"
        llm_dir.mkdir(parents=True, exist_ok=True)
        
        results = {}
        
        for file in files:
            safe_filename = sanitize_filename(file.filename or "unnamed_file")
            target_path = llm_dir / safe_filename
            
            content = await file.read()
            
            if len(content) > MockConfig.MAX_FILE_SIZE:
                results[safe_filename] = {
                    "status": False,
                    "msg": "File size exceeds 1GB limit"
                }
                continue
            
            async with aiofiles.open(target_path, "wb") as f:
                await f.write(content)
            
            results[safe_filename] = {
                "status": True,
                "msg": "File uploaded successfully",
                "path": f"llm_api/{safe_filename}",
                "size": len(content)
            }
        
        logger.info(f"LLM API files uploaded: {len(results)} files")
        
        return {"success": True, "files": results}
        
    except Exception as e:
        logger.error(f"Upload LLM API files error: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={"success": False, "error": str(e)}
        )


@router.post("/delete-files")
async def delete_backend_files(filenames: List[str] = Body(...)):
    """
    刪除後台檔案
    
    對應 Node.js 端點: POST /backend/delete-files
    """
    try:
        storage_dir = MockConfig.ensure_storage_dirs()
        
        deleted = []
        not_found = []
        
        for filename in filenames:
            safe_filename = sanitize_filename(filename)
            
            # 搜尋所有可能的目錄
            found = False
            for subdir in ["llm_api", "chat", "crawler", "doc"]:
                file_path = storage_dir / subdir / safe_filename
                if file_path.exists():
                    file_path.unlink()
                    deleted.append(safe_filename)
                    found = True
                    break
            
            if not found:
                not_found.append(safe_filename)
        
        logger.info(f"Backend files deleted: {len(deleted)}, not found: {len(not_found)}")
        
        return {
            "success": True,
            "deleted": deleted,
            "not_found": not_found
        }
        
    except Exception as e:
        logger.error(f"Delete backend files error: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={"success": False, "error": str(e)}
        )


@router.post("/folder/file-sizes")
async def get_folder_file_sizes(folder_path: str = Body(..., embed=True)):
    """
    取得資料夾檔案大小資訊
    
    對應 Node.js 端點: POST /backend/folder/file-sizes
    """
    try:
        storage_dir = MockConfig.ensure_storage_dirs()
        
        # 安全性：只允許存取 storage 目錄內的資料夾
        target_dir = storage_dir / folder_path
        
        try:
            target_dir = target_dir.resolve()
            storage_dir_resolved = storage_dir.resolve()
            if not str(target_dir).startswith(str(storage_dir_resolved)):
                return JSONResponse(
                    status_code=400,
                    content={"success": False, "error": "Invalid path"}
                )
        except Exception:
            return JSONResponse(
                status_code=400,
                content={"success": False, "error": "Invalid path"}
            )
        
        if not target_dir.exists():
            return {"success": True, "files": [], "total_size": 0}
        
        files = []
        total_size = 0
        
        for f in target_dir.rglob("*"):
            if f.is_file():
                size = f.stat().st_size
                files.append({
                    "name": f.name,
                    "path": str(f.relative_to(storage_dir)),
                    "size": size
                })
                total_size += size
        
        return {
            "success": True,
            "files": files,
            "total_size": total_size,
            "file_count": len(files)
        }
        
    except Exception as e:
        logger.error(f"Get folder file sizes error: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={"success": False, "error": str(e)}
        )
