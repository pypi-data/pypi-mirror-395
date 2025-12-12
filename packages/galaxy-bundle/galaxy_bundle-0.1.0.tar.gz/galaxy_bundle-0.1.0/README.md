# 🌌 Galaxy Bundle

[![PyPI version](https://badge.fury.io/py/galaxy-bundle.svg)](https://badge.fury.io/py/galaxy-bundle)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**A BOM-style Dependency Management Package for Python** - Similar to Spring Boot Parent POM

Galaxy Bundle 提供了一种类似于 Spring Boot Parent 的依赖管理方式，让你可以：

- 🔒 **锁定依赖版本** - 所有依赖使用经过测试的、相互兼容的版本
- 📦 **Starter 模式** - 按功能分组，一行命令安装所需依赖
- 🔄 **统一升级** - 只需升级 galaxy-bundle，所有依赖同步更新
- 🛡️ **避免冲突** - 预防依赖版本不兼容的问题

## 快速开始

### 安装

```bash
# 安装单个 Starter
pip install galaxy-bundle[redis]
pip install galaxy-bundle[kafka]
pip install galaxy-bundle[fastapi]

# 安装多个 Starters
pip install galaxy-bundle[redis,kafka,fastapi]

# 安装组合 Starter（推荐）
pip install galaxy-bundle[microservice]  # 包含 FastAPI + Postgres + Redis + Kafka + 可观测性
pip install galaxy-bundle[api]           # 包含 FastAPI + Postgres + Redis + 可观测性
pip install galaxy-bundle[worker]        # 包含 Celery + Redis + Postgres + 可观测性

# 安装全部（开发环境）
pip install galaxy-bundle[all]
```

## 可用 Starters

### 缓存

| Starter | 包含的包 | 安装命令 |
|---------|---------|---------|
| `redis` | redis, hiredis | `pip install galaxy-bundle[redis]` |

### 消息队列

| Starter | 包含的包 | 安装命令 |
|---------|---------|---------|
| `kafka` | confluent-kafka | `pip install galaxy-bundle[kafka]` |
| `kafka-python` | kafka-python | `pip install galaxy-bundle[kafka-python]` |
| `rabbitmq` | pika | `pip install galaxy-bundle[rabbitmq]` |
| `celery` | celery, redis | `pip install galaxy-bundle[celery]` |

### 数据库

| Starter | 包含的包 | 安装命令 |
|---------|---------|---------|
| `postgres` | psycopg2-binary, asyncpg | `pip install galaxy-bundle[postgres]` |
| `mysql` | pymysql, aiomysql | `pip install galaxy-bundle[mysql]` |
| `mongodb` | pymongo, motor | `pip install galaxy-bundle[mongodb]` |
| `sqlalchemy` | sqlalchemy, alembic | `pip install galaxy-bundle[sqlalchemy]` |

### Web 框架

| Starter | 包含的包 | 安装命令 |
|---------|---------|---------|
| `fastapi` | fastapi, uvicorn, pydantic, pydantic-settings | `pip install galaxy-bundle[fastapi]` |
| `flask` | flask, flask-cors, gunicorn | `pip install galaxy-bundle[flask]` |
| `django` | django, djangorestframework | `pip install galaxy-bundle[django]` |

### HTTP 客户端

| Starter | 包含的包 | 安装命令 |
|---------|---------|---------|
| `http` | httpx, aiohttp | `pip install galaxy-bundle[http]` |
| `requests` | requests, urllib3 | `pip install galaxy-bundle[requests]` |

### AI/ML

| Starter | 包含的包 | 安装命令 |
|---------|---------|---------|
| `openai` | openai, tiktoken | `pip install galaxy-bundle[openai]` |
| `langchain` | langchain, langchain-core, langchain-community | `pip install galaxy-bundle[langchain]` |

### 可观测性

| Starter | 包含的包 | 安装命令 |
|---------|---------|---------|
| `observability` | opentelemetry-api/sdk/instrumentation, prometheus-client | `pip install galaxy-bundle[observability]` |
| `logging` | structlog, python-json-logger | `pip install galaxy-bundle[logging]` |

### 测试 & 开发

| Starter | 包含的包 | 安装命令 |
|---------|---------|---------|
| `testing` | pytest, pytest-asyncio, pytest-cov, pytest-mock, httpx, factory-boy, faker | `pip install galaxy-bundle[testing]` |
| `dev` | ruff, mypy, pre-commit, ipython | `pip install galaxy-bundle[dev]` |

### 🌟 组合 Starters（推荐）

| Starter | 包含的 Starters | 适用场景 |
|---------|----------------|---------|
| `web` | fastapi + http + redis | Web 应用 |
| `api` | fastapi + postgres + sqlalchemy + redis + observability | API 服务 |
| `worker` | celery + redis + postgres + sqlalchemy + observability | 后台任务 |
| `microservice` | fastapi + postgres + sqlalchemy + redis + kafka + http + observability + logging | 微服务 |

## 编程方式使用

```python
from galaxy_bundle import (
    show_info,           # 显示帮助信息
    show_starters,       # 列出所有可用 Starters
    show_versions,       # 显示所有包版本
    get_version,         # 获取特定包的版本
    VERSIONS,            # 版本字典
)

# 查看信息
show_info()
show_starters()
show_starters('fastapi')  # 查看特定 Starter
show_versions()

# 获取版本
print(get_version('redis'))  # '5.0.0'
print(get_version('fastapi'))  # '0.109.0'

# 生成 requirements.txt
from galaxy_bundle.versions import generate_requirements_txt
print(generate_requirements_txt(['redis', 'fastapi']))
```

## 版本策略

Galaxy Bundle 遵循以下版本策略：

- **主版本** (`1.0.0`): 重大变更，可能包含不兼容的依赖升级
- **次版本** (`0.1.0`): 添加新 Starters 或依赖小版本升级
- **补丁版本** (`0.0.1`): 安全修复或 Bug 修复

## 与 Spring Boot Parent 的对比

| 特性 | Spring Boot Parent | Galaxy Bundle |
|-----|-------------------|---------------|
| 依赖版本管理 | ✅ dependencyManagement | ✅ extras dependencies |
| 功能分组 | ✅ Starters | ✅ Starters (extras) |
| 一行安装 | ✅ starter 依赖 | ✅ `pip install galaxy-bundle[xxx]` |
| 版本锁定 | ✅ BOM | ✅ pinned versions |
| 统一升级 | ✅ 升级 parent | ✅ 升级 galaxy-bundle |

## 在项目中使用

### pyproject.toml

```toml
[project]
dependencies = [
    "galaxy-bundle[microservice]",
]
```

### requirements.txt

```txt
galaxy-bundle[api]
```

## 贡献

欢迎贡献！请查看 [CONTRIBUTING.md](CONTRIBUTING.md) 了解更多。

## License

MIT License - 详见 [LICENSE](LICENSE) 文件。

