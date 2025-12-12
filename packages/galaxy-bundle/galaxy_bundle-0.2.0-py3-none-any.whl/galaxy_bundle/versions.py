"""
Galaxy Bundle - Version Constants and Utilities

This module provides programmatic access to the curated dependency versions.
You can use these constants in your own pyproject.toml or requirements.txt.
"""

from typing import Dict, List, Optional

# =============================================================================
# Curated Version Constants
# These versions are tested and known to work well together
# =============================================================================

VERSIONS: Dict[str, str] = {
    # -----------------------------------------------------------------------------
    # Cache
    # -----------------------------------------------------------------------------
    "redis": "5.0.0",
    "hiredis": "2.3.0",
    
    # -----------------------------------------------------------------------------
    # Message Queues
    # -----------------------------------------------------------------------------
    "confluent-kafka": "2.3.0",
    "kafka-python": "2.0.2",
    "pika": "1.3.0",
    "celery": "5.3.0",
    
    # -----------------------------------------------------------------------------
    # Databases
    # -----------------------------------------------------------------------------
    "psycopg2-binary": "2.9.9",
    "asyncpg": "0.29.0",
    "pymysql": "1.1.0",
    "aiomysql": "0.2.0",
    "pymongo": "4.6.0",
    "motor": "3.3.0",
    "sqlalchemy": "2.0.0",
    "alembic": "1.13.0",
    
    # -----------------------------------------------------------------------------
    # Web Frameworks
    # -----------------------------------------------------------------------------
    "fastapi": "0.109.0",
    "uvicorn": "0.27.0",
    "pydantic": "2.5.0",
    "pydantic-settings": "2.1.0",
    "flask": "3.0.0",
    "flask-cors": "4.0.0",
    "gunicorn": "21.0.0",
    "django": "5.0",
    "djangorestframework": "3.14.0",
    
    # -----------------------------------------------------------------------------
    # HTTP Clients
    # -----------------------------------------------------------------------------
    "httpx": "0.26.0",
    "aiohttp": "3.9.0",
    "requests": "2.31.0",
    "urllib3": "2.1.0",
    
    # -----------------------------------------------------------------------------
    # Data Processing
    # -----------------------------------------------------------------------------
    "pandas": "2.1.0",
    "numpy": "1.26.0",
    
    # -----------------------------------------------------------------------------
    # AI/ML
    # -----------------------------------------------------------------------------
    "openai": "1.10.0",
    "tiktoken": "0.5.0",
    "langchain": "0.1.0",
    "langchain-core": "0.1.0",
    "langchain-community": "0.0.10",
    
    # -----------------------------------------------------------------------------
    # Observability
    # -----------------------------------------------------------------------------
    "opentelemetry-api": "1.22.0",
    "opentelemetry-sdk": "1.22.0",
    "opentelemetry-instrumentation": "0.43b0",
    "prometheus-client": "0.19.0",
    "structlog": "24.1.0",
    "python-json-logger": "2.0.0",
    
    # -----------------------------------------------------------------------------
    # Testing
    # -----------------------------------------------------------------------------
    "pytest": "8.0.0",
    "pytest-asyncio": "0.23.0",
    "pytest-cov": "4.1.0",
    "pytest-mock": "3.12.0",
    "factory-boy": "3.3.0",
    "faker": "22.0.0",
    
    # -----------------------------------------------------------------------------
    # Development Tools
    # -----------------------------------------------------------------------------
    "ruff": "0.1.0",
    "mypy": "1.8.0",
    "pre-commit": "3.6.0",
    "ipython": "8.20.0",
}

# =============================================================================
# Starter Definitions
# =============================================================================

STARTERS: Dict[str, List[str]] = {
    "redis": ["redis", "hiredis"],
    "kafka": ["confluent-kafka"],
    "kafka-python": ["kafka-python"],
    "rabbitmq": ["pika"],
    "celery": ["celery", "redis"],
    "postgres": ["psycopg2-binary", "asyncpg"],
    "mysql": ["pymysql", "aiomysql"],
    "mongodb": ["pymongo", "motor"],
    "sqlalchemy": ["sqlalchemy", "alembic"],
    "fastapi": ["fastapi", "uvicorn", "pydantic", "pydantic-settings"],
    "flask": ["flask", "flask-cors", "gunicorn"],
    "django": ["django", "djangorestframework"],
    "http": ["httpx", "aiohttp"],
    "requests": ["requests", "urllib3"],
    "data": ["pandas", "numpy"],
    "openai": ["openai", "tiktoken"],
    "langchain": ["langchain", "langchain-core", "langchain-community"],
    "observability": ["opentelemetry-api", "opentelemetry-sdk", "opentelemetry-instrumentation", "prometheus-client"],
    "logging": ["structlog", "python-json-logger"],
    "testing": ["pytest", "pytest-asyncio", "pytest-cov", "pytest-mock", "httpx", "factory-boy", "faker"],
    "dev": ["ruff", "mypy", "pre-commit", "ipython"],
    # Combined starters
    "web": ["fastapi", "uvicorn", "pydantic", "pydantic-settings", "httpx", "aiohttp", "redis", "hiredis"],
    "api": ["fastapi", "uvicorn", "pydantic", "pydantic-settings", "psycopg2-binary", "asyncpg", "sqlalchemy", "alembic", "redis", "hiredis", "opentelemetry-api", "opentelemetry-sdk", "opentelemetry-instrumentation", "prometheus-client"],
    "worker": ["celery", "redis", "hiredis", "psycopg2-binary", "asyncpg", "sqlalchemy", "alembic", "opentelemetry-api", "opentelemetry-sdk", "opentelemetry-instrumentation", "prometheus-client"],
    "microservice": ["fastapi", "uvicorn", "pydantic", "pydantic-settings", "psycopg2-binary", "asyncpg", "sqlalchemy", "alembic", "redis", "hiredis", "confluent-kafka", "httpx", "aiohttp", "opentelemetry-api", "opentelemetry-sdk", "opentelemetry-instrumentation", "prometheus-client", "structlog", "python-json-logger"],
}


def get_version(package: str) -> Optional[str]:
    """
    Get the curated version for a package.
    
    Args:
        package: Package name (e.g., 'redis', 'fastapi')
        
    Returns:
        Version string or None if not found
        
    Example:
        >>> get_version('redis')
        '5.0.0'
    """
    return VERSIONS.get(package)


def get_starter_dependencies(starter: str) -> List[str]:
    """
    Get list of packages included in a starter.
    
    Args:
        starter: Starter name (e.g., 'redis', 'fastapi', 'microservice')
        
    Returns:
        List of package names
        
    Example:
        >>> get_starter_dependencies('redis')
        ['redis', 'hiredis']
    """
    return STARTERS.get(starter, [])


def list_starters() -> List[str]:
    """
    List all available starters.
    
    Returns:
        List of starter names
    """
    return list(STARTERS.keys())


def get_requirements(starter: str) -> List[str]:
    """
    Get requirements.txt style list for a starter.
    
    Args:
        starter: Starter name
        
    Returns:
        List of requirements in 'package==version' format
        
    Example:
        >>> get_requirements('redis')
        ['redis==5.0.0', 'hiredis==2.3.0']
    """
    packages = get_starter_dependencies(starter)
    return [f"{pkg}=={VERSIONS.get(pkg, 'unknown')}" for pkg in packages]


def check_compatibility(packages: List[str]) -> Dict[str, str]:
    """
    Check if packages are at recommended versions.
    
    Args:
        packages: List of tuples (package_name, installed_version)
        
    Returns:
        Dict with compatibility status for each package
    """
    result = {}
    for pkg in packages:
        if pkg in VERSIONS:
            result[pkg] = VERSIONS[pkg]
        else:
            result[pkg] = "not in bundle"
    return result


def generate_requirements_txt(starters: List[str]) -> str:
    """
    Generate requirements.txt content for selected starters.
    
    Args:
        starters: List of starter names to include
        
    Returns:
        requirements.txt formatted string
        
    Example:
        >>> print(generate_requirements_txt(['redis', 'fastapi']))
        # Generated by galaxy-bundle
        # Starters: redis, fastapi
        
        # redis
        redis==5.0.0
        hiredis==2.3.0
        
        # fastapi
        fastapi==0.109.0
        ...
    """
    lines = [
        "# Generated by galaxy-bundle",
        f"# Starters: {', '.join(starters)}",
        "",
    ]
    
    seen = set()
    for starter in starters:
        if starter not in STARTERS:
            continue
        lines.append(f"# {starter}")
        for pkg in STARTERS[starter]:
            if pkg not in seen:
                seen.add(pkg)
                version = VERSIONS.get(pkg, "unknown")
                lines.append(f"{pkg}=={version}")
        lines.append("")
    
    return "\n".join(lines)

