# EasyCore

Core utilities for building small Python services with FastAPI and Celery.

## Features

- **FastAPI**: Pre-configured app factory with router management and exception handlers
- **Celery**: Custom task class with correlation ID tracking for distributed tracing
- **Logger**: Correlation ID middleware and context management for request tracking
- **HTTPX**: Monkey patching for enhanced logging
- **Settings**: Pydantic-based settings for Redis, MongoDB, RabbitMQ, API, and more
- **Abstractions**: Singleton metaclass and common patterns

## Installation

```bash
pip install easycore
```

## Quick Start

```python
from easycore import create_fastapi_api_app, create_celery_custom_task_class

# Create FastAPI app
app = create_fastapi_api_app(
    service_name="my-service",
    service_path="api/v1",
    routers=[my_router],
    custom_exc_handlers=None
)

# Create Celery custom task
CustomTask = create_celery_custom_task_class(logger)
```

## Components

- `efastapi`: FastAPI app factories
- `ecelery`: Celery task utilities with correlation ID support
- `elogger`: Logging with correlation ID tracking
- `ehttpx`: HTTPX logging patches
- `env_settings`: Pydantic settings for common services
- `connectors`: API connector utilities
- `abstractions`: Common patterns (Singleton, etc.)
