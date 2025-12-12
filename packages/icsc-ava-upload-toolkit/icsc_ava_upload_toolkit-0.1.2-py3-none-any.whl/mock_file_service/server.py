"""
Mock File Service 主程式
使用 Python FastAPI 模擬 Node.js Fastify 的 AVA File Service

啟動方式:
    python -m src.mock_file_service.server
    
或使用 uvicorn:
    uvicorn src.mock_file_service.server:app --host 127.0.0.1 --port 8090 --reload
"""

import logging
import sys
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import MockConfig
from .handlers import chat_router, resources_router, logs_router, backend_router

# 設定日誌
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """應用程式生命週期管理"""
    # 啟動時
    logger.info("=" * 50)
    logger.info("Mock File Service 啟動中...")
    logger.info("模擬 Node.js AVA File Service API")
    logger.info("監聽: http://%s:%s", MockConfig.HOST, MockConfig.PORT)
    logger.info("儲存目錄: %s", MockConfig.STORAGE_DIR)
    logger.info("=" * 50)
    
    # 確保儲存目錄存在
    MockConfig.ensure_storage_dirs()
    
    yield
    
    # 關閉時
    logger.info("Mock File Service 已關閉")


# 建立 FastAPI 應用
app = FastAPI(
    title="Mock AVA File Service",
    description="""
## 模擬 AVA File Service API

這是一個使用 Python FastAPI 實作的 Mock 服務，用於模擬 Node.js Fastify 版本的 AVA File Service。

### 支援的 API 端點

- **聊天檔案管理**: `/chat/*`
- **資源檔案管理**: `/upload/*`, `/download/*`, `/delete/*`
- **日誌管理**: `/list-logs`, `/upload-log`, `/download-log`
- **後台檔案管理**: `/backend/*`
    """,
    version="0.1.0",
    lifespan=lifespan
)

# CORS 設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 註冊路由
app.include_router(chat_router)
app.include_router(resources_router)
app.include_router(logs_router)
app.include_router(backend_router)


@app.get("/")
async def root():
    """根路徑 - 服務狀態檢查"""
    return {
        "service": "Mock AVA File Service",
        "version": "0.1.0",
        "status": "running",
        "original": "Node.js Fastify AVA File Service",
        "mock_by": "Python FastAPI"
    }


@app.get("/health")
async def health_check():
    """健康檢查端點"""
    return {"status": "healthy"}


def main():
    """主程式入口點 - 支援命令列參數"""
    import uvicorn
    import sys
    
    # 解析命令列參數
    host = sys.argv[1] if len(sys.argv) > 1 else MockConfig.HOST
    port = int(sys.argv[2]) if len(sys.argv) > 2 else MockConfig.PORT
    reload = "--reload" in sys.argv or "-r" in sys.argv
    log_level = "info"
    
    # 檢查是否指定了 log level
    for i, arg in enumerate(sys.argv):
        if arg in ["--log-level", "-l"] and i + 1 < len(sys.argv):
            log_level = sys.argv[i + 1]
            break
    
    print(f"啟動 Mock File Service，監聽 {host}:{port}")
    print(f"儲存目錄: {MockConfig.STORAGE_DIR}")
    
    uvicorn.run(
        "mock_file_service.server:app",
        host=host,
        port=port,
        reload=reload,
        log_level=log_level
    )


if __name__ == "__main__":
    main()
