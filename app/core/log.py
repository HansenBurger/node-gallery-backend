# 日志组件

import logging
import logging.config
from pathlib import Path
from app.core.config import settings

def setup_logging():
    # 确保日志目录存在
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    # 加载配置
    logging.config.dictConfig(settings.logging)
    
    # FastAPI默认日志器
    logging.getLogger("uvicorn.error").propagate = True
    logging.getLogger("uvicorn.access").propagate = True