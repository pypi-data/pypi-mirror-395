import time
import random
from datetime import datetime
from hestia_logger import get_logger

# Get the logger
logger = get_logger("microservice")

# Possible log levels
LOG_LEVELS = ["INFO", "DEBUG", "WARNING", "ERROR", "CRITICAL"]

# Artificial log messages
LOG_MESSAGES = [
    "User login successful",
    "User login failed: Invalid credentials",
    "Payment processed successfully",
    "Database connection lost",
    "Cache invalidated",
    "API request timeout",
    "User session expired",
    "Unauthorized access attempt detected",
]


def generate_log():
    """Generates and logs a random log entry using Hestia Logger."""
    log_level = random.choice(LOG_LEVELS)
    log_message = random.choice(LOG_MESSAGES)

    # Simulate structured logging
    log_data = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "user_id": random.randint(1000, 9999),
        "session_id": f"session-{random.randint(10000, 99999)}",
    }

    # Log based on random log level
    if log_level == "INFO":
        logger.info(log_message, extra=log_data)
    elif log_level == "DEBUG":
        logger.debug(log_message, extra=log_data)
    elif log_level == "WARNING":
        logger.warning(log_message, extra=log_data)
    elif log_level == "ERROR":
        logger.error(log_message, extra=log_data)
    elif log_level == "CRITICAL":
        logger.critical(log_message, extra=log_data)


def main():
    """Continuously logs artificial events using Hestia Logger."""
    while True:
        generate_log()
        time.sleep(random.uniform(1, 3))  # Random interval between logs


if __name__ == "__main__":
    main()
