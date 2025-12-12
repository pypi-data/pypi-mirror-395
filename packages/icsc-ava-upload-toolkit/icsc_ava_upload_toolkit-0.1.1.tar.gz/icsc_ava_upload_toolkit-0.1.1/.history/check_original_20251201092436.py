#!/usr/bin/env python3
"""檢查原始函數定義"""

import sys
import os
import inspect

# 添加 src 目錄到 Python 路徑
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# 直接導入模組，不經過 FastMCP 裝飾器
import icsc_echo_mcp_server.server as server_module

print("=== 檢查原始函數定義 (裝飾器前) ===")

# 獲取原始函數
original_download_and_upload = server_module.download_and_upload.__wrapped__ if hasattr(server_module.download_and_upload, '__wrapped__') else server_module.download_and_upload
original_echo = server_module.echo.__wrapped__ if hasattr(server_module.echo, '__wrapped__') else server_module.echo

print("\n--- download_and_upload 原始函數簽名 ---")
try:
    sig = inspect.signature(original_download_and_upload)
    print(f"參數: {list(sig.parameters.keys())}")
    for param_name, param in sig.parameters.items():
        print(f"  {param_name}: {param.annotation}")
except Exception as e:
    print(f"錯誤: {e}")

print("\n--- echo 原始函數簽名 ---")
try:
    sig = inspect.signature(original_echo)
    print(f"參數: {list(sig.parameters.keys())}")
    for param_name, param in sig.parameters.items():
        print(f"  {param_name}: {param.annotation}")
except Exception as e:
    print(f"錯誤: {e}")

# 檢查 FastMCP 註冊的工具
print("\n=== FastMCP 註冊的工具 ===")
from icsc_echo_mcp_server.server import mcp

# 嘗試獲取工具資訊
try:
    # 檢查內部工具註冊
    if hasattr(mcp, '_tools'):
        print(f"註冊的工具數量: {len(mcp._tools)}")
        for name, tool in mcp._tools.items():
            print(f"\n工具: {name}")
            print(f"類型: {type(tool)}")
            if hasattr(tool, 'inputSchema'):
                print(f"輸入 Schema: {tool.inputSchema}")
    else:
        print("無法找到 _tools 屬性")
        
        # 嘗試其他可能的屬性
        for attr in dir(mcp):
            if 'tool' in attr.lower():
                print(f"發現相關屬性: {attr}")
                
except Exception as e:
    print(f"檢查工具時發生錯誤: {e}")
    import traceback
    traceback.print_exc()
