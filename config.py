"""
Configuration Module
Centralized configuration management.
Single Responsibility: Handle all configuration settings.
"""

import os
import logging
from dotenv import load_dotenv
from typing import Optional

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)


class Config:
    """Application configuration."""
    
    # API Keys
    OPENROUTER_API_KEY = os.getenv('OPENROUTER_API_KEY')
    GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
    
    # Paths
    RAW_NEWS_FILE = "raw_news.json"
    FILTERED_NEWS_FILE = "filtered_news.json"
    CONTENT_PACKAGES_FILE = "content_packages.json"
    CONTENT_WITH_AUDIO_FILE = "content_with_audio.json"
    FINAL_CONTENT_FILE = "final_content.json"
    UPLOAD_BATCH_FILE = "upload_batch.json"
    
    # Directories
    AUDIO_OUTPUT_DIR = "audio_output"
    VIDEO_OUTPUT_DIR = "video_output"
    UPLOAD_STAGING_DIR = "upload_staging"
    TEMP_DIR = "temp"
    
    # Processing Limits
    MAX_ARTICLES_TO_PROCESS = 5  # Max videos per day
    MAX_SOURCES = 7  # Number of news sources
    
    # Video Settings
    VIDEO_WIDTH = 1080
    VIDEO_HEIGHT = 1920
    VIDEO_FPS = 30
    VIDEO_DURATION = 45  # seconds
    VIDEO_BITRATE = "5000k"
    
    # TTS Settings
    TTS_LANGUAGE = 'en'
    TTS_SPEED = 1.0
    TTS_PROVIDER = 'gtts'  # 'gtts' or 'pyttsx3'
    
    # Deduplication
    SIMILARITY_THRESHOLD = 0.85  # 0-1 scale
    
    # Timeouts
    REQUEST_TIMEOUT = 10  # seconds
    API_TIMEOUT = 30  # seconds
    
    # Logging
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    
    @classmethod
    def validate(cls) -> bool:
        """
        Validate configuration.
        
        Returns:
            True if all required configs are set
        """
        required_keys = [
            'OPENROUTER_API_KEY',
        ]
        
        missing = [key for key in required_keys if not getattr(cls, key)]
        
        if missing:
            logger.error(f"Missing configuration: {', '.join(missing)}")
            return False
        
        logger.info("Configuration validated successfully")
        return True
    
    @classmethod
    def get_summary(cls) -> str:
        """
        Get configuration summary.
        
        Returns:
            String with configuration details
        """
        return f"""
AI News Bot Configuration
========================
Processing:
  - Max articles: {cls.MAX_ARTICLES_TO_PROCESS}
  - Max sources: {cls.MAX_SOURCES}
  - Similarity threshold: {cls.SIMILARITY_THRESHOLD}

Video Settings:
  - Resolution: {cls.VIDEO_WIDTH}x{cls.VIDEO_HEIGHT}
  - Duration: {cls.VIDEO_DURATION}s
  - FPS: {cls.VIDEO_FPS}
  - Bitrate: {cls.VIDEO_BITRATE}

TTS Settings:
  - Language: {cls.TTS_LANGUAGE}
  - Provider: {cls.TTS_PROVIDER}
  - Speed: {cls.TTS_SPEED}x

Directories:
  - Audio: {cls.AUDIO_OUTPUT_DIR}
  - Video: {cls.VIDEO_OUTPUT_DIR}
  - Upload staging: {cls.UPLOAD_STAGING_DIR}
  - Temp: {cls.TEMP_DIR}
"""


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format=Config.LOG_FORMAT
    )
    
    print(Config.get_summary())
    print(f"\nValidation: {'✓ PASS' if Config.validate() else '✗ FAIL'}")
