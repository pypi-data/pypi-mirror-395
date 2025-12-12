#!/usr/bin/env python3
"""異步測試修正後的 MCP Server"""

import sys
import os
import asyncio
import json

# 添加 src 目錄到 Python 路徑
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

async def test_mcp():
    try:
        from icsc_echo_mcp_server.server import mcp
        
        print("=== 測試修正後的 MCP Server ===")
        
        # 嘗試創建一個 mock context
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
            tools = await mcp._list_tools(mock_ctx)
            print(f"找到 {len(tools)} 個工具")
            
            for tool in tools:
                print(f"\n--- 工具: {tool.name} ---")
                if hasattr(tool, 'inputSchema'):
                    schema = tool.inputSchema
                    properties = schema.get('properties', {})
                    print(f"Schema properties: {list(properties.keys())}")
                    
                    # 特別檢查 download_and_upload
                    if tool.name == 'download_and_upload':
                        print(f"download_and_upload 參數: {list(properties.keys())}")
                        
                        if 'file_paths' in properties:
                            print("🚨 問題仍存在：download_and_upload 還是有 file_paths 參數")
                            print(f"file_paths 參數定義: {properties['file_paths']}")
                        else:
                            print("✅ 問題已解決：download_and_upload 沒有 file_paths 參數")
                        
                        # 顯示所有參數的詳細資訊
                        for param_name, param_def in properties.items():
                            print(f"  {param_name}: {param_def}")
                        
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

if __name__ == "__main__":
    asyncio.run(test_mcp())
