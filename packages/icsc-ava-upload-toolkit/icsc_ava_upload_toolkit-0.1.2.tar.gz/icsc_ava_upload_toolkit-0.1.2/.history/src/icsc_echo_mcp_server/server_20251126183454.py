"""
ICSC Echo MCP Server
極簡MCP Server，接受字串參數並回傳相同內容（echo功能）
支援 stdio 和 streamable-http 模式
"""

import sys
from fastmcp import FastMCP

# 建立 FastMCP 實例
mcp = FastMCP(
    name="ICSC Echo Server",
    instructions="這是一個極簡的Echo MCP Server，會將收到的訊息原封不動回傳。"
)


@mcp.tool()
def echo(message: str) -> str:
    """
    Echo工具：接收一個字串訊息並原封不動回傳。
    
    Args:
        message: 要回傳的字串訊息
        
    Returns:
        與輸入相同的字串訊息
    """
    return message


@mcp.tool()
def echo_with_prefix(message: str, prefix: str = "Echo: ") -> str:
    """
    帶前綴的Echo工具：在訊息前加上指定前綴後回傳。
    
    Args:
        message: 要回傳的字串訊息
        prefix: 要加在訊息前的前綴，預設為 "Echo: "
        
    Returns:
        加上前綴的字串訊息
    """
    return f"{prefix}{message}"


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
