import logging
from datetime import datetime
import os

class GameLogger:
    def __init__(self):
        # Set up logging
        logging.basicConfig(
            filename=f'game_log_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log',
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger('CarCare')

    def info(self, message):
        """Log info message"""
        self.logger.info(message)
        print(f"INFO: {message}")

    def error(self, message):
        """Log error message"""
        self.logger.error(message)
        print(f"ERROR: {message}")

    def warning(self, message):
        """Log warning message"""
        self.logger.warning(message)
        print(f"WARNING: {message}")

    def debug(self, message):
        """Log debug message"""
        self.logger.debug(message)
        print(f"DEBUG: {message}")