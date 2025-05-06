import yaml
from typing import Dict, Any
from pathlib import Path
from pydantic import BaseSettings


def load_yaml_config() -> Dict[str, Any]:
    config_path = Path(__file__).parent.parent / "config.yaml"
    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

class Settings(BaseSettings):
    # 基础配置
    title: str = "Node Gallery"
    version: str = "0.1.0"

    # JWT配置
    secret_key: str = "default-secret-key"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    # 数据库配置
    database_url: str = "sqlite:///./gallery.db"
    database_echo: bool = False

    # 环境配置
    environment: str = "dev"
    
    # 日志配置
    logging: Dict[str, Any] = {}

    # 动态加载YAML配置 [[5]]
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._load_from_yaml()

    def _load_from_yaml(self):
        yaml_config = load_yaml_config()
        for key, value in yaml_config.items():
            if isinstance(value, dict):
                for sub_key, sub_value in value.items():
                    setattr(self, f"{key}_{sub_key}", sub_value)
            else:
                setattr(self, key, value)

    class Config:
        env_file = ".env"  # 支持环境变量覆盖 [[6]]
        env_nested_delimiter = "__"

# 全局配置对象
settings = Settings()