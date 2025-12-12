# Mock File Service 實作計畫

## 📋 專案概述

為 ICSC Echo MCP Server 建立一個 Mock HTTP File Service，用於測試和開發環境。這個 Mock Service 使用 **Python FastAPI** 技術棧來模擬原本基於 **Node.js Fastify** 的 AVA File Service API 行為。

### 技術對照
- **原始服務**: Node.js + Fastify 框架
- **Mock 服務**: Python + FastAPI 框架  
- **目標**: 完全相容的 API 行為模擬

## 🎯 目標

- 提供與 AVA File Service 相容的 API 端點
- 支援檔案上傳、下載、管理等核心功能
- 易於啟動和整合到開發流程
- 與 `uvx` 工具鏈良好整合

## 🏗️ 架構設計

### 分離式架構（採用）

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   MCP Server    │    │  Mock Service   │    │   Test Client   │
│   (uvx 執行)    │◄──►│   (獨立運行)    │◄──►│   (測試工具)    │
│   Port: 8000    │    │   Port: 8090    │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### 目錄結構

```
src/
├── icsc_echo_mcp_server/
│   └── server.py              # 現有 MCP Server
├── mock_file_service/
│   ├── __init__.py
│   ├── server.py              # Mock server 主程式
│   ├── handlers/              # API 處理器
│   │   ├── __init__.py
│   │   ├── chat.py           # 聊天檔案 API
│   │   ├── resources.py      # 資源檔案 API
│   │   └── logs.py           # 日誌管理 API
│   ├── models/               # 資料模型
│   │   ├── __init__.py
│   │   └── responses.py      # 回應模型
│   ├── storage/              # Mock 檔案儲存
│   │   └── uploads/
│   │       ├── chat/
│   │       ├── crawler/
│   │       └── doc/
│   └── config.py            # 配置管理
├── scripts/
│   ├── dev.py               # 開發模式啟動腳本
│   └── test_runner.py       # 測試執行器
└── tests/
    ├── conftest.py          # pytest 配置
    ├── test_mock_service.py  # Mock service 測試
    └── test_integration.py  # 整合測試
```

## 🔧 技術選型

### Mock Server 技術棧

**選擇：FastAPI + Uvicorn（Python）**

**重要說明**：
- **原始 AVA File Service**: Node.js + Fastify 框架
- **我們的 Mock Service**: Python + FastAPI 框架
- **目的**: 用 Python 技術棧模擬 Node.js 服務的 API 行為

**優點**：
- 與現有 Python MCP Server 生態系統完美整合
- 自動 API 文件生成（Swagger UI）
- 原生支援 multipart 檔案上傳
- 型別提示和資料驗證
- 易於測試和除錯
- 統一的 Python 開發環境

**依賴套件**：
```python
fastapi>=0.104.0          # Python Web 框架，模擬 Node.js Fastify
uvicorn>=0.24.0           # ASGI 伺服器，類似 Node.js 的執行環境
python-multipart>=0.0.6   # 檔案上傳支援
aiofiles>=23.0.0          # 非同步檔案操作
```

## 📝 API 實作規劃

### 核心 API 端點

#### 1. 聊天檔案管理

```python
# POST /chat/upload
@app.post("/chat/upload")
async def upload_chat_file(
    file: UploadFile = File(...),
    userId: str = Form(...),
    conversationId: str = Form(...)
)
```

```python
# GET /chat/download/:userId/:conversationId/:filename
@app.get("/chat/download/{userId}/{conversationId}/{filename}")
async def download_chat_file(
    userId: str,
    conversationId: str,
    filename: str,
    preview: bool = False
)
```

#### 2. 資源檔案管理

```python
# POST /upload/{resource_type}
@app.post("/upload/{resource_type}")
async def upload_resource_file(
    resource_type: str,
    file: UploadFile = File(...)
)
```

#### 3. 後台檔案管理

```python
# POST /backend/uploadFilesLlmApi
@app.post("/backend/uploadFilesLlmApi")
async def upload_llm_api_file(file: UploadFile = File(...))
```

### 回應格式

```python
# 成功回應
{
    "success": True,
    "files": {
        "filename.pdf": {
            "status": True,
            "msg": "File uploaded successfully",
            "path": "chat/download/user123/conv456/filename.pdf"
        }
    }
}

# 錯誤回應
{
    "success": False,
    "error": "File size exceeds limit"
}
```

## 🚀 整合策略

### 1. 開發環境啟動

**分離式啟動（推薦）**：
```bash
# Terminal 1: Mock File Service
python -m src.mock_file_service.server

# Terminal 2: MCP Server (stdio 模式)
uvx icsc-echo-mcp-server stdio

# Terminal 3: MCP Server (HTTP 模式)
uvx icsc-echo-mcp-server http
```

**整合式啟動**：
```bash
# 開發模式腳本
python scripts/dev.py
```

### 2. 測試環境整合

```python
# tests/conftest.py
@pytest.fixture(scope="session")
def mock_file_service():
    """啟動 Mock File Service 用於測試"""
    def run_server():
        uvicorn.run(app, host="127.0.0.1", port=8090, log_level="error")
    
    thread = threading.Thread(target=run_server)
    thread.daemon = True
    thread.start()
    
    time.sleep(1)  # 等待 server 啟動
    yield "http://127.0.0.1:8090"
```

### 3. Docker 整合（可選）

```dockerfile
# Dockerfile.mock
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY src/ ./src/
EXPOSE 8090
CMD ["python", "-m", "src.mock_file_service.server"]
```

```yaml
# docker-compose.dev.yml
version: '3.8'
services:
  mock-file-service:
    build:
      context: .
      dockerfile: Dockerfile.mock
    ports:
      - "8090:8090"
    volumes:
      - ./src/mock_file_service/storage:/app/src/mock_file_service/storage
  
  mcp-server:
    build: .
    ports:
      - "8000:8000"
    environment:
      - FILE_SERVICE_URL=http://mock-file-service:8090
    depends_on:
      - mock-file-service
```

## 📋 實作步驟

### Phase 1: 基礎架構
1. ✅ 建立目錄結構
2. ✅ 設定 **Python FastAPI** 基礎框架
3. ✅ 配置管理系統
4. ✅ 基礎儲存結構

### Phase 2: 核心 API（模擬 Node.js Fastify 端點）
1. ✅ 用 Python FastAPI 實作檔案上傳 API
2. ✅ 用 Python FastAPI 實作檔案下載 API
3. ✅ 用 Python FastAPI 實作檔案管理 API
4. ✅ 錯誤處理和驗證

### Phase 3: 進階功能
1. ✅ 日誌管理 API
2. ✅ 檔案大小限制（對應 Node.js 版本的 1GB 限制）
3. ✅ 安全性檢查（路徑注入防護等）
4. ✅ API 文件生成（FastAPI 自動功能）

### Phase 4: 整合測試
1. ⏳ 單元測試撰寫
2. ⏳ 整合測試設定
3. ⏳ 開發腳本製作
4. ⏳ 文件完善

## 🧪 測試策略

### 單元測試
```python
# tests/test_mock_service.py
def test_upload_chat_file():
    """測試聊天檔案上傳"""
    # 實作測試邏輯

def test_download_chat_file():
    """測試聊天檔案下載"""
    # 實作測試邏輯
```

### 整合測試
```python
# tests/test_integration.py
def test_mcp_with_mock_service():
    """測試 MCP Server 與 Mock Service 整合"""
    # 實作整合測試
```

### 效能測試
- 檔案上傳效能測試
- 併發請求測試
- 記憶體使用監控

## 🔧 配置管理

```python
# src/mock_file_service/config.py
class MockConfig:
    HOST = "127.0.0.1"
    PORT = 8090
    STORAGE_DIR = Path("storage/uploads")
    MAX_FILE_SIZE = 1024 * 1024 * 1024  # 1GB
    ALLOWED_EXTENSIONS = [".pdf", ".txt", ".jpg", ".png"]
    LOG_LEVEL = "info"
```

## 📊 監控和日誌

### 日誌格式
```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
```

### 監控指標
- 請求數量統計
- 檔案大小統計
- 錯誤率統計
- 響應時間統計

## 🚀 部署考量

### 本地開發
- 使用虛擬環境管理依賴
- 支援熱重載開發
- 提供開發啟動腳本

### CI/CD 整合
- 自動化測試執行
- Docker 映像建置
- 部署腳本自動化

## 📚 相關文件

- [AVA File Service API 文件](../references/ava-file-service.md)
- [MCP Server 開發指南](../README.md)
- [測試最佳實踐](../docs/testing.md)

## 🔄 維護計畫

### 定期檢查
- 依賴套件更新
- API 相容性驗證
- 效能優化評估

### 功能擴展
- 新增 API 端點支援
- 增強安全性功能
- 改善使用者體驗

---

**建立日期**: 2025-11-28  
**最後更新**: 2025-11-28  
**負責人**: ICSC 開發團隊
