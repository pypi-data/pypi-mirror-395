"""
ICSC Echo MCP Server
極簡MCP Server，接受字串參數並回傳相同內容（echo功能）
支援 stdio 和 streamable-http 模式
"""

import sys
import os
import tempfile
import requests
from pathlib import Path
from fastmcp import FastMCP, Context

# 建立 FastMCP 實例
mcp = FastMCP(
    name="ICSC Echo Server",
    instructions="這是一個極簡的Echo MCP Server，會將收到的訊息原封不動回傳。",
    strict_input_validation=False  # 使用靈活驗證，允許未知欄位
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


@mcp.tool()
def download_and_upload(file_url: str, conversation_id: str, ctx: Context) -> str:
    """
    从URL下载文件并上传到文件服务
    
    Args:
        file_url: 要下载的完整文件URL
        conversation_id: 对话ID
        ctx: Context对象
        
    Returns:
        成功时返回上传后的文件路径，失败时返回详细错误信息
    """
    temp_file_path = None
    
    try:
        # 1. 验证 user_id
        user_id = get_user_id(ctx)
        if not user_id:
            error_msg = "错误：找不到用户ID (user_id)。请确保 x-user-id header 已正确设置。"
            ctx.error(error_msg)
            return error_msg
        
        ctx.info(f"开始处理文件下载和上传。User ID: {user_id}, Conversation ID: {conversation_id}, File URL: {file_url}")
        
        # 2. 获取 file_service_url
        file_service_url = get_file_service_url(ctx)
        if not file_service_url:
            error_msg = "错误：找不到文件服务URL (file_service_url)。请确保 x-file-service-url header 已正确设置。"
            ctx.error(error_msg)
            return error_msg
        
        ctx.info(f"文件服务URL: {file_service_url}")
        
        # 3. 下载文件到临时目录
        try:
            ctx.info(f"开始下载文件: {file_url}")
            response = requests.get(file_url, stream=True, timeout=300)  # 5分钟超时
            response.raise_for_status()
            
            # 从URL或Content-Disposition header获取文件名
            filename = None
            content_disposition = response.headers.get('Content-Disposition')
            if content_disposition:
                import re
                match = re.findall(r'filename="?([^"]+)"?', content_disposition)
                if match:
                    filename = match[0]
            
            if not filename:
                # 从URL中提取文件名
                filename = Path(file_url).name
                if not filename or filename == '':
                    filename = 'downloaded_file'
            
            # 创建temp目录
            temp_dir = Path("temp")
            temp_dir.mkdir(exist_ok=True)
            
            # 保存文件
            temp_file_path = temp_dir / filename
            ctx.info(f"保存文件到临时位置: {temp_file_path}")
            
            with open(temp_file_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            
            file_size = temp_file_path.stat().st_size
            ctx.info(f"文件下载完成。大小: {file_size} bytes")
            
        except requests.exceptions.Timeout:
            error_msg = f"错误：下载文件超时。URL: {file_url}。请检查网络连接或文件是否过大。"
            ctx.error(error_msg)
            return error_msg
        except requests.exceptions.RequestException as e:
            error_msg = f"错误：下载文件失败。URL: {file_url}。详细信息: {str(e)}"
            ctx.error(error_msg)
            return error_msg
        except Exception as e:
            error_msg = f"错误：保存文件时发生异常。详细信息: {str(e)}"
            ctx.error(error_msg)
            return error_msg
        
        # 4. 上传文件到文件服务
        try:
            upload_url = f"{file_service_url}/chat/upload"
            ctx.info(f"开始上传文件到: {upload_url}")
            
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
                    file_path = result['files'][filename]['path']
                    ctx.info(f"文件上传成功。路径: {file_path}")
                    return f"文件上传成功！\n文件路径: {file_path}\n文件名: {filename}\n文件大小: {file_size} bytes"
                else:
                    error_msg = f"错误：文件服务返回失败状态。响应: {result}"
                    ctx.error(error_msg)
                    return error_msg
                    
        except requests.exceptions.Timeout:
            error_msg = f"错误：上传文件超时。目标: {upload_url}。文件可能过大或网络连接不稳定。"
            ctx.error(error_msg)
            return error_msg
        except requests.exceptions.RequestException as e:
            error_msg = f"错误：上传文件失败。目标: {upload_url}。详细信息: {str(e)}"
            ctx.error(error_msg)
            return error_msg
        except Exception as e:
            error_msg = f"错误：上传过程中发生异常。详细信息: {str(e)}"
            ctx.error(error_msg)
            return error_msg
            
    finally:
        # 5. 清理临时文件
        if temp_file_path and Path(temp_file_path).exists():
            try:
                Path(temp_file_path).unlink()
                ctx.info(f"临时文件已清理: {temp_file_path}")
            except Exception as e:
                ctx.warning(f"警告：无法删除临时文件 {temp_file_path}。错误: {str(e)}")


def main():
    """主程式入口點，根據命令列參數決定運行模式"""
    if len(sys.argv) > 1:
        transport = sys.argv[1]
        if transport == "http":
            # Streamable HTTP 模式
            mcp.run(transport="streamable-http", host="127.0.0.1", port=8000)
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
