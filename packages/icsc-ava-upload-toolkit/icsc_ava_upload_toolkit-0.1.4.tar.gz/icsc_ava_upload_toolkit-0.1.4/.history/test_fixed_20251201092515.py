#!/usr/bin/env python3
"""測試修正後的 MCP Server"""

import sys
import os
import json

# 添加 src 目錄到 Python 路徑
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

try:
    # 設定環境變數以避免 Unicode 錯誤
    os.environ['PYTHONIOENCODING'] = 'utf-8'
    
    from icsc_echo_mcp_server.server import mcp
    
    print("=== 測試修正後的 MCP Server ===")
    
    # 嘗試創建一個 mock context 來測試工具列表
    class MockContext:
        def info(self, msg):
            print(f"INFO: {msg}")
        def error(self, msg):
            print(f"ERROR: {msg}")
        def warning(self, msg):
            print(f"WARNING: {msg}")
    
    mock_ctx = MockContext()
    
    # 獲取工具列表
    try:
        tools = mcp._list_tools(mock_ctx)
        print(f"找到 {len(tools)} 個工具")
        
        for tool in tools:
            print(f"\n--- 工具: {tool.name} ---")
            if hasattr(tool, 'inputSchema'):
                schema = tool.inputSchema
                print(f"Schema properties: {list(schema.get('properties', {}).keys())}")
                
                # 特別檢查 download_and_upload
                if tool.name == 'download_and_upload':
                    properties = schema.get('properties', {})
                    print(f"download_and_upload 參數: {list(properties.keys())}")
                    
                    if 'file_paths' in properties:
                        print("🚨 問題仍存在：download_and_upload 還是有 file_paths 參數")
                    else:
                        print("✅ 問題已解決：download_and_upload 沒有 file_paths 參數")
                        
            else:
                print("沒有 inputSchema 屬性")
                
    except Exception as e:
        print(f"獲取工具列表時發生錯誤: {e}")
        import traceback
        traceback.print_exc()

except Exception as e:
    print(f"錯誤: {e}")
    import traceback
    traceback.print_exc()
