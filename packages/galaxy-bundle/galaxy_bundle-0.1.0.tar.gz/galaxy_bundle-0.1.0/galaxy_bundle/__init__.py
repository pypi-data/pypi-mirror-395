"""
Galaxy Bundle - A BOM-style Dependency Management Package for Python

Similar to Spring Boot Parent POM, this package provides:
- Curated dependency versions that work well together
- Multiple "starters" for different use cases (redis, kafka, fastapi, etc.)
- Easy installation: `pip install galaxy-bundle[redis,kafka]`

Usage:
    # Install specific starters
    pip install galaxy-bundle[redis]
    pip install galaxy-bundle[kafka]
    pip install galaxy-bundle[fastapi]
    
    # Install combined starters
    pip install galaxy-bundle[microservice]  # FastAPI + Postgres + Redis + Kafka + Observability
    pip install galaxy-bundle[api]           # FastAPI + Postgres + Redis + Observability
    pip install galaxy-bundle[worker]        # Celery + Redis + Postgres + Observability
    
    # Install everything (for development)
    pip install galaxy-bundle[all]
"""

from galaxy_bundle.versions import (
    VERSIONS,
    get_version,
    get_starter_dependencies,
    list_starters,
    check_compatibility,
)
from galaxy_bundle.info import (
    show_info,
    show_starters,
    show_versions,
)

__version__ = "0.1.0"
__all__ = [
    "VERSIONS",
    "get_version",
    "get_starter_dependencies", 
    "list_starters",
    "check_compatibility",
    "show_info",
    "show_starters",
    "show_versions",
]

