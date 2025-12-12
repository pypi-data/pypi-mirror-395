#!/usr/bin/env python3
"""測試 MCP Server 的工具定義"""

import sys
import os
import json

# 添加 src 目錄到 Python 路徑
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

try:
    from icsc_echo_mcp_server.server import mcp
    
    print("=== MCP Server Tools 檢查 ===")
    
    # 獲取所有工具
    tools = mcp._list_tools()
    
    print(f"總共找到 {len(tools)} 個工具:")
    for tool in tools:
        print(f"\n--- 工具: {tool.name} ---")
        print(f"描述: {tool.description}")
        print(f"輸入 Schema:")
        print(json.dumps(tool.inputSchema, indent=2, ensure_ascii=False))
        
        # 特別檢查 download_and_upload
        if tool.name == 'download_and_upload':
            print("\n⚠️  檢查 download_and_upload 的參數:")
            properties = tool.inputSchema.get('properties', {})
            for param_name in properties:
                print(f"  - {param_name}: {properties[param_name]}")
            
            # 檢查是否有意外的 file_paths 參數
            if 'file_paths' in properties:
                print("\n🚨 發現問題! download_and_upload 包含不應該存在的 file_paths 參數!")
            else:
                print("\n✅ download_and_upload 參數正確")

except Exception as e:
    print(f"錯誤: {e}")
    import traceback
    traceback.print_exc()
