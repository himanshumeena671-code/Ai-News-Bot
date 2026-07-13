"""
Phase 3: Text-to-Speech Module
Generates voice narration using free TTS providers.
Single Responsibility: Convert scripts to audio.
"""

import logging
import json
import os
from typing import Dict, List, Optional
from datetime import datetime
import subprocess
import tempfile
from pathlib import Path

logger = logging.getLogger(__name__)


class TextToSpeech:
    """Converts text to speech using free TTS providers."""
    
    def __init__(self, output_dir: str = "audio_output"):
        """
        Initialize TTS converter.
        
        Args:
            output_dir: Directory to store generated audio files
        """
        self.output_dir = output_dir
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        
        # Check for pyttsx3 or gTTS availability
        self.use_gtts = self._check_gtts()
        logger.info(f"TTS initialized. Using: {'gTTS' if self.use_gtts else 'pyttsx3'}")
    
    def _check_gtts(self) -> bool:
        """
        Check if gTTS is available.
        
        Returns:
            True if gTTS is available
        """
        try:
            from gtts import gTTS
            logger.info("gTTS is available")
            return True
        except ImportError:
            logger.warning("gTTS not available, will use pyttsx3")
            return False
    
    def generate_speech_gtts(self, text: str, filename: str, speed: float = 1.0) -> bool:
        """
        Generate speech using Google Text-to-Speech (gTTS).
        Free tier works well for short texts.
        
        Args:
            text: Text to convert to speech
            filename: Output audio filename
            speed: Speech speed multiplier (0.5-2.0)
            
        Returns:
            True if successful
        """
        try:
            from gtts import gTTS
            
            logger.info(f"Generating speech using gTTS: {filename}")
            
            # Clean text for TTS
            text = self._clean_text_for_tts(text)
            
            # Generate speech
            tts = gTTS(text=text, lang='en', slow=False)
            
            # Save to file
            output_path = os.path.join(self.output_dir, filename)
            tts.save(output_path)
            
            logger.info(f"Successfully generated speech: {filename}")
            return True
            
        except Exception as e:
            logger.error(f"Error generating speech with gTTS: {str(e)}")
            return False
    
    def generate_speech_pyttsx3(self, text: str, filename: str, speed: float = 1.0) -> bool:
        """
        Generate speech using pyttsx3 (offline, no API key needed).
        
        Args:
            text: Text to convert to speech
            filename: Output audio filename
            speed: Speech speed multiplier (0.5-2.0)
            
        Returns:
            True if successful
        """
        try:
            import pyttsx3
            
            logger.info(f"Generating speech using pyttsx3: {filename}")
            
            # Clean text for TTS
            text = self._clean_text_for_tts(text)
            
            # Initialize engine
            engine = pyttsx3.init()
            
            # Configure voice
            engine.setProperty('rate', int(150 * speed))  # Speed
            engine.setProperty('volume', 0.9)  # Volume (0.0 to 1.0)
            
            # Set voice (prefer female)
            try:
                voices = engine.getProperty('voices')
                if len(voices) > 1:
                    engine.setProperty('voice', voices[1].id)  # Usually female voice
            except Exception as e:
                logger.warning(f"Could not set voice: {str(e)}")
            
            # Save to file
            output_path = os.path.join(self.output_dir, filename)
            engine.save_to_file(text, output_path)
            engine.runAndWait()
            
            logger.info(f"Successfully generated speech: {filename}")
            return True
            
        except Exception as e:
            logger.error(f"Error generating speech with pyttsx3: {str(e)}")
            return False
    
    def generate_speech(self, text: str, filename: str, speed: float = 1.0) -> bool:
        """
        Generate speech using best available TTS provider.
        
        Args:
            text: Text to convert to speech
            filename: Output audio filename
            speed: Speech speed multiplier
            
        Returns:
            True if successful
        """
        if self.use_gtts:
            return self.generate_speech_gtts(text, filename, speed)
        else:
            return self.generate_speech_pyttsx3(text, filename, speed)
    
    def _clean_text_for_tts(self, text: str) -> str:
        """
        Clean text for better TTS output.
        
        Args:
            text: Raw text
            
        Returns:
            Cleaned text
        """
        # Remove special characters but keep basic punctuation
        text = text.replace('&', 'and')
        text = text.replace('#', '')
        text = text.replace('@', 'at')
        text = text.replace('$', 'dollars')
        
        # Remove excessive whitespace
        text = ' '.join(text.split())
        
        return text
    
    def generate_from_script(self, content_package: Dict, filename_prefix: str = None) -> Optional[Dict]:
        """
        Generate speech from a content package.
        
        Args:
            content_package: Generated content with script
            filename_prefix: Custom filename prefix
            
        Returns:
            Updated package with audio file path, or None if failed
        """
        try:
            if filename_prefix is None:
                filename_prefix = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            filename = f"{filename_prefix}.mp3"
            script = content_package.get('script', '')
            
            logger.info(f"Generating audio for: {content_package.get('viral_title', 'Unknown')}")
            
            # Generate speech
            success = self.generate_speech(script, filename)
            
            if success:
                content_package['audio_file'] = filename
                content_package['audio_path'] = os.path.join(self.output_dir, filename)
                content_package['audio_generated'] = True
                content_package['updated_at'] = datetime.now().isoformat()
                
                logger.info(f"Successfully generated audio: {filename}")
                return content_package
            else:
                logger.error(f"Failed to generate audio for: {filename}")
                return None
                
        except Exception as e:
            logger.error(f"Error generating audio from script: {str(e)}")
            return None
    
    def process_multiple_scripts(self, content_packages: List[Dict]) -> List[Dict]:
        """
        Generate audio for multiple content packages.
        
        Args:
            content_packages: List of content packages
            
        Returns:
            Updated packages with audio files
        """
        logger.info(f"Processing {len(content_packages)} content packages for TTS...")
        
        updated_packages = []
        
        for i, package in enumerate(content_packages):
            prefix = f"gta6_short_{i+1}_{datetime.now().strftime('%H%M%S')}"
            updated = self.generate_from_script(package, prefix)
            
            if updated:
                updated_packages.append(updated)
        
        logger.info(f"Successfully processed {len(updated_packages)} packages")
        return updated_packages
    
    def save_packages_with_audio(self, packages: List[Dict], filename: str = "content_with_audio.json") -> bool:
        """
        Save content packages with audio file paths.
        
        Args:
            packages: Updated packages
            filename: Output filename
            
        Returns:
            True if successful
        """
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(packages, f, indent=2, ensure_ascii=False)
            logger.info(f"Saved {len(packages)} packages with audio to {filename}")
            return True
        except Exception as e:
            logger.error(f"Error saving packages: {str(e)}")
            return False
    
    def load_and_generate_audio(self, input_file: str = "content_packages.json", output_file: str = "content_with_audio.json") -> List[Dict]:
        """
        Load content packages and generate audio for all.
        
        Args:
            input_file: Input JSON file
            output_file: Output JSON file
            
        Returns:
            List of updated packages
        """
        try:
            with open(input_file, 'r', encoding='utf-8') as f:
                packages = json.load(f)
            
            logger.info(f"Loaded {len(packages)} packages from {input_file}")
            
            updated_packages = self.process_multiple_scripts(packages)
            self.save_packages_with_audio(updated_packages, output_file)
            
            return updated_packages
        except Exception as e:
            logger.error(f"Error in load_and_generate_audio: {str(e)}")
            return []
    
    def get_audio_duration(self, audio_file: str) -> Optional[float]:
        """
        Get audio file duration in seconds.
        Uses ffprobe if available.
        
        Args:
            audio_file: Path to audio file
            
        Returns:
            Duration in seconds, or None if unable to determine
        """
        try:
            audio_path = os.path.join(self.output_dir, audio_file)
            
            # Try using ffprobe (requires FFmpeg)
            result = subprocess.run(
                ['ffprobe', '-v', 'error', '-show_entries', 'format=duration',
                 '-of', 'default=noprint_wrappers=1:nokey=1:noprint_wrappers=1',
                 audio_path],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode == 0:
                try:
                    duration = float(result.stdout.strip())
                    logger.info(f"Audio duration: {duration:.2f}s")
                    return duration
                except ValueError:
                    pass
            
            # Fallback: try using mutagen if available
            try:
                from mutagen.mp3 import MP3
                audio = MP3(audio_path)
                duration = audio.info.length
                logger.info(f"Audio duration (via mutagen): {duration:.2f}s")
                return duration
            except ImportError:
                logger.warning("ffprobe and mutagen not available for duration detection")
                return None
                
        except Exception as e:
            logger.error(f"Error getting audio duration: {str(e)}")
            return None


if __name__ == "__main__":
    # Setup logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Test the TTS
    try:
        tts = TextToSpeech()
        packages = tts.load_and_generate_audio()
        
        print(f"\nGenerated audio for {len(packages)} packages")
        for pkg in packages:
            if pkg.get('audio_generated'):
                print(f"\n🔊 {pkg['viral_title']}")
                print(f"   Audio: {pkg['audio_file']}")
    except Exception as e:
        print(f"Error: {e}")
