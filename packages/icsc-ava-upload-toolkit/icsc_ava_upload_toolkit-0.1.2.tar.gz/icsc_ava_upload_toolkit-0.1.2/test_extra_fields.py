#!/usr/bin/env python3
"""測試 FastMCP 是否允許未知欄位"""

import sys
import os
import asyncio

# 添加 src 目錄到 Python 路徑
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

async def test_extra_fields():
    try:
        from icsc_echo_mcp_server.server import mcp
        
        print("=== 測試 FastMCP 未知欄位配置 ===")
        
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
            if hasattr(tool, 'parameters'):
                schema = tool.parameters
                print(f"參數 Schema: {schema}")
                
                # 檢查 additionalProperties 設定
                if 'additionalProperties' in schema:
                    print(f"additionalProperties: {schema['additionalProperties']}")
                else:
                    print("未設定 additionalProperties (預設可能為 true)")
                
                # 特別檢查 download_and_upload
                if tool.name == 'download_and_upload':
                    properties = schema.get('properties', {})
                    print(f"download_and_upload 參數: {list(properties.keys())}")
                    
                    # 測試模擬調用帶未知欄位
                    print("\n🧪 測試模擬調用...")
                    await simulate_tool_call(tool, mock_ctx)
            else:
                print("沒有 parameters 屬性")

async def simulate_tool_call(tool, ctx):
    """模擬工具調用，包含未知欄位"""
    try:
        # 模擬調用 download_and_upload 帶有 file_paths 未知欄位
        if tool.name == 'download_and_upload':
            # 這裡我們只是檢查是否會因為未知欄位而報錯
            print("✅ 如果配置正確，應該會忽略 file_paths 未知欄位")
            
            # 檢查工具的 model_config
            if hasattr(tool, 'model_config'):
                config = tool.model_config
                print(f"工具 model_config: {config}")
                if 'extra' in config:
                    print(f"extra 設定: {config['extra']}")
            
    except Exception as e:
        print(f"❌ 模擬調用失敗: {e}")

if __name__ == "__main__":
    asyncio.run(test_extra_fields())
