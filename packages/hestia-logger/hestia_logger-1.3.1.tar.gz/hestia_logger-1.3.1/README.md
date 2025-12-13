# HESTIA Logger 

[![Python](https://img.shields.io/badge/Python-3.11%2B-darkcyan)](https://pypi.org/project/hestia-logger/)
[![PyPI - Version](https://img.shields.io/pypi/v/hestia-logger?label=PyPI%20Version&color=green)](https://pypi.org/project/hestia-logger/)
[![PyPI Downloads](https://static.pepy.tech/badge/hestia-logger)](https://pepy.tech/projects/hestia-logger)
[![License: Apache 2.0](https://img.shields.io/badge/License-Apache2.0-orange.svg)](https://github.com/fox-techniques/hestia-logger/blob/main/LICENSE)
[![GitHub](https://img.shields.io/badge/GitHub-hestia--logger-181717?logo=github)](https://github.com/fox-techniques/hestia-logger)


**A high-performance, structured logging system for Python applications.**  
Supports **async logging, Elastic Stack integration, structured JSON logs, and colorized console output.**

## Key Features

- **Structured JSON & Human-Readable Logs** (Optimized for Elastic Stack)  
- **Dynamic Metadata Support** (`user_id`, `request_id`, etc.)  
- **Application-Aware Logging** (`get_logger("my_app")`)  
- **Multi-Thread & Multi-Process Friendly** (`thread_id`, `process_id`)  
- **Colored Console Output** (`INFO` in green, `ERROR` in red, etc.)  
- **Internal Logger for Debugging the Logging System**  
- **Supports File Rotation & Future Cloud Integration**  

---

## Documentation

The full documentation is available on [GitHub Pages](https://fox-techniques.github.io/hestia-logger/).

---

##  Installation

```bash
pip install hestia-logger
```

##  Usage

**1. Basic Setup**

```python
from hestia_logger import get_logger

# Get a logger instance
logger = get_logger("development")

# Log messages with different levels
logger.debug("This is a DEBUG log")
logger.info("Application started successfully")
logger.warning("Low disk space warning")
logger.error("Failed to connect to database")
logger.critical("System is down!")
```

**2. Decorator Example**

```python 
from hestia_logger import get_logger
from hestia_logger.decorators import log_execution

# Initialize the logger
logger = get_logger("decorator")

@log_execution
def add_numbers(a, b):
     """Adds two numbers and returns the result."""
     return a + b

@log_execution
def simulate_task():
     """Simulates a task that takes time."""
     import time
     time.sleep(2)
     return "Task completed!"

# Call the functions
if __name__ == "__main__":
     result = add_numbers(5, 10)
     logger.info(f"Result: {result}")

     task_status = simulate_task()
     logger.info(f"Task Status: {task_status}")

```


**3. Adding Custom Metadata**

```python
from hestia_logger import get_logger

logger = get_logger("my_application", metadata={"user_id": "12345", 
                                                "request_id": "abcd-xyz"})

logger.info("User login successful")
```

## Log File Structure

HESTIA Logger creates two main log files:


|File|	Format|	Purpose|
|---|---|---|
|**app.log**	|JSON	|Machine-readable (Elastic Stack)|
|**all.log**	|Text	|Human-readable debug logs|

## Log Colors (Console Output)

|Log Level|	Color|
|---|---|
|DEBUG|	🔵 Blue|
|INFO|	⚫ Black|
|WARNING|	🟡 Yellow|
|ERROR|	🔴 Red|
|CRITICAL|	🔥 Bold Red|

## Configuration

HESTIA Logger supports environment-based configuration via .env or export:

```bash
# Environment Variables
ENVIRONMENT=local
LOG_LEVEL=INFO
```

## Example Log Output

### Console (Colorized) +  all.log (Text Format)

```yaml
2025-03-06 20:40:23 - my_application - INFO - Application started!
```

### app.log (JSON Format - Elastic Stack Ready)

```json
{
    "timestamp": "2025-03-06T20:40:23.286Z",
    "level": "INFO",
    "hostname": "server-1",
    "container_id": "N/A",
    "application": "my_application",
    "event": "Application started successfully!",
    "thread": 12345,
    "process": 56789,
    "uuid": "d3f5b2c1-4f27-46a8-b3d2-f4a7a5c3ef29",
    "metadata": {
        "user_id": "12345",
        "request_id": "abcd-xyz"
    }
}
```

## License

This project is licensed under the Apache 2.0 License - see the [LICENSE](https://github.com/fox-techniques/hestia-logger/blob/main/LICENSE) file for details.