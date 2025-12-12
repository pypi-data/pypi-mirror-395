"""
ICSC Ava Upload MCP Server
檔案上傳和處理 MCP Server，支援工具鏈設計
支援 stdio 和 streamable-http 模式
"""

import sys
import os
import tempfile
import logging
import argparse
import requests
import json
from pathlib import Path
from fastmcp import FastMCP, Context

logger = logging.getLogger(__name__)

# 建立 FastMCP 實例
mcp = FastMCP(
    name="ICSC Ava Upload Server",
    instructions="這是一個檔案上傳和處理的 MCP Server，作為工具鏈中的第二棒工具，接收來自上游工具的暫存 URL 並將檔案註冊到 LibreChat 系統中。",
    
)

def get_user_id(ctx: Context) -> str | None:
    """
    從 Context 中獲取 X-User-Id
    嘗試從多個可能的位置查找變數
    """
    # 1. 嘗試從 request_context 獲取 Starlette Request 物件
    # 參考: https://gofastmcp.com/python-sdk/fastmcp-server-context#get-http-request
    try:
        rc = getattr(ctx, "request_context", None)
        
        if rc:
            # 嘗試取得 request 物件 (Starlette Request)
            request = getattr(rc, "request", None)
            
            if request:
                headers = getattr(request, "headers", None)
                if headers:
                    # Header keys are case-insensitive in Starlette, but using the exact key is safer
                    val = headers.get("x-user-id") or headers.get("X-User-Id")
                    if val: return val
    except Exception:
        pass

    # 2. 嘗試從 meta 獲取 (JSON-RPC metadata)
    try:
        meta = getattr(ctx, "meta", None)
        if isinstance(meta, dict):
            val = meta.get("X-User-Id")
            if val: return val
    except Exception:
        pass
        
    return None


def get_file_service_url(ctx: Context) -> str | None:
    """
    从 Context 中获取 File Service URL
    尝试从 request headers 获取 x-file-service-url
    如果抓不到则从环境变量获取
    """
    # 1. 先尝试从 Context 的 request headers 获取
    try:
        rc = getattr(ctx, "request_context", None)
        
        if rc:
            request = getattr(rc, "request", None)
            
            if request:
                headers = getattr(request, "headers", None)
                if headers:
                    val = headers.get("x-file-service-url") or headers.get("X-File-Service-Url")
                    if val: 
                        return val.rstrip('/')  # 移除尾部斜杠
    except Exception:
        pass
    
    # 2. 如果从 headers 获取不到，尝试从环境变量获取
    try:
        import os
        env_val = os.getenv('FILE_SERVICE_URL')
        if env_val:
            return env_val.rstrip('/')
    except Exception:
        pass
        
    return None


def get_backend_service_url(ctx: Context) -> str | None:
    """
    从 Context 中获取 Backend Service URL
    优先从 request headers 读取 x-backend-service-url，其次读取环境变量 BACKEND_SERVICE_URL
    """
    try:
        rc = getattr(ctx, "request_context", None)
        if rc:
            request = getattr(rc, "request", None)
            if request:
                headers = getattr(request, "headers", None)
                if headers:
                    val = headers.get("x-backend-service-url") or headers.get("X-Backend-Service-Url")
                    if val:
                        return val.rstrip('/')
    except Exception:
        pass

    try:
        env_val = os.getenv('BACKEND_SERVICE_URL')
        if env_val:
            return env_val.rstrip('/')
    except Exception:
        pass

    return None


def _validate_headers(ctx: Context) -> tuple[str | None, str | None, str | None, str | None]:
    """驗證必要的 headers 並返回 user_id、file_service_url、backend_service_url"""
    user_id = get_user_id(ctx)
    if not user_id:
        return None, None, None, "Error: Missing user_id in headers."
    
    file_service_url = get_file_service_url(ctx)
    if not file_service_url:
        return None, None, None, "Error: Missing file_service_url in headers."
    
    backend_service_url = get_backend_service_url(ctx)
    
    return user_id, file_service_url, backend_service_url, None


def _extract_filename(response: requests.Response, file_url: str) -> str:
    """從 response headers 或 URL 提取檔名"""
    filename = None
    content_disposition = response.headers.get('Content-Disposition')
    if content_disposition:
        import re
        match = re.findall(r'filename="?([^"]+)"?', content_disposition)
        if match:
            filename = match[0]
    
    if not filename:
        filename = Path(file_url).name
        if not filename or filename == '':
            filename = 'downloaded_file'
    
    return filename


def _download_file(file_url: str) -> tuple[str | None, Path | None]:
    """下載檔案到臨時位置，返回檔名和臨時檔案路徑"""
    try:
        response = requests.get(file_url, stream=True, timeout=300)
        response.raise_for_status()
        
        filename = _extract_filename(response, file_url)
        
        temp_dir = Path("temp")
        temp_dir.mkdir(exist_ok=True)
        temp_file_path = temp_dir / filename
        
        with open(temp_file_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        return filename, temp_file_path
        
    except Exception as e:
        return None, None


def _upload_to_librechat(file_service_url: str, backend_service_url: str, user_id: str, conversation_id: str, 
                        filename: str, temp_file_path: Path) -> dict:
    """上傳檔案到 LibreChat 後端"""
    try:
        upload_url = f"{file_service_url}/chat/upload"
        logger.info("準備上傳檔案到 LibreChat | upload_url=%s user_id=%s conversation_id=%s filename=%s size=%s",
                    upload_url, user_id, conversation_id, filename, temp_file_path.stat().st_size)
        
        with open(temp_file_path, 'rb') as f:
            files = {'file': (filename, f, 'application/octet-stream')}
            data = {
                'userId': user_id,
                'conversationId': conversation_id
            }
            
            upload_response = requests.post(upload_url, files=files, data=data, timeout=300)
            upload_response.raise_for_status()
            
            result = upload_response.json()
            logger.info("LibreChat 回應結果: %s", result)
            
            if result.get('success'):
                file_info = result.get('files', {}).get(filename, {})
                final_path = file_info.get('path', 'unknown_path')
                download_url = f"{backend_service_url}/downloadChat/{user_id}?conversationId={conversation_id}&conversationFilename={Path(final_path).name}" if backend_service_url else None
                
                return {
                    "success": True,
                    "data": {
                        "filename": filename,
                        "size": temp_file_path.stat().st_size,
                        "download_url": download_url
                    },
                    "message": f"File '{filename}' has been successfully processed.",
                    "instruction": "Present the 'download_url' to the user for direct download. Do NOT call the download_and_upload tool again for this file."
                }
            else:
                return {
                    "success": False,
                    "message": f"Upload service returned error: {result}"
                }
                
    except Exception as e:
        logger.exception("上傳至 LibreChat 失敗")
        return {
            "success": False,
            "message": f"Upload process failed: {str(e)}"
        }


def _cleanup_temp_file(temp_file_path: Path | None, ctx: Context) -> None:
    """清理臨時檔案"""
    if temp_file_path and temp_file_path.exists():
        try:
            temp_file_path.unlink()
            ctx.info(f"临时文件已清理: {temp_file_path}")
        except Exception as e:
            ctx.warning(f"警告：无法删除临时文件 {temp_file_path}。错误: {str(e)}")


@mcp.tool()
def download_and_upload(file_url: str, file_paths: list[str], conversation_id: str, ctx: Context) -> str:
    """
    [CHAINING TOOL] Process a file URL generated by a previous tool and register it with the system.
    
    Use this tool IMMEDIATELY after receiving a 'downloadUrl' from an upstream tool (like 'upload_file').
    This tool downloads the file from the temporary URL and uploads it to the LibreChat backend 
    to make it available for the user's session.

    Args:
        file_url: The temporary download URL provided by the previous tool's output payload.
        file_paths: File paths list (maintained for compatibility, not used in this tool)
        conversation_id: The current conversation ID.
        ctx: Context object.

    Returns:
        JSON string containing the status, the final internal file path, and a user-friendly message.
    """
    temp_file_path = None
    
    try:
        logger.info("開始處理 download_and_upload | file_url=%s conversation_id=%s", file_url, conversation_id)
        
        # 1. 驗證 Headers
        user_id, file_service_url, backend_service_url, error_msg = _validate_headers(ctx)
        if error_msg:
            logger.warning("Header 驗證失敗: %s", error_msg)
            return json.dumps({
                "success": False,
                "message": error_msg
            })
        
        # 2. 下載檔案
        filename, temp_file_path = _download_file(file_url)
        if not filename:
            logger.warning("下載失敗或無法取得檔名 | file_url=%s", file_url)
            return json.dumps({
                "success": False,
                "message": "Download failed: Unable to extract filename or download file"
            })
        logger.info("檔案已下載完成 | filename=%s temp_path=%s", filename, temp_file_path)
        
        # 3. 上傳到 LibreChat 後端
        result = _upload_to_librechat(file_service_url, backend_service_url, user_id, conversation_id, filename, temp_file_path)        
        logger.info("上傳結果: %s", result)
        
        
        
        return json.dumps(result)
        
    finally:
        # 4. 清理臨時檔案
        _cleanup_temp_file(temp_file_path, ctx)


def _configure_logging(log_level: str, log_file: str | None, log_to_console: bool) -> None:
    """根據參數設定 logging level 與輸出目的地"""
    log_level_str = (log_level or "INFO").upper()
    level = logging.getLevelName(log_level_str)
    if not isinstance(level, int):
        level = logging.INFO
        logger.warning("未識別的 log_level=%s，已回退到 INFO", log_level_str)

    handlers: list[logging.Handler] = []
    if log_file:
        handlers.append(logging.FileHandler(log_file, encoding="utf-8"))
    if log_to_console or not handlers:
        handlers.append(logging.StreamHandler())

    logging.basicConfig(
        level=level,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        handlers=handlers,
        force=True,
    )
    logger.info("Logging 已設定 | level=%s handlers=%s", logging.getLevelName(level), ["file" if isinstance(h, logging.FileHandler) else "console" for h in handlers])


def _parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="ICSC Ava Upload MCP Server")
    parser.add_argument("transport", nargs="?", choices=["http", "stdio"], default="stdio", help="啟動模式，預設 stdio")
    parser.add_argument("host", nargs="?", default="127.0.0.1", help="HTTP 模式 host，預設 127.0.0.1")
    parser.add_argument("port", nargs="?", type=int, default=8001, help="HTTP 模式 port，預設 8001")
    parser.add_argument("--log-level", default="INFO", help="Logging 等級，如 DEBUG/INFO/WARN/ERROR")
    parser.add_argument("--log-file", default=None, help="若指定，輸出到此檔案")
    parser.add_argument("--no-console", action="store_true", help="不輸出到 console（若無其他 handler 仍會啟用 console）")
    return parser.parse_args(argv)


def main():
    """主程式入口點，根據命令列參數決定運行模式"""
    args = _parse_args(sys.argv[1:])
    _configure_logging(args.log_level, args.log_file, not args.no_console)

    if args.transport == "http":
        print(f"啟動 HTTP 模式，監聽 {args.host}:{args.port}")
        mcp.run(transport="streamable-http", host=args.host, port=args.port)
    elif args.transport == "stdio":
        mcp.run(transport="stdio")
    else:
        print(f"未知的傳輸模式: {args.transport}")
        print("可用模式: stdio, http")
        print("HTTP 模式用法: python -m icsc_ava_upload_mcp_server.server http [host] [port]")
        sys.exit(1)


if __name__ == "__main__":
    main()
