import os
import logging
from logging.handlers import RotatingFileHandler

class LoggerService:
    """
    Centralized logging service for the application.
    Provides consistent logging configuration across all services.
    """
    _instance = None
    _initialized = False
    
    
    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = LoggerService()
        return cls._instance
    
    
    def __init__(self):
        """Initialize the logging service if not already initialized."""
        if not LoggerService._initialized:
            # Create logs directory if it doesn't exist
            self.log_dir = os.path.join(os.path.dirname(__file__), '..', 'logs')
            os.makedirs(self.log_dir, exist_ok=True)
            
            # Configure root logger
            logging.basicConfig(
                level=logging.INFO,
                format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            )
            
            # Configure file handler with rotation
            self.file_handler = RotatingFileHandler(
                os.path.join(self.log_dir, 'application.log'),
                maxBytes=10485760,  # 10MB
                backupCount=10
            )
            self.file_handler.setFormatter(
                logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            )
            
            LoggerService._initialized = True
    
    
    def get_logger(self, name):
        """
        Get a logger for a specific service or component.
        
        Args:
            name: Name of the service/component
            
        Returns:
            Logger instance configured with the application's settings
        """
        logger = logging.getLogger(name)
        logger.addHandler(self.file_handler)
        return logger