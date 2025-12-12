"""
Logging utility module using loguru.

This module provides a centralized logger that can be configured
to write logs to a file path specified via environment variables.
"""
import sys
import os
from loguru import logger


def setup_logger():
    """
    Set up the logger with configuration from environment variables.
    
    Environment variables:
    - CLIENT_LOG_ENABLED: Enable/disable logging (default: 'true')
    - CLIENT_LOG_LEVEL: Logging level (default: 'INFO')
    - CLIENT_LOG_FILE_PATH: File path for log output (optional)
    
    This function configures loguru based on the following logic:
    1. If logging is disabled (CLIENT_LOG_ENABLED=false): Only WARNING and ERROR to stderr
    2. If logging is enabled and CLIENT_LOG_FILE_PATH is set: Log to both file and stderr at LOG_LEVEL
    3. If logging is enabled but no CLIENT_LOG_FILE_PATH: Log to stderr only at LOG_LEVEL
    """
    # Remove default handler
    logger.remove()
    
    # Read configuration from environment variables
    log_enabled = os.getenv('LOG_ENABLED', 'false').lower() == 'true'
    log_level = os.getenv('LOG_LEVEL', 'INFO').upper()
    log_file_path = os.getenv('LOG_FILE_PATH', None)
    
    # Case 1: Logging is disabled - only WARNING and ERROR to stderr
    if not log_enabled:
        logger.add(
            sys.stderr,
            format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
            level="WARNING"
        )
        return logger
    
    # Case 2: Logging is enabled with log_file_path - log to both file and stderr
    if log_file_path:
        # Add file handler
        logger.add(
            log_file_path,
            rotation="10 MB",  # Rotate when file reaches 10 MB
            retention="7 days",  # Keep logs for 7 days
            compression="zip",  # Compress rotated logs
            format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
            level=log_level
        )
        # Add stderr handler
        logger.add(
            sys.stderr,
            format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
            level=log_level
        )
        logger.info(f"Logger configured to write to file: {log_file_path} and stderr at level: {log_level}")
    else:
        # Case 3: Logging is enabled without log_file_path - log to stderr only
        logger.add(
            sys.stderr,
            format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
            level=log_level
        )
        logger.info(f"Logger configured to write to stderr only at level: {log_level}")
    
    return logger


def get_logger():
    """
    Get the configured logger instance.
    
    Returns:
        logger: The loguru logger instance
    """
    return logger


# Initialize logger when module is imported
setup_logger()
