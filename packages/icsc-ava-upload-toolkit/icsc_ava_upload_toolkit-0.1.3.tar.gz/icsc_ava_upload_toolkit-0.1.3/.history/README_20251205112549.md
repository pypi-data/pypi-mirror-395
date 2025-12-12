# ICSC Ava Upload Toolkit

完整的檔案上傳工具套件，包含 MCP Server 和 Mock File Service，支援工具鏈設計，專為 LibreChat 系統設計。

## 功能

### MCP Server (icsc-ava-upload-mcp-server)
- **download_and_upload**: [CHAINING TOOL] 接收來自上游工具的暫存 URL，下載檔案並上傳到 LibreChat 後端系統

### Mock File Service (mock-file-service)  
- **FastAPI 模擬服務**: 模擬 Node.js Fastify 的 AVA File Service
- **檔案上傳/下載**: 提供完整的檔案管理 API
- **多種儲存類型**: 支援 chat、crawler、doc、logs 等不同類型的檔案儲存

## 安裝

### 使用 uv 安裝

```bash
# 安裝專案依賴
uv sync

# 或者以開發模式安裝
uv pip install -e .
```

### 使用 uvx 直接運行

#### MCP Server

```bash
# 從本地專案運行 MCP Server (STDIO 模式)
uvx --from . icsc-ava-upload-server stdio

# MCP Server (HTTP 模式) - 可指定 host 和 port
uvx --from . icsc-ava-upload-server http 127.0.0.1 8001

# 使用簡短命令
uvx --from . icsc-ava-mcp stdio
```

#### Mock File Service

```bash
# 從本地專案運行 Mock File Service - 可指定 host 和 port
uvx --from . mock-file-service 127.0.0.1 8090

# 使用簡短命令
uvx --from . icsc-ava-mock-service 127.0.0.1 8090

# 開發模式 (支援熱重載)
uvx --from . mock-file-service 127.0.0.1 8090 --reload
```

## 運行模式

### MCP Server 運行模式

#### STDIO 模式

適用於本地 MCP Client 連接：

```bash
# 使用 uv run
uv run python -m icsc_ava_upload_mcp_server.server stdio

# 或使用安裝後的命令
uv run icsc-ava-upload-server stdio
```

#### Streamable HTTP 模式

適用於遠端 MCP Client 連接：

```bash
# 使用 uv run (預設 127.0.0.1:8001)
uv run python -m icsc_ava_upload_mcp_server.server http

# 指定 host 和 port
uv run python -m icsc_ava_upload_mcp_server.server http 0.0.0.0 9000

# 或使用安裝後的命令
uv run icsc-ava-upload-server http 127.0.0.1 8001
```

### Mock File Service 運行模式

```bash
# 使用 uv run (預設 127.0.0.1:8090)
uv run python -m mock_file_service.server

# 指定 host 和 port
uv run python -m mock_file_service.server 0.0.0.0 9000

# 開發模式 (熱重載)
uv run python -m mock_file_service.server 127.0.0.1 8090 --reload

# 或使用安裝後的命令
uv run mock-file-service 127.0.0.1 8090
```

### 同時運行兩個服務

#### 方法一：使用快速啟動腳本（推薦）

```bash
# 一鍵啟動兩個服務
uv run icsc-ava-start

# 或使用 uvx
uvx --from . icsc-ava-start
```

#### 方法二：手動啟動

```bash
# 終端機 1: 啟動 Mock File Service
uv run mock-file-service 127.0.0.1 8090

# 終端機 2: 啟動 MCP Server
uv run icsc-ava-upload-server http 127.0.0.1 8001
```

HTTP 模式預設監聽：
- **MCP Server**: `http://127.0.0.1:8001/mcp`
- **Mock File Service**: `http://127.0.0.1:8090`

## MCP Client 設定範例

### Claude Desktop (stdio 模式)

在 `claude_desktop_config.json` 中加入：

```json
{
  "mcpServers": {
    "icsc-ava-upload": {
      "command": "uvx",
      "args": ["--from", "D:\\project\\icsc-file-uploader", "icsc-ava-upload-server", "stdio"]
    }
  }
}
```

### HTTP 模式連接

啟動 HTTP 伺服器後，MCP Client 可連接到：
- URL: `http://127.0.0.1:8001/mcp`

## 開發

### VSCode 啟動設定

專案已包含 `.vscode/launch.json`，提供兩種除錯模式：
- **MCP Server (STDIO)**: 以 stdio 模式啟動
- **MCP Server (HTTP)**: 以 streamable-http 模式啟動

## 發佈

### 發佈到官方 PyPI

1. **更新版本號**：
   ```bash
   # 更新 pyproject.toml 中的版本號
   # 確保版本號遵循語意化版本控制 (Semantic Versioning)
   ```

2. **構建套件**：
   ```bash
   # 使用 uv 構建套件
   uv build
   
   # 或使用傳統的 setuptools
   python -m build
   ```

3. **上傳到 PyPI**：
   ```bash
   # 上傳到官方 PyPI
   uv publish
   
   # 或使用 twine
   python -m twine upload dist/*
   ```

4. **驗證發佈**：
   ```bash
   # 檢查套件是否成功發佈
   pip install icsc-ava-upload-toolkit
   
   # 或使用 uv
   uv add icsc-ava-upload-toolkit
   ```

### 發佈到測試 PyPI

如需先測試發佈流程：

```bash
# 上傳到測試 PyPI
uv publish --publish-url https://test.pypi.org/legacy/

# 從測試 PyPI 安裝
pip install --index-url https://test.pypi.org/simple/ icsc-ava-upload-toolkit
```

### Git 標籤管理

發佈時建議建立 Git 標籤：

```bash
# 建立標籤
git tag v1.0.0

# 推送標籤到遠端
git push origin v1.0.0
```

### 發佈檢查清單

- [ ] 版本號已更新
- [ ] CHANGELOG.md 已更新
- [ ] 所有測試通過
- [ ] 文檔已更新
- [ ] 構建成功
- [ ] 測試 PyPI 驗證通過
- [ ] 正式發佈到 PyPI

## 授權

MIT License
