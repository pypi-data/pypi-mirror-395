# AVA File Service 使用文件

## 📋 目錄

- [概述](#概述)
- [技術架構](#技術架構)
- [API 端點](#api-端點)
  - [聊天檔案管理](#聊天檔案管理)
  - [資源檔案管理](#資源檔案管理)
  - [日誌管理](#日誌管理)
  - [後台檔案管理](#後台檔案管理)
- [檔案儲存結構](#檔案儲存結構)
- [安全性說明](#安全性說明)
- [環境配置](#環境配置)
- [使用範例](#使用範例)
- [錯誤處理](#錯誤處理)

---

## 概述

AVA File Service 是一個基於 Node.js 和 Fastify 框架的高效能檔案服務，負責處理 AVA 系統中所有檔案的上傳、下載、刪除等操作。

### 主要功能

- 📤 **檔案上傳**: 支援多檔案上傳，最大 1GB
- 📥 **檔案下載**: 支援串流下載和預覽模式
- 🗑️ **檔案刪除**: 支援單檔案和批次刪除
- 📁 **目錄管理**: 自動建立和管理檔案目錄結構
- 📊 **檔案資訊**: 提供檔案大小、建立時間等資訊
- 📝 **日誌輪替**: 自動管理和輪替日誌檔案

### 版本資訊

- **版本**: 1.0.0
- **Node.js 要求**: >= 18
- **預設端口**: 8090

---

## 技術架構

### 核心技術棧

```json
{
  "runtime": "Node.js >= 18",
  "framework": "Fastify 4.28.1",
  "plugins": [
    "@fastify/multipart 8.3.0",
    "rotating-file-stream 3.2.3",
    "uuid 11.1.0"
  ]
}
```

### 系統架構

```
┌─────────────────────────────────────────────────────────┐
│                    External Clients                      │
│              (Frontend / Backend / API Server)           │
└─────────────────────────────────────────────────────────┘
                            │
                            ↓
┌─────────────────────────────────────────────────────────┐
│                    Nginx (Optional)                      │
│                  Reverse Proxy / SSL                     │
└─────────────────────────────────────────────────────────┘
                            │
                            ↓
┌─────────────────────────────────────────────────────────┐
│                  AVA File Service                        │
│                  (Fastify Server)                        │
│                  Port: 8090                              │
└─────────────────────────────────────────────────────────┘
                            │
                            ↓
┌─────────────────────────────────────────────────────────┐
│                  File System Storage                     │
│                  /app/uploads/                           │
│                  ├── chat/                               │
│                  ├── crawler/                            │
│                  └── doc/                                │
└─────────────────────────────────────────────────────────┘
```

---

## API 端點

### 聊天檔案管理

#### 1. 上傳聊天檔案

**端點**: `POST /chat/upload`

**Content-Type**: `multipart/form-data`

**請求參數**:

| 欄位 | 類型 | 必填 | 說明 |
|------|------|------|------|
| `file` | File | ✅ | 要上傳的檔案 |
| `userId` | String | ✅ | 使用者 ID |
| `conversationId` | String | ✅ | 對話 ID |

**請求範例**:

```bash
curl -X POST http://localhost:8090/chat/upload \
  -F "file=@example.pdf" \
  -F "userId=507f1f77bcf86cd799439011" \
  -F "conversationId=f0b8730a-4d60-4cd8-aed6-c79795ba20fa"
```

**回應範例**:

```json
{
  "success": true,
  "files": {
    "example.pdf": {
      "status": true,
      "msg": "File uploaded successfully",
      "path": "chat/download/507f1f77bcf86cd799439011/f0b8730a-4d60-4cd8-aed6-c79795ba20fa/example.pdf"
    }
  }
}
```

**儲存路徑**: `uploads/chat/{userId}/{conversationId}/{filename}`

---

#### 2. 下載聊天檔案

**端點**: `GET /chat/download/:userId/:conversationId/:filename`

**URL 參數**:

| 參數 | 類型 | 必填 | 說明 |
|------|------|------|------|
| `userId` | String | ✅ | 使用者 ID |
| `conversationId` | String | ✅ | 對話 ID |
| `filename` | String | ✅ | 檔案名稱 |

**查詢參數**:

| 參數 | 類型 | 必填 | 說明 |
|------|------|------|------|
| `preview` | Boolean | ❌ | `true` 為預覽模式，`false` 或不提供為下載模式 |

**請求範例**:

```bash
# 下載檔案
curl -O http://localhost:8090/chat/download/507f1f77bcf86cd799439011/f0b8730a-4d60-4cd8-aed6-c79795ba20fa/example.pdf

# 預覽 PDF (在瀏覽器中開啟)
http://localhost:8090/chat/download/507f1f77bcf86cd799439011/f0b8730a-4d60-4cd8-aed6-c79795ba20fa/example.pdf?preview=true
```

**支援的預覽格式**:
- PDF: `application/pdf` (inline)
- 其他: `application/octet-stream` (attachment)

---

## 安全性說明

### ⚠️ 重要安全提醒

**AVA File Service 本身不提供身份驗證或授權機制**，其安全性依賴於以下架構設計：

### 安全模型

```
┌─────────────────────────────────────────────────────────┐
│ 1. 外部請求                                              │
│    (需要通過 Backend Server 驗證)                        │
└─────────────────────────────────────────────────────────┘
                            │
                            ↓
┌─────────────────────────────────────────────────────────┐
│ 2. Nginx / Backend Server                                │
│    ✅ SSL/TLS 加密                                       │
│    ✅ Session/Token 驗證                                 │
│    ✅ 使用者權限檢查                                      │
└─────────────────────────────────────────────────────────┘
                            │
                            ↓
┌─────────────────────────────────────────────────────────┐
│ 3. File Service (內部網路)                              │
│    ❌ 無身份驗證                                         │
│    ❌ 無授權檢查                                         │
│    ✅ 路徑注入防護                                       │
│    ✅ 檔案大小限制                                       │
└─────────────────────────────────────────────────────────┘
```

### 已實作的安全機制

#### 1. 路徑注入防護

```javascript
// 清理檔名中的危險字元
const safeFilename = originalFilename.replace(/[/\\?%*:|"<>]/g, "_");

// 確保路徑不超出允許的目錄
if (!safeFilePath.startsWith(uploadDir)) {
    return reply.code(400).send({ 
        error: "Invalid path. Potential directory traversal attack detected." 
    });
}
```

#### 2. 檔案大小限制

- **最大檔案大小**: 1GB (1024 * 1024 * 1024 bytes)
- 超過限制會自動拒絕上傳

#### 3. 檔名安全處理

- 移除路徑分隔符: `/` `\`
- 移除特殊字元: `?` `%` `*` `:` `|` `"` `<` `>`
- 防止檔名注入攻擊

---

## 使用範例

### Python 範例 - PDF 合併流程

```python
import requests
from pathlib import Path

class PDFService:
    def __init__(self, file_service_url):
        self.file_service_url = file_service_url.rstrip('/')
    
    def _download_from_file_service(self, file_path):
        """從 file-service 下載檔案"""
        download_url = f"{self.file_service_url}/{file_path}"
        response = requests.get(download_url, stream=True)
        response.raise_for_status()
        
        # 儲存到臨時檔案
        temp_file = Path(f"/tmp/{Path(file_path).name}")
        with open(temp_file, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
        
        return temp_file
    
    def _upload_to_file_service(self, file_path, user_id, conversation_id):
        """上傳檔案到 file-service"""
        upload_url = f"{self.file_service_url}/chat/upload"
        
        with open(file_path, 'rb') as f:
            files = {'file': (Path(file_path).name, f, 'application/pdf')}
            data = {
                'userId': user_id,
                'conversationId': conversation_id
            }
            
            response = requests.post(upload_url, files=files, data=data)
            response.raise_for_status()
            
            result = response.json()
            if result.get('success'):
                # 回傳的路徑格式: chat/download/{userId}/{conversationId}/{filename}
                return result['files'][Path(file_path).name]['path']
            else:
                raise Exception("Upload failed")
    
    def merge_pdfs(self, file_paths, user_id, conversation_id):
        """合併多個 PDF 檔案"""
        import fitz  # PyMuPDF
        
        # 1. 下載所有檔案
        downloaded_files = []
        for file_path in file_paths:
            local_file = self._download_from_file_service(file_path)
            downloaded_files.append(local_file)
        
        # 2. 合併 PDF
        merged_doc = fitz.open()
        for file_path in downloaded_files:
            current_doc = fitz.open(str(file_path))
            merged_doc.insert_pdf(current_doc)
            current_doc.close()
        
        # 3. 儲存合併結果
        output_file = Path(f"/tmp/merged_{user_id}.pdf")
        merged_doc.save(str(output_file))
        merged_doc.close()
        
        # 4. 上傳到 file-service
        file_service_path = self._upload_to_file_service(
            output_file, user_id, conversation_id
        )
        
        # 5. 清理臨時檔案
        for file_path in downloaded_files:
            file_path.unlink()
        output_file.unlink()
        
        return {
            'success': True,
            'download_url': f"http://backend/downloadChat/{user_id}?conversationId={conversation_id}&conversationFilename={output_file.name}"
        }

# 使用範例
pdf_service = PDFService('http://localhost:8090')
result = pdf_service.merge_pdfs(
    [
        'chat/download/user123/conv456/file1.pdf',
        'chat/download/user123/conv456/file2.pdf'
    ],
    'user123',
    'conv456'
)
print(result)
```

---

## 完整的 API 端點列表

### 聊天檔案管理
- `POST /chat/upload` - 上傳聊天檔案
- `GET /chat/download/:userId/:conversationId/:filename` - 下載聊天檔案
- `GET /chat/files/:userId/:conversationId` - 列出聊天檔案
- `DELETE /chat/files/:userId/:conversationId` - 刪除聊天檔案

### 資源檔案管理
- `POST /upload/:resource_type` - 上傳資源檔案 (crawler/doc)
- `POST /download/:resource_type` - 下載資源檔案
- `POST /delete/:resource_type` - 刪除資源檔案

### 日誌管理
- `GET /list-logs` - 列出日誌檔案
- `POST /upload-log` - 上傳日誌檔案
- `POST /download-log` - 下載日誌檔案

### 後台檔案管理
- `POST /backend/uploadFilesLlmApi` - 上傳 LLM API 檔案
- `POST /backend/delete-files` - 刪除後台檔案
- `POST /backend/folder/file-sizes` - 取得資料夾檔案大小資訊

---

## 錯誤處理

### HTTP 狀態碼

| 狀態碼 | 說明 | 常見原因 |
|--------|------|----------|
| `200` | 成功 | 請求成功處理 |
| `400` | 錯誤的請求 | 缺少必要參數、路徑注入攻擊 |
| `403` | 禁止存取 | 檔案權限不足 |
| `404` | 找不到資源 | 檔案或目錄不存在 |
| `500` | 伺服器錯誤 | 內部錯誤、磁碟空間不足 |

---

**文件版本**: 1.0.0  
**最後更新**: 2025-11-28
