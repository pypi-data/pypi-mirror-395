import asyncio
import time
import logging
from hestia_logger.core.custom_logger import get_logger
from hestia_logger.decorators import log_execution
from hestia_logger.internal_logger import hestia_internal_logger

# Define service loggers (NO NEED to define `app_logger`, handled internally)
logger_api = get_logger("api_service", log_level=logging.DEBUG)
logger_db = get_logger("database_service", log_level=logging.WARNING)


@log_execution
def sync_function(x, y):
    """
    A simple synchronous function to test logging and decorator.
    """
    logger_api.info("Inside sync_function.")
    return x + y


@log_execution
async def async_function(x, y):
    """
    A simple asynchronous function to test logging and decorator.
    """
    logger_db.info("Inside async_function.")
    await asyncio.sleep(1)
    return x * y


async def test_hestia_logging():
    """
    Logs structured messages to multiple loggers to test all log levels,
    decorator functionality, and log rotation.
    """
    hestia_internal_logger.info("🎉 Starting HESTIA Logger Test...")

    # Log structured JSON message (should go to `app.log`)
    logger_api.info({"message": "Main script started.", "event": "app_init"})

    # Test Decorator (Sync)
    print("[DEBUG] Running sync function...")
    sync_result = sync_function(5, 10)
    print(f"[DEBUG] Sync result: {sync_result}")

    # Test Decorator (Async)
    print("[DEBUG] Running async function...")
    async_result = await async_function(2, 3)
    print(f"[DEBUG] Async result: {async_result}")

    # API Logger Test (DEBUG + INFO)
    logger_api.debug(
        "API Debug: Testing API request logging."
    )  # Will go to service log
    logger_api.info("API Received request.")  # Will go to service log

    # Database Logger Test (WARNING + ERROR + CRITICAL)
    logger_db.warning(
        "Database Warning: Query execution slow."
    )  # Will go to service log
    logger_db.error("Database Error: Connection failed!")  # Will go to service log
    logger_db.critical(
        "CRITICAL Database Error: System Down!"
    )  # Will go to service log

    # Log completion message (should go to `app.log`)
    logger_db.info({"message": "Main script completed.", "event": "app_done"})

    # Simulate log rotation by generating many logs
    print("[DEBUG] Simulating log rotation...")
    for i in range(100):
        logger_api.info(f"Log rotation test entry {i+1}")

    hestia_internal_logger.info("HESTIA Logger Test Completed!")


# Run the test and ensure logs are written immediately
asyncio.run(test_hestia_logging())

print("[DEBUG] Test script completed.")
