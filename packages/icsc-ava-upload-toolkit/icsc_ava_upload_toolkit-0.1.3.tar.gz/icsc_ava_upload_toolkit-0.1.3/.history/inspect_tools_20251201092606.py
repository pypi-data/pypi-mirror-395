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
        
        class MockContext:
            def info(self, msg):
                print(f"INFO: {msg}")
            def error(self, msg):
                print(f"ERROR: {msg}")
            def warning(self, msg):
                print(f"WARNING: {msg}")
        
        mock_ctx = MockContext()
        
        # 獲取工具列表
        tools = await mcp._list_tools(mock_ctx)
        
        for tool in tools:
            print(f"\n--- 工具: {tool.name} ---")
            print(f"工具類型: {type(tool)}")
            print(f"工具屬性: {[attr for attr in dir(tool) if not attr.startswith('_')]}")
            
            # 檢查各種可能的 schema 屬性
            for attr in ['inputSchema', 'schema', 'parameters', 'args_schema']:
                if hasattr(tool, attr):
                    value = getattr(tool, attr)
                    print(f"  {attr}: {type(value)} = {value}")
            
            # 檢查是否有方法可以獲取 schema
            for method_name in ['to_dict', 'to_schema', 'get_schema', 'model_dump']:
                if hasattr(tool, method_name):
                    try:
                        method = getattr(tool, method_name)
                        if callable(method):
                            result = method()
                            print(f"  {method_name}(): {result}")
                    except Exception as e:
                        print(f"  {method_name}() 錯誤: {e}")
            
            # 特別檢查 download_and_upload
            if tool.name == 'download_and_upload':
                print(f"\n🔍 深入檢查 download_and_upload:")
                
                # 嘗試獲取函數簽名
                if hasattr(tool, 'function') or hasattr(tool, 'fn'):
                    func = getattr(tool, 'function', getattr(tool, 'fn', None))
                    if func:
                        import inspect
                        try:
                            sig = inspect.signature(func)
                            print(f"  函數簽名: {sig}")
                            print(f"  參數: {list(sig.parameters.keys())}")
                        except Exception as e:
                            print(f"  無法獲取函數簽名: {e}")

    except Exception as e:
        print(f"錯誤: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(inspect_tools())
