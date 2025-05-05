# node-gallery-backend

后端服务文件树：

```bash
node-gallery-backend
├─ app
│  ├─ api                   # 路由层（按业务拆分）
│  │  ├─ api_import.py
│  │  ├─ dependencies.py
│  │  └─ __init__.py
│  ├─ core                  # 核心配置与工具
│  │  └─ __init__.py
│  ├─ db                    # 数据库相关
│  │  ├─ models             # SQLModel 数据模型
│  │  │  ├─ user.py
│  │  │  └─ __init__.py
│  │  ├─ repositories       # 数据库操作层       
│  │  │  └─ ___init__.py
│  │  ├─ schemas            # Pydantic 数据校验模型
│  │  │  └─ __init__.py
│  │  ├─ session.py
│  │  └─ __init__.py
│  ├─ main.py               # FastAPI应用入口
│  └─ services              # 业务逻辑层
│     └─ __init__.py
├─ config.yaml              # 配置项
├─ docs
├─ pdm.lock
├─ pyproject.toml
├─ README.md
└─ tests                    # 测试目录
   └─ __init__.py

```
