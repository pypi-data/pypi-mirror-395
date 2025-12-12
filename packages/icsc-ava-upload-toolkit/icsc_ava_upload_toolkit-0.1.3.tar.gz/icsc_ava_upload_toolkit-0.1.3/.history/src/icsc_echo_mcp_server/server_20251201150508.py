"""
ICSC Echo MCP Server
極簡MCP Server，接受字串參數並回傳相同內容（echo功能）
支援 stdio 和 streamable-http 模式
"""

import sys
import os
import tempfile
import requests
import json
from pathlib import Path
from fastmcp import FastMCP, Context

# 建立 FastMCP 實例
mcp = FastMCP(
    name="ICSC Echo Server",
    instructions="這是一個極簡的Echo MCP Server，會將收到的訊息原封不動回傳。",
    
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


@mcp.tool()
def echo(file_paths: list[str], message: str, conversation_id: str, ctx: Context) -> str:
    """
    Echo工具：接收一個字串訊息並原封不動回傳。
    
    Args:
        file_paths: 檔案路徑列表，內容會像是["chat/download/6846f22b16f66da023091c32/3f3bf8d0-4f4c-4342-88ed-f76fd59542f7/abc.pdf"]
        message: 要回傳的字串訊息
        conversation_id: 對話 ID，無須填，會由 Context 自動帶入        
        
    Returns:
        與輸入相同的字串訊息
    """
    ctx.info(f"Received echo request. Message: {message}, Conversation ID: {conversation_id}")
    
    user_id = get_user_id(ctx)
    if not user_id:
        return "找不到此用代碼"
        
    # 可以在這裡記錄 user_id 以供除錯
    ctx.info(f"Access from user: {user_id}")
    
    return f"{message}\nFiles: {file_paths}"


@mcp.tool()
def echo_with_prefix(file_paths: list[str], message: str, conversation_id: str,ctx: Context, prefix: str = "Echo: ") -> str:
    """
    帶前綴的Echo工具：在訊息前加上指定前綴後回傳。
    
    Args:
        file_paths: 檔案路徑列表，內容會像是["chat/download/6846f22b16f66da023091c32/3f3bf8d0-4f4c-4342-88ed-f76fd59542f7/abc.pdf"]
        message: 要回傳的字串訊息
        conversation_id: 聊天ID        
        prefix: 要加在訊息前的前綴，預設為 "Echo: "
        
    Returns:
        加上前綴的字串訊息和檔案路徑
    """
    user_id = get_user_id(ctx)
    if not user_id:
        return "找不到此用代碼"

    ctx.info(f"Access from user: {user_id}")

    return f"{prefix}{message}\nFiles: {file_paths}"


def _validate_headers(ctx: Context) -> tuple[str | None, str | None, str | None]:
    """驗證必要的 headers 並返回 user_id 和 file_service_url"""
    user_id = get_user_id(ctx)
    if not user_id:
        return None, None, "Error: Missing user_id in headers."
    
    file_service_url = get_file_service_url(ctx)
    if not file_service_url:
        return None, None, "Error: Missing file_service_url in headers."
    
    return user_id, file_service_url, None


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


def _upload_to_librechat(file_service_url: str, user_id: str, conversation_id: str, 
                        filename: str, temp_file_path: Path) -> dict:
    """上傳檔案到 LibreChat 後端"""
    try:
        upload_url = f"{file_service_url}/chat/upload"
        
        with open(temp_file_path, 'rb') as f:
            files = {'file': (filename, f, 'application/octet-stream')}
            data = {
                'userId': user_id,
                'conversationId': conversation_id
            }
            
            upload_response = requests.post(upload_url, files=files, data=data, timeout=300)
            upload_response.raise_for_status()
            
            result = upload_response.json()
            
            if result.get('success'):
                file_info = result.get('files', {}).get(filename, {})
                final_path = file_info.get('path', 'unknown_path')
                
                return {
                    "success": True,
                    "data": {
                        "internal_file_path": final_path,
                        "filename": filename,
                        "size": temp_file_path.stat().st_size
                    },
                    "message": f"File '{filename}' has been successfully processed and stored at {final_path}.",
                    "instruction": "The file is now ready. You can use 'internal_file_path' for further analysis or RAG tasks if requested."
                }
            else:
                return {
                    "success": False,
                    "message": f"Upload service returned error: {result}"
                }
                
    except Exception as e:
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
        # 1. 驗證 Headers
        user_id, file_service_url, error_msg = _validate_headers(ctx)
        if error_msg:
            return json.dumps({
                "success": False,
                "message": error_msg
            })
        
        # 2. 下載檔案
        filename, temp_file_path = _download_file(file_url)
        if not filename:
            return json.dumps({
                "success": False,
                "message": "Download failed: Unable to extract filename or download file"
            })
        
        # 3. 上傳到 LibreChat 後端
        result = _upload_to_librechat(file_service_url, user_id, conversation_id, filename, temp_file_path)
        return json.dumps(result)
        
    finally:
        # 4. 清理臨時檔案
        _cleanup_temp_file(temp_file_path, ctx)


def main():
    """主程式入口點，根據命令列參數決定運行模式"""
    if len(sys.argv) > 1:
        transport = sys.argv[1]
        if transport == "http":
            # Streamable HTTP 模式
            mcp.run(transport="streamable-http", host="127.0.0.1", port=8001)
        elif transport == "stdio":
            # STDIO 模式
            mcp.run(transport="stdio")
        else:
            print(f"未知的傳輸模式: {transport}")
            print("可用模式: stdio, http")
            sys.exit(1)
    else:
        # 預設使用 stdio 模式
        mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
