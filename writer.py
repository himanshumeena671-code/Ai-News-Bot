"""
Phase 2: AI Script Writer Module
Generates viral titles, hooks, scripts, and metadata using OpenRouter API.
Single Responsibility: Transform news into YouTube Shorts content.
"""

import requests
import json
import logging
from typing import Dict, List, Optional
import os
from datetime import datetime

logger = logging.getLogger(__name__)


class AIScriptWriter:
    """Generates AI-powered YouTube Shorts scripts and metadata."""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize AI script writer.
        
        Args:
            api_key: OpenRouter API key (uses OPENROUTER_API_KEY env if not provided)
        """
        self.api_key = api_key or os.getenv('OPENROUTER_API_KEY')
        
        if not self.api_key:
            raise ValueError("OPENROUTER_API_KEY not found in environment variables")
        
        self.api_url = "https://openrouter.ai/api/v1/chat/completions"
        self.model = "meta-llama/llama-2-7b-chat"  # Free tier model
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://github.com/himanshumeena671-code/Ai-News-Bot",
            "X-Title": "AI News Bot"
        }
    
    def generate_viral_title(self, article_title: str, summary: str) -> str:
        """
        Generate a viral YouTube Shorts title.
        
        Args:
            article_title: Original article title
            summary: Article summary
            
        Returns:
            Viral title (max 60 characters)
        """
        prompt = f"""Create a SHORT, VIRAL YouTube Shorts title (max 60 chars) for this GTA VI news.
Be catchy, use emojis, and create urgency.

Original Title: {article_title}
Summary: {summary}

Respond with ONLY the title, nothing else."""
        
        try:
            response = self._call_openrouter(prompt)
            title = response.strip()[:60]
            logger.info(f"Generated viral title: {title}")
            return title
        except Exception as e:
            logger.error(f"Error generating viral title: {str(e)}")
            return article_title[:60]
    
    def generate_hook(self, article_title: str, summary: str) -> str:
        """
        Generate a 3-second hook to grab attention.
        
        Args:
            article_title: Original article title
            summary: Article summary
            
        Returns:
            3-second hook (50-70 words)
        """
        prompt = f"""Create a SHORT, ATTENTION-GRABBING 3-second hook for a YouTube Short (50-70 words).
Must start with something shocking or exciting about GTA VI.

Article: {article_title}
{summary}

Respond with ONLY the hook text, nothing else."""
        
        try:
            response = self._call_openrouter(prompt)
            logger.info(f"Generated hook")
            return response.strip()
        except Exception as e:
            logger.error(f"Error generating hook: {str(e)}")
            return "Check out this amazing GTA VI news!"
    
    def generate_script(self, article_title: str, summary: str) -> str:
        """
        Generate a 30-45 second YouTube Shorts script.
        
        Args:
            article_title: Original article title
            summary: Article summary
            
        Returns:
            Full script with timestamps and narration
        """
        prompt = f"""Create a VIRAL YouTube Shorts script (30-45 seconds, ~100-150 words) for GTA VI news.
Format:
- Start with hook (shocking statement)
- Build excitement about the news
- Include specific details from the article
- End with call to action (Like, Subscribe, etc)

Article: {article_title}
{summary}

Respond with ONLY the script text, nothing else."""
        
        try:
            response = self._call_openrouter(prompt)
            logger.info(f"Generated script")
            return response.strip()
        except Exception as e:
            logger.error(f"Error generating script: {str(e)}")
            return "Breaking GTA VI news just dropped!"
    
    def generate_description(self, article_title: str, script: str, source_link: str) -> str:
        """
        Generate YouTube description.
        
        Args:
            article_title: Article title
            script: Generated script
            source_link: Link to original article
            
        Returns:
            YouTube description
        """
        description = f"""{article_title}

🎮 Latest GTA VI News and Updates

📖 Full Story:
{source_link}

✅ Subscribe for more GTA VI content!
✅ Like and comment your thoughts!
✅ Turn on notifications for new uploads!

#GTA6 #GrandTheftAuto #Gaming #News
"""
        return description
    
    def generate_hashtags(self, title: str, summary: str) -> List[str]:
        """
        Generate relevant hashtags.
        
        Args:
            title: Article title
            summary: Article summary
            
        Returns:
            List of hashtags
        """
        prompt = f"""Generate 10 trending hashtags for a YouTube Short about GTA VI.
Format: Just list hashtags separated by spaces.

Topic: {title}

Respond with ONLY hashtags, nothing else."""
        
        try:
            response = self._call_openrouter(prompt)
            hashtags = response.strip().split()
            return hashtags[:10]
        except Exception as e:
            logger.error(f"Error generating hashtags: {str(e)}")
            return ["#GTA6", "#Gaming", "#News", "#GrandTheftAuto"]
    
    def process_article(self, article: Dict) -> Dict:
        """
        Process a single article and generate all content.
        
        Args:
            article: Article dictionary with title, summary, link
            
        Returns:
            Complete content package with all generated materials
        """
        logger.info(f"Processing article: {article['title'][:50]}...")
        
        title = article.get('title', '')
        summary = article.get('summary', '')
        link = article.get('link', '')
        source = article.get('source', 'Unknown')
        
        try:
            # Generate all content
            viral_title = self.generate_viral_title(title, summary)
            hook = self.generate_hook(title, summary)
            script = self.generate_script(title, summary)
            description = self.generate_description(title, script, link)
            hashtags = self.generate_hashtags(title, summary)
            
            content_package = {
                'original_title': title,
                'original_source': source,
                'original_link': link,
                'viral_title': viral_title,
                'hook': hook,
                'script': script,
                'description': description,
                'hashtags': hashtags,
                'generated_at': datetime.now().isoformat(),
                'status': 'ready_for_tts'
            }
            
            logger.info(f"Successfully processed article")
            return content_package
            
        except Exception as e:
            logger.error(f"Error processing article: {str(e)}")
            return None
    
    def process_multiple_articles(self, articles: List[Dict], limit: int = 5) -> List[Dict]:
        """
        Process multiple articles.
        
        Args:
            articles: List of articles
            limit: Maximum articles to process (to avoid API quota)
            
        Returns:
            List of content packages
        """
        logger.info(f"Processing {min(len(articles), limit)} articles...")
        
        content_packages = []
        
        for i, article in enumerate(articles[:limit]):
            package = self.process_article(article)
            if package:
                content_packages.append(package)
            
            # Small delay to avoid rate limiting
            if i < limit - 1:
                import time
                time.sleep(2)
        
        logger.info(f"Successfully processed {len(content_packages)} articles")
        return content_packages
    
    def _call_openrouter(self, prompt: str, max_tokens: int = 500) -> str:
        """
        Call OpenRouter API.
        
        Args:
            prompt: Prompt for the model
            max_tokens: Maximum tokens in response
            
        Returns:
            Model response
        """
        try:
            payload = {
                "model": self.model,
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "temperature": 0.7,
                "max_tokens": max_tokens
            }
            
            response = requests.post(
                self.api_url,
                headers=self.headers,
                json=payload,
                timeout=30
            )
            
            response.raise_for_status()
            data = response.json()
            
            if 'choices' in data and len(data['choices']) > 0:
                return data['choices'][0]['message']['content']
            else:
                raise Exception("No valid response from API")
                
        except requests.exceptions.RequestException as e:
            logger.error(f"API request error: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Error calling OpenRouter: {str(e)}")
            raise
    
    def save_content_packages(self, packages: List[Dict], filename: str = "content_packages.json") -> bool:
        """
        Save generated content packages to JSON.
        
        Args:
            packages: List of content packages
            filename: Output filename
            
        Returns:
            True if successful
        """
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(packages, f, indent=2, ensure_ascii=False)
            logger.info(f"Saved {len(packages)} content packages to {filename}")
            return True
        except Exception as e:
            logger.error(f"Error saving content packages: {str(e)}")
            return False
    
    def load_and_process(self, input_file: str = "filtered_news.json", output_file: str = "content_packages.json", limit: int = 5) -> List[Dict]:
        """
        Load filtered news and process it.
        
        Args:
            input_file: Input JSON file
            output_file: Output JSON file
            limit: Maximum articles to process
            
        Returns:
            List of content packages
        """
        try:
            with open(input_file, 'r', encoding='utf-8') as f:
                articles = json.load(f)
            
            logger.info(f"Loaded {len(articles)} articles from {input_file}")
            packages = self.process_multiple_articles(articles, limit)
            self.save_content_packages(packages, output_file)
            
            return packages
        except Exception as e:
            logger.error(f"Error in load_and_process: {str(e)}")
            return []


if __name__ == "__main__":
    # Setup logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Test the writer
    try:
        writer = AIScriptWriter()
        packages = writer.load_and_process(limit=2)
        
        print(f"\nGenerated {len(packages)} content packages")
        for pkg in packages:
            print(f"\n🎯 {pkg['viral_title']}")
            print(f"Hook: {pkg['hook'][:100]}...")
    except Exception as e:
        print(f"Error: {e}")
