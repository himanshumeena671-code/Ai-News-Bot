"""
Deduplication and Filtering Module
Removes duplicate news, clickbait, and unrelated content.
Single Responsibility: Filter and deduplicate articles.
"""

import logging
import json
from typing import List, Dict, Set
from difflib import SequenceMatcher

logger = logging.getLogger(__name__)


class NewsDuplicator:
    """Filters and deduplicates news articles."""
    
    # Keywords that indicate clickbait or unrelated content
    CLICKBAIT_KEYWORDS = [
        'you won\'t believe', 'shocking', 'leaked', 'exclusive',
        'leaked images', 'inside scoop', 'unbelievable', 'celebrity',
        'subscribe now', 'click here', 'shocking truth'
    ]
    
    # Keywords that must be present for GTA VI relevance
    GTA_KEYWORDS = [
        'gta', 'grand theft auto', 'rockstar', 'vi', 'six',
        'gameplay', 'trailer', 'news', 'announcement'
    ]
    
    def __init__(self, similarity_threshold: float = 0.85):
        """
        Initialize deduplicator.
        
        Args:
            similarity_threshold: Threshold for detecting duplicate titles (0-1)
        """
        self.similarity_threshold = similarity_threshold
        self.processed_titles = set()
    
    def is_clickbait(self, text: str) -> bool:
        """
        Detect if article is clickbait.
        
        Args:
            text: Article title or summary
            
        Returns:
            True if clickbait detected
        """
        text_lower = text.lower()
        
        # Check for clickbait patterns
        clickbait_count = sum(1 for keyword in self.CLICKBAIT_KEYWORDS if keyword in text_lower)
        
        # Check for ALL CAPS patterns (common in clickbait)
        caps_ratio = sum(1 for c in text if c.isupper()) / max(len(text), 1)
        
        return clickbait_count >= 2 or caps_ratio > 0.5
    
    def is_gta_related(self, title: str, summary: str) -> bool:
        """
        Check if article is GTA VI related.
        
        Args:
            title: Article title
            summary: Article summary
            
        Returns:
            True if GTA VI related
        """
        text = (title + " " + summary).lower()
        
        # Must contain at least one GTA-related keyword
        gta_found = sum(1 for keyword in self.GTA_KEYWORDS if keyword in text)
        
        # Filter out comparison articles unless they mention GTA VI specifically
        if 'vs' in text or 'compared' in text or 'better than' in text:
            return 'gta vi' in text or 'gta 6' in text
        
        return gta_found >= 1
    
    def calculate_similarity(self, str1: str, str2: str) -> float:
        """
        Calculate similarity between two strings.
        
        Args:
            str1: First string
            str2: Second string
            
        Returns:
            Similarity score (0-1)
        """
        return SequenceMatcher(None, str1.lower(), str2.lower()).ratio()
    
    def is_duplicate(self, title: str) -> bool:
        """
        Check if title is a duplicate.
        
        Args:
            title: Article title
            
        Returns:
            True if duplicate found
        """
        for processed_title in self.processed_titles:
            similarity = self.calculate_similarity(title, processed_title)
            if similarity >= self.similarity_threshold:
                logger.debug(f"Duplicate detected: {title[:50]}...")
                return True
        
        return False
    
    def filter_articles(self, articles: List[Dict]) -> List[Dict]:
        """
        Filter and deduplicate articles.
        
        Args:
            articles: List of raw articles
            
        Returns:
            Filtered list of unique, relevant articles
        """
        logger.info(f"Starting filtration of {len(articles)} articles...")
        
        filtered_articles = []
        removed_count = 0
        
        for article in articles:
            title = article.get('title', '')
            summary = article.get('summary', '')
            
            # Check if GTA related
            if not self.is_gta_related(title, summary):
                logger.debug(f"Removed non-GTA article: {title[:50]}...")
                removed_count += 1
                continue
            
            # Check for clickbait
            if self.is_clickbait(title):
                logger.debug(f"Removed clickbait: {title[:50]}...")
                removed_count += 1
                continue
            
            # Check for duplicates
            if self.is_duplicate(title):
                removed_count += 1
                continue
            
            # Add to filtered list
            filtered_articles.append(article)
            self.processed_titles.add(title)
        
        logger.info(f"Filtration complete: {len(filtered_articles)} articles kept, {removed_count} removed")
        return filtered_articles
    
    def save_filtered_news(self, articles: List[Dict], filename: str = "filtered_news.json") -> bool:
        """
        Save filtered news to JSON file.
        
        Args:
            articles: Filtered articles
            filename: Output filename
            
        Returns:
            True if successful
        """
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(articles, f, indent=2, ensure_ascii=False)
            logger.info(f"Saved {len(articles)} filtered articles to {filename}")
            return True
        except Exception as e:
            logger.error(f"Error saving filtered news: {str(e)}")
            return False
    
    def load_and_filter(self, input_file: str = "raw_news.json", output_file: str = "filtered_news.json") -> List[Dict]:
        """
        Load raw news and filter it.
        
        Args:
            input_file: Input JSON file
            output_file: Output JSON file
            
        Returns:
            Filtered articles
        """
        try:
            with open(input_file, 'r', encoding='utf-8') as f:
                articles = json.load(f)
            
            filtered = self.filter_articles(articles)
            self.save_filtered_news(filtered, output_file)
            
            return filtered
        except Exception as e:
            logger.error(f"Error in load_and_filter: {str(e)}")
            return []


if __name__ == "__main__":
    # Setup logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Test the deduplicator
    dedup = NewsDuplicator()
    filtered = dedup.load_and_filter()
    
    print(f"\nFiltered articles: {len(filtered)}")
    for article in filtered[:3]:
        print(f"\n✅ {article['title']}")
        print(f"   Source: {article['source']}")
