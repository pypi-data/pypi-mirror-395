# FastAPI MongoDB Logger

A comprehensive logging package for FastAPI applications that stores endpoint logs and custom events in MongoDB.

## Installation

```bash
pip install fastapi-mongo-logger-mateoramos
```

## Quick Start

### 1. Basic Setup

```python
from fastapi import FastAPI
from fastapi_mongo_logger import MongoLogger, LoggingMiddleware

app = FastAPI()

# Initialize logger
logger = MongoLogger(
    mongo_url="mongodb://localhost:27017",
    database_name="my_app_logs",
    collection_name="api_logs"
)

# Add middleware for automatic endpoint logging
app.add_middleware(LoggingMiddleware, logger=logger)

@app.get("/")
async def root():
    return {"message": "Hello World"}
```

### 2. Manual Logging with Decorators

```python
from fastapi_mongo_logger import log_endpoint, log_function

@log_endpoint(logger, user_type="admin")
async def admin_function():
    # Your code here
    pass

@log_function(logger, event_type="data_processing")
def process_data():
    # Your code here
    pass
```

### 3. Custom Logging

```python
# Log custom events anywhere in your code
await logger.log_custom("user_action", {
    "user_id": "123",
    "action": "login",
    "ip_address": "192.168.1.1"
})
```

## Features

- **Automatic endpoint logging** via middleware
- **Manual logging** with decorators
- **Custom event logging** for any part of your application
- **Comprehensive data capture**: request/response bodies, headers, timing, errors
- **Async/sync function support**
- **Flexible data storage** in MongoDB

## Configuration Options

- `log_request_body`: Enable/disable request body logging (default: True)
- `log_response_body`: Enable/disable response body logging (default: False)
- Custom fields can be added to any log entry