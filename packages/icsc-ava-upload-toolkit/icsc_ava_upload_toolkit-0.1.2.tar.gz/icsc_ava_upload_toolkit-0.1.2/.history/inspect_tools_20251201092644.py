#!/usr/bin/env python3
"""深入檢查 FastMCP 工具結構"""

import sys
import os
import asyncio

# 添加 src 目錄到 Python 路徑
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

async def inspect_tools():
    try:
        from icsc_echo_mcp_server.server import mcp
        
        print("=== 深入檢查 FastMCP 工具結構 ===")
        
        mock_ctx = create_mock_context()
        tools = await get_tools_list(mcp, mock_ctx)
        
        for tool in tools:
            analyze_tool(tool)
            
    except Exception as e:
        print(f"錯誤: {e}")
        import traceback
        traceback.print_exc()

def create_mock_context():
    """創建模擬 Context"""
    class MockContext:
        def info(self, msg):
            print(f"INFO: {msg}")
        def error(self, msg):
            print(f"ERROR: {msg}")
        def warning(self, msg):
            print(f"WARNING: {msg}")
    return MockContext()

async def get_tools_list(mcp_instance, context):
    """獲取工具列表"""
    try:
        return await mcp_instance._list_tools(context)
    except Exception as e:
        print(f"獲取工具列表時發生錯誤: {e}")
        return []

def analyze_tool(tool):
    """分析單個工具"""
    print(f"\n--- 工具: {tool.name} ---")
    print(f"工具類型: {type(tool)}")
    
    # 列出工具屬性
    attributes = [attr for attr in dir(tool) if not attr.startswith('_')]
    print(f"工具屬性: {attributes}")
    
    # 檢查各種可能的 schema 屬性
    schema_attrs = ['inputSchema', 'schema', 'parameters', 'args_schema']
    for attr in schema_attrs:
        if hasattr(tool, attr):
            value = getattr(tool, attr)
            print(f"  {attr}: {type(value)} = {value}")
    
    # 檢查可以獲取 schema 的方法
    schema_methods = ['to_dict', 'to_schema', 'get_schema', 'model_dump']
    for method_name in schema_methods:
        check_tool_method(tool, method_name)
    
    # 特別檢查 download_and_upload
    if tool.name == 'download_and_upload':
        deep_inspect_download_and_upload(tool)

def check_tool_method(tool, method_name):
    """檢查工具方法"""
    if hasattr(tool, method_name):
        try:
            method = getattr(tool, method_name)
            if callable(method):
                result = method()
                print(f"  {method_name}(): {result}")
        except Exception as e:
            print(f"  {method_name}() 錯誤: {e}")

def deep_inspect_download_and_upload(tool):
    """深入檢查 download_and_upload 工具"""
    print("\n深入檢查 download_and_upload:")
    
    # 嘗試獲取函數簽名
    func = get_tool_function(tool)
    if func:
        inspect_function_signature(func)

def get_tool_function(tool):
    """獲取工具函數"""
    if hasattr(tool, 'function'):
        return getattr(tool, 'function')
    elif hasattr(tool, 'fn'):
        return getattr(tool, 'fn')
    return None

def inspect_function_signature(func):
    """檢查函數簽名"""
    import inspect
    try:
        sig = inspect.signature(func)
        print(f"  函數簽名: {sig}")
        print(f"  參數: {list(sig.parameters.keys())}")
    except Exception as e:
        print(f"  無法獲取函數簽名: {e}")

if __name__ == "__main__":
    asyncio.run(inspect_tools())
