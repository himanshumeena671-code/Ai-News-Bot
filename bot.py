import feedparser
import json
from datetime import datetime

# GTA VI news sources
RSS_FEEDS = [
    "https://www.rockstargames.com/newswire/rss",
    "https://www.ign.com/rss",
]

news = []

for feed_url in RSS_FEEDS:
    try:
        feed = feedparser.parse(feed_url)

        for entry in feed.entries[:10]:
            text = (
                (entry.get("title", "") + " " +
                 entry.get("summary", "")).lower()
            )

            if any(keyword in text for keyword in [
                "gta", "grand theft auto", "gta vi", "gta 6", "rockstar"
            ]):
                news.append({
                    "title": entry.get("title", ""),
                    "summary": entry.get("summary", ""),
                    "link": entry.get("link", ""),
                    "published": entry.get("published", ""),
                    "scraped_at": datetime.utcnow().isoformat()
                })

    except Exception as e:
        print(f"Error reading {feed_url}: {e}")

with open("news.json", "w", encoding="utf-8") as f:
    json.dump(news, f, indent=4, ensure_ascii=False)

print(f"Saved {len(news)} news articles.")
