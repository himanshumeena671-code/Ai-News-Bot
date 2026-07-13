"""
Logging Module
Centralized logging configuration.
Single Responsibility: Setup and manage logging.
"""

import logging
import os
from datetime import datetime
from pathlib import Path


class LoggerSetup:
    """Handles logging configuration."""
    
    @staticmethod
    def setup_logging(log_dir: str = "logs", log_level: str = "INFO") -> logging.Logger:
        """
        Setup logging with file and console handlers.
        
        Args:
            log_dir: Directory to store log files
            log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
            
        Returns:
            Configured logger instance
        """
        # Create logs directory
        Path(log_dir).mkdir(parents=True, exist_ok=True)
        
        # Create logger
        logger = logging.getLogger('ai_news_bot')
        logger.setLevel(getattr(logging, log_level))
        
        # Remove existing handlers
        logger.handlers.clear()
        
        # Create formatters
        detailed_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        simple_formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s',
            datefmt='%H:%M:%S'
        )
        
        # File handler (detailed)
        log_filename = os.path.join(
            log_dir,
            f"ai_news_bot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        )
        file_handler = logging.FileHandler(log_filename)
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(detailed_formatter)
        logger.addHandler(file_handler)
        
        # Console handler (simple)
        console_handler = logging.StreamHandler()
        console_handler.setLevel(getattr(logging, log_level))
        console_handler.setFormatter(simple_formatter)
        logger.addHandler(console_handler)
        
        logger.info(f"Logging initialized. Log file: {log_filename}")
        return logger
    
    @staticmethod
    def get_logger(name: str) -> logging.Logger:
        """
        Get logger instance for a module.
        
        Args:
            name: Module name
            
        Returns:
            Logger instance
        """
        return logging.getLogger(name)


if __name__ == "__main__":
    logger = LoggerSetup.setup_logging()
    logger.debug("Debug message")
    logger.info("Info message")
    logger.warning("Warning message")
    logger.error("Error message")
