"""
Master Orchestration Module
Coordinates entire AI News Bot pipeline.
Single Responsibility: Orchestrate all phases of the pipeline.
"""

import logging
import sys
import argparse
from typing import List, Dict, Optional
from datetime import datetime
import json

from logger import LoggerSetup
from config import Config
from sources import NewsCollector
from deduplicator import NewsDuplicator
from writer import AIScriptWriter
from tts import TextToSpeech
from editor import VideoEditor
from uploader import UploadManager

logger = LoggerSetup.setup_logging()


class AINewsBot:
    """Master bot that orchestrates the entire pipeline."""
    
    def __init__(self):
        """
        Initialize the bot with all components.
        """
        logger.info("Initializing AI News Bot...")
        
        # Validate configuration
        if not Config.validate():
            raise RuntimeError("Configuration validation failed")
        
        logger.info(Config.get_summary())
        
        # Initialize components
        self.collector = NewsCollector(timeout=Config.REQUEST_TIMEOUT)
        self.deduplicator = NewsDuplicator(similarity_threshold=Config.SIMILARITY_THRESHOLD)
        self.writer = AIScriptWriter(api_key=Config.OPENROUTER_API_KEY)
        self.tts = TextToSpeech(output_dir=Config.AUDIO_OUTPUT_DIR)
        self.editor = VideoEditor(output_dir=Config.VIDEO_OUTPUT_DIR, temp_dir=Config.TEMP_DIR)
        self.uploader = UploadManager(output_dir=Config.UPLOAD_STAGING_DIR)
        
        logger.info("AI News Bot initialized successfully")
    
    def phase_1_collect_news(self) -> bool:
        """
        Phase 1: Collect news from all sources.
        
        Returns:
            True if successful
        """
        logger.info("=" * 60)
        logger.info("PHASE 1: NEWS COLLECTION")
        logger.info("=" * 60)
        
        try:
            # Collect news
            articles = self.collector.collect_all_news()
            
            if not articles:
                logger.warning("No articles collected")
                return False
            
            # Save raw news
            self.collector.save_to_json(Config.RAW_NEWS_FILE)
            
            logger.info(f"✓ Phase 1 Complete: {len(articles)} articles collected")
            return True
            
        except Exception as e:
            logger.error(f"✗ Phase 1 Failed: {str(e)}")
            return False
    
    def phase_2_filter_news(self) -> bool:
        """
        Phase 2: Filter and deduplicate news.
        
        Returns:
            True if successful
        """
        logger.info("=" * 60)
        logger.info("PHASE 2: NEWS FILTERING & DEDUPLICATION")
        logger.info("=" * 60)
        
        try:
            # Load raw news
            articles = self.collector.load_from_json(Config.RAW_NEWS_FILE)
            
            if not articles:
                logger.error("No raw news to filter")
                return False
            
            # Filter and deduplicate
            filtered = self.deduplicator.filter_articles(articles)
            
            if not filtered:
                logger.warning("All articles filtered out")
                return False
            
            # Save filtered news
            self.deduplicator.save_filtered_news(filtered, Config.FILTERED_NEWS_FILE)
            
            logger.info(f"✓ Phase 2 Complete: {len(filtered)} articles after filtering")
            return True
            
        except Exception as e:
            logger.error(f"✗ Phase 2 Failed: {str(e)}")
            return False
    
    def phase_3_generate_scripts(self) -> bool:
        """
        Phase 3: Generate AI scripts and metadata.
        
        Returns:
            True if successful
        """
        logger.info("=" * 60)
        logger.info("PHASE 3: AI SCRIPT GENERATION")
        logger.info("=" * 60)
        
        try:
            # Load filtered news
            with open(Config.FILTERED_NEWS_FILE, 'r', encoding='utf-8') as f:
                articles = json.load(f)
            
            if not articles:
                logger.error("No filtered news to process")
                return False
            
            # Process articles with AI
            packages = self.writer.process_multiple_articles(
                articles,
                limit=Config.MAX_ARTICLES_TO_PROCESS
            )
            
            if not packages:
                logger.error("Failed to generate scripts")
                return False
            
            # Save content packages
            self.writer.save_content_packages(packages, Config.CONTENT_PACKAGES_FILE)
            
            logger.info(f"✓ Phase 3 Complete: {len(packages)} scripts generated")
            return True
            
        except Exception as e:
            logger.error(f"✗ Phase 3 Failed: {str(e)}")
            return False
    
    def phase_4_generate_audio(self) -> bool:
        """
        Phase 4: Generate text-to-speech audio.
        
        Returns:
            True if successful
        """
        logger.info("=" * 60)
        logger.info("PHASE 4: TEXT-TO-SPEECH GENERATION")
        logger.info("=" * 60)
        
        try:
            # Load content packages
            with open(Config.CONTENT_PACKAGES_FILE, 'r', encoding='utf-8') as f:
                packages = json.load(f)
            
            if not packages:
                logger.error("No content packages to process")
                return False
            
            # Generate audio
            packages_with_audio = self.tts.process_multiple_scripts(packages)
            
            if not packages_with_audio:
                logger.error("Failed to generate audio")
                return False
            
            # Save packages with audio
            self.tts.save_packages_with_audio(packages_with_audio, Config.CONTENT_WITH_AUDIO_FILE)
            
            logger.info(f"✓ Phase 4 Complete: {len(packages_with_audio)} audio files generated")
            return True
            
        except Exception as e:
            logger.error(f"✗ Phase 4 Failed: {str(e)}")
            return False
    
    def phase_5_create_videos(self) -> bool:
        """
        Phase 5: Create YouTube Shorts videos.
        
        Returns:
            True if successful
        """
        logger.info("=" * 60)
        logger.info("PHASE 5: VIDEO CREATION")
        logger.info("=" * 60)
        
        try:
            # Load packages with audio
            with open(Config.CONTENT_WITH_AUDIO_FILE, 'r', encoding='utf-8') as f:
                packages = json.load(f)
            
            if not packages:
                logger.error("No packages with audio to process")
                return False
            
            # Create videos
            packages_with_video = self.editor.process_multiple_videos(
                packages,
                audio_dir=Config.AUDIO_OUTPUT_DIR
            )
            
            if not packages_with_video:
                logger.error("Failed to create videos")
                return False
            
            # Save packages with videos
            self.editor.save_packages_with_videos(packages_with_video, Config.FINAL_CONTENT_FILE)
            
            # Cleanup temporary files
            self.editor.cleanup_temp_files()
            
            logger.info(f"✓ Phase 5 Complete: {len(packages_with_video)} videos created")
            return True
            
        except Exception as e:
            logger.error(f"✗ Phase 5 Failed: {str(e)}")
            return False
    
    def phase_6_prepare_upload(self) -> bool:
        """
        Phase 6: Prepare for upload.
        
        Returns:
            True if successful
        """
        logger.info("=" * 60)
        logger.info("PHASE 6: UPLOAD PREPARATION")
        logger.info("=" * 60)
        
        try:
            # Prepare upload batch
            upload_batch = self.uploader.load_and_prepare_upload(Config.FINAL_CONTENT_FILE)
            
            if not upload_batch:
                logger.warning("No videos ready for upload")
                return False
            
            logger.info(f"✓ Phase 6 Complete: {len(upload_batch)} videos prepared for upload")
            return True
            
        except Exception as e:
            logger.error(f"✗ Phase 6 Failed: {str(e)}")
            return False
    
    def run_full_pipeline(self) -> bool:
        """
        Run the complete pipeline from start to finish.
        
        Returns:
            True if all phases completed successfully
        """
        logger.info("\n" + "#" * 60)
        logger.info("# AI NEWS BOT - FULL PIPELINE EXECUTION")
        logger.info(f"# Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        logger.info("#" * 60 + "\n")
        
        try:
            # Execute all phases
            phases = [
                ("Collection", self.phase_1_collect_news),
                ("Filtering", self.phase_2_filter_news),
                ("Script Generation", self.phase_3_generate_scripts),
                ("Audio Generation", self.phase_4_generate_audio),
                ("Video Creation", self.phase_5_create_videos),
                ("Upload Preparation", self.phase_6_prepare_upload),
            ]
            
            results = []
            for phase_name, phase_func in phases:
                success = phase_func()
                results.append((phase_name, success))
                
                if not success and phase_name not in ["Upload Preparation"]:
                    logger.error(f"Pipeline halted at {phase_name}")
                    break
            
            # Summary
            logger.info("\n" + "=" * 60)
            logger.info("PIPELINE EXECUTION SUMMARY")
            logger.info("=" * 60)
            
            for phase_name, success in results:
                status = "✓ PASS" if success else "✗ FAIL"
                logger.info(f"{phase_name:.<40} {status}")
            
            successful_phases = sum(1 for _, success in results if success)
            total_phases = len(results)
            
            logger.info(f"\nResult: {successful_phases}/{total_phases} phases completed")
            logger.info(f"Completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            logger.info("=" * 60 + "\n")
            
            if successful_phases == total_phases:
                logger.info("🎉 PIPELINE SUCCESSFUL - Videos ready for upload!")
                return True
            else:
                logger.warning(f"⚠️  PIPELINE PARTIALLY COMPLETE - {successful_phases}/{total_phases} phases")
                return False
            
        except Exception as e:
            logger.error(f"\n✗ PIPELINE FAILED: {str(e)}")
            return False
    
    def run_collection_only(self) -> bool:
        """Run only news collection phase."""
        return self.phase_1_collect_news()
    
    def run_up_to_scripts(self) -> bool:
        """Run up to script generation."""
        return all([
            self.phase_1_collect_news(),
            self.phase_2_filter_news(),
            self.phase_3_generate_scripts(),
        ])
    
    def run_up_to_videos(self) -> bool:
        """Run up to video creation."""
        return all([
            self.phase_1_collect_news(),
            self.phase_2_filter_news(),
            self.phase_3_generate_scripts(),
            self.phase_4_generate_audio(),
            self.phase_5_create_videos(),
        ])


def main():
    """
    Main entry point.
    """
    parser = argparse.ArgumentParser(
        description='AI News Bot - Automated YouTube Shorts Generator',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python bot.py --run-full              # Run complete pipeline
  python bot.py --collect-news          # Only collect news
  python bot.py --up-to-scripts         # Up to script generation
  python bot.py --up-to-videos          # Up to video creation
        """
    )
    
    parser.add_argument(
        '--run-full',
        action='store_true',
        help='Run complete pipeline (default)'
    )
    parser.add_argument(
        '--collect-news',
        action='store_true',
        help='Run only news collection phase'
    )
    parser.add_argument(
        '--up-to-scripts',
        action='store_true',
        help='Run up to script generation'
    )
    parser.add_argument(
        '--up-to-videos',
        action='store_true',
        help='Run up to video creation'
    )
    parser.add_argument(
        '--version',
        action='version',
        version='AI News Bot v1.0.0'
    )
    
    args = parser.parse_args()
    
    try:
        bot = AINewsBot()
        
        # Determine which pipeline to run
        if args.collect_news:
            success = bot.run_collection_only()
        elif args.up_to_scripts:
            success = bot.run_up_to_scripts()
        elif args.up_to_videos:
            success = bot.run_up_to_videos()
        else:
            success = bot.run_full_pipeline()
        
        # Exit with appropriate code
        sys.exit(0 if success else 1)
        
    except KeyboardInterrupt:
        logger.info("\nPipeline interrupted by user")
        sys.exit(130)
    except Exception as e:
        logger.error(f"Fatal error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
