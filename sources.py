"""
Phase 1: News Collection Module
Collects GTA VI news from multiple sources with error handling and logging.
Single Responsibility: Fetch and aggregate news from various sources.
"""

import feedparser
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import json
import logging
from typing import List, Dict
import time

logger = logging.getLogger(__name__)


class NewsCollector:
    """Collects GTA VI news from multiple sources."""
    
    def __init__(self, timeout: int = 10):
        """
        Initialize news collector.
        
        Args:
            timeout: Request timeout in seconds
        """
        self.timeout = timeout
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        self.news_articles = []
    
    def fetch_google_news_rss(self) -> List[Dict]:
        """
        Fetch GTA VI news from Google News RSS feed.
        
        Returns:
            List of article dictionaries with title, link, published, source
        """
        try:
            logger.info("Fetching Google News RSS for GTA VI...")
            url = "https://news.google.com/rss/search?q=GTA+VI&hl=en-US&gl=US&ceid=US:en"
            
            feed = feedparser.parse(url)
            articles = []
            
            for entry in feed.entries[:20]:  # Limit to 20 articles
                article = {
                    'title': entry.get('title', ''),
                    'link': entry.get('link', ''),
                    'published': entry.get('published', datetime.now().isoformat()),
                    'source': 'Google News',
                    'summary': entry.get('summary', '')
                }
                articles.append(article)
            
            logger.info(f"Successfully fetched {len(articles)} articles from Google News")
            return articles
            
        except Exception as e:
            logger.error(f"Error fetching Google News RSS: {str(e)}")
            return []
    
    def fetch_rockstar_newswire(self) -> List[Dict]:
        """
        Fetch news from Rockstar Newswire RSS feed.
        
        Returns:
            List of article dictionaries
        """
        try:
            logger.info("Fetching Rockstar Newswire...")
            url = "https://www.rockstargames.com/newswire/feed"
            
            feed = feedparser.parse(url)
            articles = []
            
            for entry in feed.entries[:15]:
                # Filter for GTA VI related news
                title = entry.get('title', '').lower()
                summary = entry.get('summary', '').lower()
                
                if 'gta' in title or 'gta' in summary or 'grand theft' in title or 'grand theft' in summary:
                    article = {
                        'title': entry.get('title', ''),
                        'link': entry.get('link', ''),
                        'published': entry.get('published', datetime.now().isoformat()),
                        'source': 'Rockstar Newswire',
                        'summary': entry.get('summary', '')
                    }
                    articles.append(article)
            
            logger.info(f"Fetched {len(articles)} Rockstar Newswire articles")
            return articles
            
        except Exception as e:
            logger.error(f"Error fetching Rockstar Newswire: {str(e)}")
            return []
    
    def fetch_reddit_gta6(self) -> List[Dict]:
        """
        Fetch trending posts from Reddit r/GTA6 subreddit.
        
        Returns:
            List of article dictionaries
        """
        try:
            logger.info("Fetching Reddit r/GTA6 posts...")
            
            url = "https://reddit.com/r/GTA6/hot.json"
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            response = requests.get(url, headers=headers, timeout=self.timeout)
            response.raise_for_status()
            
            data = response.json()
            articles = []
            
            for post in data.get('data', {}).get('children', [])[:15]:
                post_data = post.get('data', {})
                article = {
                    'title': post_data.get('title', ''),
                    'link': f"https://reddit.com{post_data.get('permalink', '')}",
                    'published': datetime.fromtimestamp(post_data.get('created_utc', 0)).isoformat(),
                    'source': 'Reddit r/GTA6',
                    'summary': post_data.get('selftext', '')[:500]
                }
                articles.append(article)
            
            logger.info(f"Fetched {len(articles)} Reddit posts")
            return articles
            
        except Exception as e:
            logger.error(f"Error fetching Reddit r/GTA6: {str(e)}")
            return []
    
    def fetch_ign_gaming(self) -> List[Dict]:
        """
        Fetch gaming news from IGN RSS feed.
        
        Returns:
            List of article dictionaries
        """
        try:
            logger.info("Fetching IGN gaming news...")
            url = "https://feeds.ign.com/ign/all"
            
            feed = feedparser.parse(url)
            articles = []
            
            for entry in feed.entries[:20]:
                title = entry.get('title', '').lower()
                summary = entry.get('summary', '').lower()
                
                if 'gta' in title or 'gta' in summary or 'grand theft' in title or 'grand theft' in summary:
                    article = {
                        'title': entry.get('title', ''),
                        'link': entry.get('link', ''),
                        'published': entry.get('published', datetime.now().isoformat()),
                        'source': 'IGN',
                        'summary': entry.get('summary', '')
                    }
                    articles.append(article)
            
            logger.info(f"Fetched {len(articles)} IGN articles")
            return articles
            
        except Exception as e:
            logger.error(f"Error fetching IGN: {str(e)}")
            return []
    
    def fetch_gamerant(self) -> List[Dict]:
        """
        Fetch gaming news from GameRant RSS feed.
        
        Returns:
            List of article dictionaries
        """
        try:
            logger.info("Fetching GameRant news...")
            url = "https://gamerant.com/feed/"
            
            feed = feedparser.parse(url)
            articles = []
            
            for entry in feed.entries[:20]:
                title = entry.get('title', '').lower()
                summary = entry.get('summary', '').lower()
                
                if 'gta' in title or 'gta' in summary or 'grand theft' in title or 'grand theft' in summary:
                    article = {
                        'title': entry.get('title', ''),
                        'link': entry.get('link', ''),
                        'published': entry.get('published', datetime.now().isoformat()),
                        'source': 'GameRant',
                        'summary': entry.get('summary', '')
                    }
                    articles.append(article)
            
            logger.info(f"Fetched {len(articles)} GameRant articles")
            return articles
            
        except Exception as e:
            logger.error(f"Error fetching GameRant: {str(e)}")
            return []
    
    def fetch_dexerto(self) -> List[Dict]:
        """
        Fetch gaming news from Dexerto RSS feed.
        
        Returns:
            List of article dictionaries
        """
        try:
            logger.info("Fetching Dexerto news...")
            url = "https://www.dexerto.com/feed/"
            
            feed = feedparser.parse(url)
            articles = []
            
            for entry in feed.entries[:20]:
                title = entry.get('title', '').lower()
                summary = entry.get('summary', '').lower()
                
                if 'gta' in title or 'gta' in summary or 'grand theft' in title or 'grand theft' in summary:
                    article = {
                        'title': entry.get('title', ''),
                        'link': entry.get('link', ''),
                        'published': entry.get('published', datetime.now().isoformat()),
                        'source': 'Dexerto',
                        'summary': entry.get('summary', '')
                    }
                    articles.append(article)
            
            logger.info(f"Fetched {len(articles)} Dexerto articles")
            return articles
            
        except Exception as e:
            logger.error(f"Error fetching Dexerto: {str(e)}")
            return []
    
    def collect_all_news(self) -> List[Dict]:
        """
        Collect news from all sources.
        
        Returns:
            Combined list of all articles from all sources
        """
        logger.info("Starting news collection from all sources...")
        
        all_articles = []
        
        # Collect from all sources with small delay to avoid rate limiting
        all_articles.extend(self.fetch_google_news_rss())
        time.sleep(1)
        
        all_articles.extend(self.fetch_rockstar_newswire())
        time.sleep(1)
        
        all_articles.extend(self.fetch_reddit_gta6())
        time.sleep(1)
        
        all_articles.extend(self.fetch_ign_gaming())
        time.sleep(1)
        
        all_articles.extend(self.fetch_gamerant())
        time.sleep(1)
        
        all_articles.extend(self.fetch_dexerto())
        
        logger.info(f"Total articles collected: {len(all_articles)}")
        self.news_articles = all_articles
        
        return all_articles
    
    def save_to_json(self, filename: str = "raw_news.json") -> bool:
        """
        Save collected news to JSON file.
        
        Args:
            filename: Output filename
            
        Returns:
            True if successful, False otherwise
        """
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(self.news_articles, f, indent=2, ensure_ascii=False)
            logger.info(f"Saved {len(self.news_articles)} articles to {filename}")
            return True
        except Exception as e:
            logger.error(f"Error saving to JSON: {str(e)}")
            return False
    
    def load_from_json(self, filename: str = "raw_news.json") -> List[Dict]:
        """
        Load news from JSON file.
        
        Args:
            filename: Input filename
            
        Returns:
            List of articles
        """
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                articles = json.load(f)
            logger.info(f"Loaded {len(articles)} articles from {filename}")
            self.news_articles = articles
            return articles
        except Exception as e:
            logger.error(f"Error loading from JSON: {str(e)}")
            return []


if __name__ == "__main__":
    # Setup logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Test the collector
    collector = NewsCollector()
    news = collector.collect_all_news()
    collector.save_to_json()
    
    print(f"\nCollected {len(news)} articles")
    for article in news[:3]:
        print(f"\n📰 {article['title']}")
        print(f"   Source: {article['source']}")
        print(f"   Link: {article['link']}")
