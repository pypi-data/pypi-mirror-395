"""
Galaxy Bundle - Information Display Utilities

Provides functions to display information about available starters and versions.
"""

from typing import Optional
from galaxy_bundle.versions import VERSIONS, STARTERS


def show_info() -> None:
    """Display general information about galaxy-bundle."""
    print("""
╔═══════════════════════════════════════════════════════════════════════════════╗
║                              🌌 Galaxy Bundle                                  ║
║                    A BOM-style Dependency Management Package                   ║
╚═══════════════════════════════════════════════════════════════════════════════╝

Galaxy Bundle provides curated, tested dependency versions for Python projects.
Similar to Spring Boot Parent POM, it ensures all your dependencies work well together.

📦 Installation Examples:

    # Install specific starters
    pip install galaxy-bundle[redis]
    pip install galaxy-bundle[kafka]
    pip install galaxy-bundle[fastapi]
    
    # Install multiple starters
    pip install galaxy-bundle[redis,kafka,fastapi]
    
    # Install combined starters
    pip install galaxy-bundle[microservice]
    pip install galaxy-bundle[api]
    pip install galaxy-bundle[worker]
    
    # Install everything (development)
    pip install galaxy-bundle[all]

📚 Available Functions:
    
    from galaxy_bundle import (
        show_starters,     # List all available starters
        show_versions,     # Show curated package versions
        get_version,       # Get version for a specific package
        VERSIONS,          # Dict of all package versions
    )

🔗 GitHub: https://github.com/phodal/galaxy-bundle
""")


def show_starters(starter: Optional[str] = None) -> None:
    """
    Display available starters and their packages.
    
    Args:
        starter: Optional specific starter to show details for
    """
    if starter:
        if starter not in STARTERS:
            print(f"❌ Starter '{starter}' not found.")
            print(f"   Available starters: {', '.join(STARTERS.keys())}")
            return
        
        packages = STARTERS[starter]
        print(f"\n📦 Starter: {starter}")
        print("   Packages included:")
        for pkg in packages:
            version = VERSIONS.get(pkg, "unknown")
            print(f"   • {pkg}=={version}")
        print(f"\n   Install with: pip install galaxy-bundle[{starter}]")
        return
    
    print("""
╔═══════════════════════════════════════════════════════════════════════════════╗
║                         🚀 Available Starters                                  ║
╚═══════════════════════════════════════════════════════════════════════════════╝
""")
    
    categories = {
        "Cache": ["redis"],
        "Message Queues": ["kafka", "kafka-python", "rabbitmq", "celery"],
        "Databases": ["postgres", "mysql", "mongodb", "sqlalchemy"],
        "Web Frameworks": ["fastapi", "flask", "django"],
        "HTTP Clients": ["http", "requests"],
        "Data Processing": ["data"],
        "AI/ML": ["openai", "langchain"],
        "Observability": ["observability", "logging"],
        "Testing": ["testing"],
        "Development": ["dev"],
        "Combined (Recommended)": ["web", "api", "worker", "microservice"],
    }
    
    for category, starters_list in categories.items():
        print(f"📁 {category}:")
        for s in starters_list:
            if s in STARTERS:
                pkg_count = len(STARTERS[s])
                print(f"   • {s:<20} ({pkg_count} packages)")
        print()
    
    print("💡 Use show_starters('fastapi') to see packages in a specific starter")
    print("💡 Install with: pip install galaxy-bundle[starter1,starter2]")


def show_versions(category: Optional[str] = None) -> None:
    """
    Display curated package versions.
    
    Args:
        category: Optional category filter
    """
    print("""
╔═══════════════════════════════════════════════════════════════════════════════╗
║                         📋 Curated Package Versions                            ║
╚═══════════════════════════════════════════════════════════════════════════════╝
""")
    
    categories = {
        "Cache": ["redis", "hiredis"],
        "Message Queues": ["confluent-kafka", "kafka-python", "pika", "celery"],
        "Databases": ["psycopg2-binary", "asyncpg", "pymysql", "aiomysql", "pymongo", "motor", "sqlalchemy", "alembic"],
        "Web Frameworks": ["fastapi", "uvicorn", "pydantic", "pydantic-settings", "flask", "flask-cors", "gunicorn", "django", "djangorestframework"],
        "HTTP Clients": ["httpx", "aiohttp", "requests", "urllib3"],
        "Data Processing": ["pandas", "numpy"],
        "AI/ML": ["openai", "tiktoken", "langchain", "langchain-core", "langchain-community"],
        "Observability": ["opentelemetry-api", "opentelemetry-sdk", "opentelemetry-instrumentation", "prometheus-client", "structlog", "python-json-logger"],
        "Testing": ["pytest", "pytest-asyncio", "pytest-cov", "pytest-mock", "factory-boy", "faker"],
        "Development": ["ruff", "mypy", "pre-commit", "ipython"],
    }
    
    if category:
        if category not in categories:
            print(f"❌ Category '{category}' not found.")
            print(f"   Available categories: {', '.join(categories.keys())}")
            return
        
        print(f"📁 {category}:")
        for pkg in categories[category]:
            version = VERSIONS.get(pkg, "unknown")
            print(f"   {pkg:<30} {version}")
        return
    
    for cat, packages in categories.items():
        print(f"📁 {cat}:")
        for pkg in packages:
            version = VERSIONS.get(pkg, "unknown")
            print(f"   {pkg:<30} {version}")
        print()
    
    print(f"📊 Total packages: {len(VERSIONS)}")

