#!/usr/bin/env python3
"""簡單測試 MCP Server 的工具定義"""

import sys
import os
import inspect

# 添加 src 目錄到 Python 路徑
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

try:
    from icsc_echo_mcp_server.server import download_and_upload, echo, echo_with_prefix
    
    print("=== 檢查工具函數定義 ===")
    
    # 檢查 download_and_upload
    print("\n--- download_and_upload 函數簽名 ---")
    sig = inspect.signature(download_and_upload)
    print(f"參數: {list(sig.parameters.keys())}")
    for param_name, param in sig.parameters.items():
        print(f"  {param_name}: {param.annotation} = {param.default}")
    
    # 檢查 echo
    print("\n--- echo 函數簽名 ---")
    sig = inspect.signature(echo)
    print(f"參數: {list(sig.parameters.keys())}")
    
    # 檢查 echo_with_prefix  
    print("\n--- echo_with_prefix 函數簽名 ---")
    sig = inspect.signature(echo_with_prefix)
    print(f"參數: {list(sig.parameters.keys())}")

except Exception as e:
    print(f"錯誤: {e}")
    import traceback
    traceback.print_exc()
