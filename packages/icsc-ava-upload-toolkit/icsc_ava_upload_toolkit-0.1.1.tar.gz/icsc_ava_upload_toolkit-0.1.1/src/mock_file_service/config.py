"""
Mock File Service 配置管理
"""

from pathlib import Path


class MockConfig:
    """Mock File Service 配置"""
    
    HOST = "127.0.0.1"
    PORT = 8090
    
    # 儲存目錄（相對於專案根目錄）
    STORAGE_DIR = Path(__file__).parent / "storage" / "uploads"
    
    # 檔案大小限制：1GB（與 Node.js 版本一致）
    MAX_FILE_SIZE = 1024 * 1024 * 1024
    
    # 日誌等級
    LOG_LEVEL = "info"
    
    @classmethod
    def ensure_storage_dirs(cls):
        """確保儲存目錄存在"""
        dirs = [
            cls.STORAGE_DIR / "chat",
            cls.STORAGE_DIR / "crawler", 
            cls.STORAGE_DIR / "doc",
            cls.STORAGE_DIR / "logs",
        ]
        for d in dirs:
            d.mkdir(parents=True, exist_ok=True)
        return cls.STORAGE_DIR
