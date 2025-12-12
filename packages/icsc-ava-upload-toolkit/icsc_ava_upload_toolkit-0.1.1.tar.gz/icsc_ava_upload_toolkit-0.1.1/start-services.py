#!/usr/bin/env python3
"""
ICSC Ava Upload Toolkit - 服務啟動腳本
同時啟動 Mock File Service 和 MCP Server
"""

import subprocess
import sys
import time
import os
from pathlib import Path

def start_service(name, command, args):
    """啟動服務"""
    print(f"🚀 啟動 {name}...")
    try:
        process = subprocess.Popen(
            [sys.executable, "-m", command] + args,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True,
            bufsize=1
        )
        return process
    except Exception as e:
        print(f"❌ 啟動 {name} 失敗: {e}")
        return None

def main():
    """主程式"""
    print("🎯 ICSC Ava Upload Toolkit - 服務啟動器")
    print("=" * 50)
    
    # 設定 PYTHONPATH
    env = os.environ.copy()
    env["PYTHONPATH"] = str(Path(__file__).parent / "src")
    
    # 啟動 Mock File Service
    mock_service = start_service(
        "Mock File Service", 
        "mock_file_service.server", 
        ["127.0.0.1", "8090"]
    )
    
    if not mock_service:
        sys.exit(1)
    
    # 等待 Mock File Service 啟動
    time.sleep(2)
    
    # 啟動 MCP Server
    mcp_server = start_service(
        "MCP Server", 
        "icsc_ava_upload_mcp_server.server", 
        ["http", "127.0.0.1", "8001"]
    )
    
    if not mcp_server:
        mock_service.terminate()
        sys.exit(1)
    
    print("\n✅ 兩個服務都已啟動！")
    print("📍 Mock File Service: http://127.0.0.1:8090")
    print("📍 MCP Server: http://127.0.0.1:8001/mcp")
    print("\n按 Ctrl+C 停止所有服務...")
    
    try:
        # 同時監控兩個服務的輸出
        while True:
            # 檢查 Mock File Service 輸出
            if mock_service.poll() is None:
                line = mock_service.stdout.readline()
                if line:
                    print(f"[Mock Service] {line.strip()}")
            
            # 檢查 MCP Server 輸出  
            if mcp_server.poll() is None:
                line = mcp_server.stdout.readline()
                if line:
                    print(f"[MCP Server] {line.strip()}")
            
            # 檢查是否有服務意外停止
            if mock_service.poll() is not None:
                print("❌ Mock File Service 意外停止")
                break
                
            if mcp_server.poll() is not None:
                print("❌ MCP Server 意外停止")
                break
                
            time.sleep(0.1)
            
    except KeyboardInterrupt:
        print("\n\n🛑 正在停止服務...")
        
    finally:
        # 清理程序
        for service, name in [(mock_service, "Mock File Service"), (mcp_server, "MCP Server")]:
            if service and service.poll() is None:
                print(f"🔄 停止 {name}...")
                service.terminate()
                try:
                    service.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    print(f"⚡ 強制停止 {name}")
                    service.kill()
        
        print("✅ 所有服務已停止")

if __name__ == "__main__":
    main()
