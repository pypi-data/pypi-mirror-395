# 📄 User Guide

This guide provides **simple examples** to demonstrate how to use HESTIA Logger:

## **Python during development**  

=== "Script Example"

     Use it in your script:

     ```python title="script_example.py" linenums="1"
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

     Run the Script

     ```bash
     uv run python example.py

     ```


     **📌 Expected output in `logs/app.log`:**
     
     ```json
     {"timestamp": "2025-03-14T13:57:41.Z", "level": "INFO", "service": "development", "environment": "local", "hostname": "ubuntu", "app_version": "1.0.0", "message": "Application started successfully"}
     {"timestamp": "2025-03-14T13:57:41.Z", "level": "WARNING", "service": "development", "environment": "local", "hostname": "ubuntu", "app_version": "1.0.0", "message": "Low disk space warning"}
     {"timestamp": "2025-03-14T13:57:41.Z", "level": "ERROR", "service": "development", "environment": "local", "hostname": "ubuntu", "app_version": "1.0.0", "message": "Failed to connect to database"}
     {"timestamp": "2025-03-14T13:57:41.Z", "level": "CRITICAL", "service": "development", "environment": "local", "hostname": "ubuntu", "app_version": "1.0.0", "message": "System is down!"}

     ```
     **📌 Expected output in `logs/development.log`:**
     ```text
     2025-03-14 13:57:41,052 - development - INFO - Application started successfully
     2025-03-14 13:57:41,052 - development - WARNING - Low disk space warning
     2025-03-14 13:57:41,053 - development - ERROR - Failed to connect to database
     2025-03-14 13:57:41,053 - development - CRITICAL - System is down!
     ```

     
=== "Decorator Example"
     
     **HESTIA** Logger provides a **decorator** to automatically log function execution.

     ```python title="example_decorator.py" linenums="1"

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

     **📌 Expected log output:**
     
     ```json
     {"timestamp": "2025-03-14T12:35:00.123Z", "level": "INFO", "service": "decorator", "message": "📌 Started: add_numbers()"}
     {"timestamp": "2025-03-14T12:35:00.125Z", "level": "INFO", "service": "decorator", "message": "✅ Finished: add_numbers() in 0.0004 sec"}
     
     ```

=== "Metadata Example"

     **HESTIA** supports custom metadata to extend the default content of the logger instance:

     ```python title="example_metadata.py" linenums="1"
     from hestia_logger import get_logger

     logger = get_logger("my_application", metadata={"user_id": "12345", 
                                                     "request_id": "abcd-xyz"})

     logger.info("User login successful")
     ```

     
     **📌 Expected output in `logs/app.log`:**

     ```json
     {
          "timestamp": "2025-03-14T14:04:30.Z", 
          "level": "INFO", 
          "service": "my_application", 
          "environment": "local", 
          "hostname": "ubuntu", 
          "app_version": "1.0.0", 
          "user_id": "12345", 
          "request_id": "abcd-xyz", 
          "message": "User login successful"
     }
     ```


     **📌 Expected output in `logs/my_application.log`:**

     ```text
     2025-03-14 14:04:30,840 - my_application - INFO - User login successful
     ```

---


## **Running inside a container**  

**Step 1.** Create a simple script that logs messages inside a container.

```python title="app.py" linenums="1"
from hestia_logger import get_logger
import time

# Get logger instance
logger = get_logger("container_test")

logger.info("🚀 Starting Hestia Logger inside Docker...")

for i in range(5):
    logger.debug(f"Iteration {i+1}: Debugging log message")
    logger.info(f"Iteration {i+1}: Info log message")
    time.sleep(1)  # Simulate work

logger.warning("⚠️ This is a warning log inside Docker.")
logger.error("❌ This is an error log inside Docker.")
logger.critical("🔥 Critical system failure inside Docker!")

logger.info("✅ Hestia Logger test completed inside Docker.")

```

**Step 2.** Create a Dockerfile:

```sh title="Dockerfile" linenums="1"
# Use official Python + uv image
FROM ghcr.io/astral-sh/uv:python3.10-alpine

# Set working directory
WORKDIR /app

# Copy project files
COPY . .

# Install dependencies defined in pyproject.toml (no dev deps)
RUN uv sync --no-dev

# Make sure the project virtualenv is on PATH (optional but handy)
ENV PATH="/app/.venv/bin:$PATH"

# Set environment variables
ENV ENVIRONMENT="container"
ENV LOGS_DIR="/var/logs"
ENV LOG_LEVEL="INFO"
ENV ENABLE_INTERNAL_LOGGER="true"

# Create logs directory with proper permissions
RUN mkdir -p /var/logs && chmod -R 777 /var/logs

# Define entrypoint (runs with the uv-managed environment)
CMD ["uv", "run", "python", "app.py"]
```

**Step 3.** Build and run the  Docker Container

Build the container:

```sh
docker build -t hestia-test .
```

Run the container:

```sh
docker run --rm -v $(pwd)/logs:/var/logs hestia-test

```

The `-v $(pwd)/logs:/var/logs` mounts the logs folder from the container to your local machine.
This ensures logs persist outside the container.